"""
Job Scraper Engine
Scrapes jobs from Craigslist, Facebook, Google, Reddit, etc.
Deduplicates, consolidates, and makes available for contractors
"""

import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple
from difflib import SequenceMatcher
from job_scraper_config import (
    JOB_SOURCES, JOB_CATEGORIES, DEDUPLICATION_RULES,
    QUALITY_FILTERS, SERVICE_AREAS, COMMISSION_SETTINGS
)


class JobScraperEngine:
    """Main engine for scraping and managing job opportunities"""

    def __init__(self):
        self.data_dir = "data/jobs"
        self.ensure_directories()
        self.jobs = self._load_jobs()
        self.scrape_log = self._load_scrape_log()
        self.sources_status = {}

    def ensure_directories(self):
        """Create necessary directories"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs("data/scraped_raw", exist_ok=True)
        os.makedirs("data/deduplicated", exist_ok=True)
        os.makedirs("data/live_jobs", exist_ok=True)

    # ========================================================================
    # JOB SCRAPING - CRAIGSLIST
    # ========================================================================

    def scrape_craigslist(self) -> Dict:
        """
        Scrape jobs from Craigslist
        Returns: {"scraped": count, "errors": [], "sample_jobs": []}
        """
        import requests
        from bs4 import BeautifulSoup

        scraped_jobs = []
        errors = []

        try:
            config = JOB_SOURCES.get("craigslist", {})
            regions = config.get("regions", [])
            keywords = config.get("keywords", [])

            for region in regions:
                for keyword in keywords[:3]:  # Limit keywords to avoid over-scraping
                    try:
                        # Build URL
                        url = f"https://{region}.craigslist.org/search/sss?query={keyword}"

                        headers = config.get("headers", {})
                        response = requests.get(url, headers=headers, timeout=10)
                        response.raise_for_status()

                        soup = BeautifulSoup(response.content, 'html.parser')
                        listings = soup.find_all('li', class_='result-row')

                        for listing in listings[:20]:  # Get top 20 per search
                            try:
                                job = self._parse_craigslist_listing(listing, region, keyword)
                                if job:
                                    scraped_jobs.append(job)
                            except Exception as e:
                                errors.append(f"Error parsing listing: {str(e)}")

                    except Exception as e:
                        errors.append(f"Error scraping {region} {keyword}: {str(e)}")

            return {
                "source": "craigslist",
                "scraped": len(scraped_jobs),
                "errors": errors,
                "jobs": scraped_jobs,
                "timestamp": datetime.now().isoformat(),
            }

        except ImportError:
            return {
                "source": "craigslist",
                "scraped": 0,
                "errors": ["requests or BeautifulSoup not installed. Run: pip install requests beautifulsoup4"],
                "jobs": [],
            }

    def _parse_craigslist_listing(self, listing, region: str, keyword: str) -> Dict:
        """Parse individual Craigslist listing"""
        try:
            title_elem = listing.find('a', class_='result-title')
            title = title_elem.text if title_elem else ""
            url = title_elem['href'] if title_elem and 'href' in title_elem.attrs else ""

            date_elem = listing.find('time')
            posted_date = date_elem['datetime'] if date_elem and 'datetime' in date_elem.attrs else datetime.now().isoformat()

            price_elem = listing.find('span', class_='result-price')
            price_text = price_elem.text if price_elem else "$0"
            price = int(''.join(filter(str.isdigit, price_text))) if price_text else 0

            location_elem = listing.find('span', class_='result-meta')
            location = location_elem.text if location_elem else region

            return {
                "id": f"craigslist_{region}_{hash(title) % 10000}",
                "source": "craigslist",
                "title": title,
                "category": self._detect_category(title),
                "location": location,
                "region": region,
                "budget": price if price > 0 else None,
                "description": title,  # Brief description from title
                "posted_date": posted_date,
                "url": url,
                "contact_info": "See Craigslist posting",
                "raw_data": {
                    "keyword_searched": keyword,
                },
            }
        except Exception as e:
            return None

    # ========================================================================
    # JOB SCRAPING - FACEBOOK MARKETPLACE
    # ========================================================================

    def scrape_facebook_marketplace(self) -> Dict:
        """
        Scrape jobs from Facebook Marketplace
        Note: Requires Selenium for browser automation or API access
        """
        errors = []

        # Facebook scraping requires Selenium and is complex due to dynamic content
        # This is a template for integration

        return {
            "source": "facebook_marketplace",
            "scraped": 0,
            "errors": ["Facebook scraping requires Selenium setup. Instructions in documentation."],
            "jobs": [],
            "timestamp": datetime.now().isoformat(),
        }

    # ========================================================================
    # JOB SCRAPING - GOOGLE MAPS
    # ========================================================================

    def scrape_google_maps(self) -> Dict:
        """
        Scrape potential jobs from Google Maps reviews and Q&A
        Looks for homeowners asking for services
        """
        errors = []
        scraped_jobs = []

        try:
            config = JOB_SOURCES.get("google_maps", {})

            # This requires Google Maps API or web scraping
            # Would extract from business reviews and Q&A sections

            return {
                "source": "google_maps",
                "scraped": 0,
                "errors": ["Requires Google Maps API key. See setup guide."],
                "jobs": [],
                "timestamp": datetime.now().isoformat(),
            }
        except Exception as e:
            return {
                "source": "google_maps",
                "scraped": 0,
                "errors": [str(e)],
                "jobs": [],
            }

    # ========================================================================
    # JOB SCRAPING - REDDIT
    # ========================================================================

    def scrape_reddit(self) -> Dict:
        """
        Scrape jobs from Reddit r/forhire and local subreddits
        Requires PRAW (Python Reddit API Wrapper)
        """
        try:
            import praw

            config = JOB_SOURCES.get("reddit", {})
            subreddits = config.get("subreddits", [])
            scraped_jobs = []

            # PRAW setup would go here
            # reddit = praw.Reddit(client_id=..., client_secret=..., user_agent=...)

            return {
                "source": "reddit",
                "scraped": len(scraped_jobs),
                "jobs": scraped_jobs,
                "timestamp": datetime.now().isoformat(),
            }

        except ImportError:
            return {
                "source": "reddit",
                "scraped": 0,
                "errors": ["PRAW not installed. Run: pip install praw"],
                "jobs": [],
            }

    # ========================================================================
    # DIRECT JOB SUBMISSION
    # ========================================================================

    def add_job_directly(self, job_data: Dict) -> Dict:
        """
        Add a job directly (homeowner or contractor submits)
        """
        job_id = f"direct_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        job = {
            "id": job_id,
            "source": "direct_submission",
            "title": job_data.get("title"),
            "category": job_data.get("category") or self._detect_category(job_data.get("title", "")),
            "location": job_data.get("location"),
            "budget": float(job_data.get("budget", 0)),
            "description": job_data.get("description"),
            "posted_date": datetime.now().isoformat(),
            "contact_info": {
                "name": job_data.get("homeowner_name"),
                "phone": job_data.get("phone"),
                "email": job_data.get("email"),
            },
            "url": None,
            "status": "active",
            "created_at": datetime.now().isoformat(),
        }

        # Validate
        if not self._validate_job(job):
            return {"success": False, "error": "Job failed validation"}

        # Check for duplicates
        duplicates = self._find_duplicates(job)
        if duplicates:
            return {
                "success": False,
                "error": f"Job appears to be duplicate of {duplicates[0]['id']}",
                "similar_jobs": duplicates,
            }

        self.jobs[job_id] = job
        self._save_jobs()

        return {
            "success": True,
            "job_id": job_id,
            "message": f"Job posted successfully. {len(self.jobs)} total jobs available.",
        }

    # ========================================================================
    # JOB VALIDATION & QUALITY FILTERING
    # ========================================================================

    def _validate_job(self, job: Dict) -> bool:
        """Validate job meets quality standards"""
        filters = QUALITY_FILTERS

        # Check budget
        budget = job.get("budget", 0)
        if budget < filters.get("min_budget", 100):
            return False
        if filters.get("max_budget") and budget > filters.get("max_budget"):
            return False

        # Check contact info
        if filters.get("require_contact_info"):
            contact = job.get("contact_info", {})
            if not (contact.get("phone") or contact.get("email")):
                return False

        # Check description length
        desc = job.get("description", "")
        if len(desc) < filters.get("minimum_description_length", 20):
            return False

        # Check for spam keywords
        exclude = filters.get("exclude_keywords", [])
        desc_lower = (job.get("title", "") + " " + job.get("description", "")).lower()
        for keyword in exclude:
            if keyword.lower() in desc_lower:
                return False

        return True

    # ========================================================================
    # DEDUPLICATION
    # ========================================================================

    def _find_duplicates(self, new_job: Dict, threshold: float = 0.85) -> List[Dict]:
        """
        Find duplicate jobs using multiple methods:
        - Exact title match
        - Similar description
        - Same location + similar budget
        """
        duplicates = []
        rules = DEDUPLICATION_RULES

        for existing_job in self.jobs.values():
            if existing_job.get("status") == "expired":
                continue

            # Method 1: Exact title
            if rules.get("exact_title_match"):
                if new_job.get("title").lower() == existing_job.get("title").lower():
                    duplicates.append(existing_job)
                    continue

            # Method 2: Text similarity
            similarity = self._text_similarity(
                new_job.get("description", ""),
                existing_job.get("description", "")
            )
            if similarity > threshold:
                duplicates.append(existing_job)
                continue

            # Method 3: Location + Budget match
            if (new_job.get("location") == existing_job.get("location") and
                self._budget_similar(new_job.get("budget"), existing_job.get("budget"))):
                duplicates.append(existing_job)

        return duplicates

    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity (0-1)"""
        return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()

    def _budget_similar(self, budget1: float, budget2: float, variance: float = 0.1) -> bool:
        """Check if budgets are similar (within variance %)"""
        if not (budget1 and budget2):
            return False
        if budget1 == 0 or budget2 == 0:
            return False
        ratio = max(budget1, budget2) / min(budget1, budget2)
        return ratio < (1 + variance)

    # ========================================================================
    # JOB CATEGORIZATION
    # ========================================================================

    def _detect_category(self, text: str) -> str:
        """Auto-detect job category from text"""
        text_lower = text.lower()

        for category, details in JOB_CATEGORIES.items():
            keywords = details.get("keywords", [])
            for keyword in keywords:
                if keyword in text_lower:
                    return category

        return "handyman"  # Default category

    # ========================================================================
    # JOB RETRIEVAL & FILTERING
    # ========================================================================

    def get_active_jobs(self, filters: Dict = None) -> List[Dict]:
        """
        Get all active jobs with optional filtering
        filters: {
            "category": "plumbing",
            "location": "Dallas",
            "min_budget": 500,
            "max_budget": 5000,
            "min_days_old": 0,
        }
        """
        active_jobs = [j for j in self.jobs.values() if j.get("status") == "active"]

        if not filters:
            return active_jobs

        filtered = active_jobs

        if "category" in filters:
            filtered = [j for j in filtered if j.get("category") == filters["category"]]

        if "location" in filters:
            filtered = [j for j in filtered if filters["location"].lower() in j.get("location", "").lower()]

        if "min_budget" in filters:
            filtered = [j for j in filtered if j.get("budget", 0) >= filters["min_budget"]]

        if "max_budget" in filters:
            filtered = [j for j in filtered if j.get("budget", 0) <= filters["max_budget"]]

        return filtered

    def get_jobs_by_category(self) -> Dict[str, int]:
        """Get count of active jobs by category"""
        active = [j for j in self.jobs.values() if j.get("status") == "active"]
        by_category = {}

        for job in active:
            category = job.get("category", "unknown")
            by_category[category] = by_category.get(category, 0) + 1

        return by_category

    def get_jobs_by_location(self) -> Dict[str, int]:
        """Get count of active jobs by location"""
        active = [j for j in self.jobs.values() if j.get("status") == "active"]
        by_location = {}

        for job in active:
            location = job.get("location", "unknown")
            by_location[location] = by_location.get(location, 0) + 1

        return by_location

    # ========================================================================
    # JOB STATUS MANAGEMENT
    # ========================================================================

    def mark_job_expired(self, job_id: str):
        """Mark a job as expired/no longer accepting bids"""
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "expired"
            self.jobs[job_id]["expired_at"] = datetime.now().isoformat()
            self._save_jobs()

    def mark_job_completed(self, job_id: str, contractor_id: str):
        """Mark a job as completed"""
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = "completed"
            self.jobs[job_id]["completed_by"] = contractor_id
            self.jobs[job_id]["completed_at"] = datetime.now().isoformat()
            self._save_jobs()

    # ========================================================================
    # STATISTICS & REPORTING
    # ========================================================================

    def generate_scrape_report(self) -> Dict:
        """Generate overall scraping statistics"""
        active_jobs = len([j for j in self.jobs.values() if j.get("status") == "active"])
        completed_jobs = len([j for j in self.jobs.values() if j.get("status") == "completed"])
        expired_jobs = len([j for j in self.jobs.values() if j.get("status") == "expired"])

        total_budget = sum(j.get("budget", 0) for j in self.jobs.values() if j.get("status") == "active")

        return {
            "total_jobs": len(self.jobs),
            "active_jobs": active_jobs,
            "completed_jobs": completed_jobs,
            "expired_jobs": expired_jobs,
            "total_available_budget": total_budget,
            "average_job_value": total_budget / active_jobs if active_jobs > 0 else 0,
            "jobs_by_category": self.get_jobs_by_category(),
            "jobs_by_location": self.get_jobs_by_location(),
            "jobs_by_source": self._jobs_by_source(),
            "scrape_log": self.scrape_log[-10:] if self.scrape_log else [],  # Last 10 scrapes
        }

    def _jobs_by_source(self) -> Dict[str, int]:
        """Get job counts by source"""
        by_source = {}
        for job in self.jobs.values():
            source = job.get("source", "unknown")
            by_source[source] = by_source.get(source, 0) + 1
        return by_source

    # ========================================================================
    # DATA PERSISTENCE
    # ========================================================================

    def _load_jobs(self) -> Dict:
        """Load jobs from storage"""
        jobs_file = f"{self.data_dir}/all_jobs.json"
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                return json.load(f)
        return {}

    def _save_jobs(self):
        """Save jobs to storage"""
        jobs_file = f"{self.data_dir}/all_jobs.json"
        os.makedirs(os.path.dirname(jobs_file), exist_ok=True)
        with open(jobs_file, "w") as f:
            json.dump(self.jobs, f, indent=2)

    def _load_scrape_log(self) -> List:
        """Load scrape log"""
        log_file = f"{self.data_dir}/scrape_log.json"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                return json.load(f)
        return []

    def _save_scrape_log(self):
        """Save scrape log"""
        log_file = f"{self.data_dir}/scrape_log.json"
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        with open(log_file, "w") as f:
            json.dump(self.scrape_log, f, indent=2)
