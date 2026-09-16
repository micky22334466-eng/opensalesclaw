"""
Job Dispatcher Core Engine
Matches jobs to contractors, tracks pipeline, and calculates commissions
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple
from job_dispatcher_config import (
    JOB_TYPES, JOB_SIZES, SERVICE_AREAS, CONTRACTOR_DATABASE,
    MATCHING_WEIGHTS, PIPELINE_STAGES, COMMISSION_CONFIG, DISTRIBUTION_CONFIG
)


class JobDispatcher:
    """Main engine for matching jobs to contractors and tracking pipeline"""

    def __init__(self):
        self.contractors = CONTRACTOR_DATABASE
        self.data_dir = "data"
        self.ensure_directories()
        self.jobs = self._load_jobs()
        self.pipeline_log = self._load_pipeline_log()
        self.commissions = self._load_commissions()

    def ensure_directories(self):
        """Create necessary data directories"""
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(f"{self.data_dir}/jobs", exist_ok=True)
        os.makedirs(f"{self.data_dir}/commissions", exist_ok=True)

    # ========================================================================
    # JOB MANAGEMENT
    # ========================================================================

    def post_new_job(self, job_data: Dict) -> Dict:
        """
        Post a new job to the system
        job_data: {
            "title": "Bathroom Remodel",
            "type": "bathroom",
            "location": "Dallas",
            "budget": 5000,
            "description": "Full bathroom renovation",
            "timeline": "2 weeks",
            "homeowner_name": "John Doe",
            "homeowner_phone": "(214) 555-1234",
            "homeowner_email": "john@example.com",
            "source": "direct_submission"
        }
        """
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        job = {
            "id": job_id,
            "title": job_data.get("title"),
            "type": job_data.get("type"),
            "location": job_data.get("location"),
            "budget": float(job_data.get("budget", 0)),
            "description": job_data.get("description"),
            "timeline": job_data.get("timeline"),
            "homeowner_name": job_data.get("homeowner_name"),
            "homeowner_phone": job_data.get("homeowner_phone"),
            "homeowner_email": job_data.get("homeowner_email"),
            "source": job_data.get("source", "unknown"),
            "status": "new",
            "created_at": datetime.now().isoformat(),
            "sent_to": [],  # Contractors we've contacted
            "accepted_by": None,  # Who accepted
            "completed_at": None,
            "paid_at": None,
        }

        self.jobs[job_id] = job
        self._save_jobs()
        return job

    def estimate_job_size(self, budget: float) -> str:
        """Estimate job size from budget"""
        if budget < 2000:
            return "small"
        elif budget < 8000:
            return "medium"
        else:
            return "large"

    # ========================================================================
    # MATCHING ALGORITHM
    # ========================================================================

    def find_matching_contractors(self, job: Dict) -> List[Tuple[str, float]]:
        """
        Find contractors for a job and score them
        Returns: [(contractor_id, match_score), ...]
        """
        job_type = job.get("type")
        job_location = job.get("location")
        job_budget = job.get("budget")
        job_size = self.estimate_job_size(job_budget)

        matches = []

        for contractor_id, contractor in self.contractors.items():
            score = 0.0

            # 1. SPECIALTY MATCH (40% weight)
            # Does contractor specialize in this job type?
            if job_type in JOB_TYPES:
                needed_specialties = JOB_TYPES[job_type]["specialties_needed"]
                contractor_specialties = contractor.get("specialties", [])

                specialty_matches = len(set(needed_specialties) & set(contractor_specialties))
                specialty_score = (specialty_matches / len(needed_specialties)) * 100
                score += (specialty_score / 100) * MATCHING_WEIGHTS["specialty_match"]

            # 2. LOCATION MATCH (25% weight)
            # Does contractor service this area?
            if job_location in contractor.get("service_areas", []):
                score += MATCHING_WEIGHTS["location_match"]

            # 3. AVAILABILITY (20% weight)
            # Do they have capacity?
            if contractor.get("availability") == "available":
                current = contractor.get("currently_active", 0)
                max_jobs = contractor.get("max_jobs_active", 5)
                if current < max_jobs:
                    availability_score = (1 - current / max_jobs)
                    score += availability_score * MATCHING_WEIGHTS["availability"]

            # 4. JOB SIZE FIT (10% weight)
            # Do they take this size of job?
            if job_size in contractor.get("job_size", []):
                score += MATCHING_WEIGHTS["job_size_fit"]

            # 5. RATING BONUS (5% weight)
            # Higher rated contractors get slight boost
            rating = contractor.get("rating", 3.0)
            rating_score = (rating - 3.0) / 2.0  # Normalize to 0-1
            score += rating_score * MATCHING_WEIGHTS["rating_bonus"]

            # Convert to percentage (0-100)
            match_percentage = min(100, score * 100)

            if match_percentage > 30:  # Only return matches >30%
                matches.append((contractor_id, match_percentage))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    # ========================================================================
    # JOB DISTRIBUTION
    # ========================================================================

    def distribute_job_to_contractors(self, job_id: str) -> Dict:
        """
        Send job to matching contractors via text/email/call
        Returns distribution report
        """
        job = self.jobs.get(job_id)
        if not job:
            return {"success": False, "error": "Job not found"}

        # Find matches
        matches = self.find_matching_contractors(job)
        max_to_send = DISTRIBUTION_CONFIG.get("max_contractors_per_job", 5)
        selected = matches[:max_to_send]

        distribution_report = {
            "job_id": job_id,
            "total_matches": len(matches),
            "contacted": len(selected),
            "contacts": [],
        }

        # Record who we contacted
        for contractor_id, match_score in selected:
            contractor = self.contractors[contractor_id]

            contact_record = {
                "contractor_id": contractor_id,
                "contractor_name": contractor.get("name"),
                "match_score": match_score,
                "methods": DISTRIBUTION_CONFIG.get("contact_methods", []),
                "sent_at": datetime.now().isoformat(),
            }

            distribution_report["contacts"].append(contact_record)
            job["sent_to"].append({
                "contractor_id": contractor_id,
                "sent_at": datetime.now().isoformat(),
                "match_score": match_score,
                "status": "pending",
            })

        job["status"] = "sent"
        self._save_jobs()
        return distribution_report

    # ========================================================================
    # PIPELINE TRACKING
    # ========================================================================

    def update_job_status(self, job_id: str, new_status: str, contractor_id: str = None) -> Dict:
        """
        Update job status in pipeline
        Stages: new → sent → contacted → accepted → in_progress → completed → paid
        """
        job = self.jobs.get(job_id)
        if not job:
            return {"success": False, "error": "Job not found"}

        old_status = job.get("status")
        job["status"] = new_status

        # Track pipeline movement
        log_entry = {
            "job_id": job_id,
            "stage": new_status,
            "contractor_id": contractor_id,
            "timestamp": datetime.now().isoformat(),
            "job_value": job.get("budget"),
        }

        # If accepted, mark which contractor
        if new_status == "accepted" and contractor_id:
            job["accepted_by"] = contractor_id
            self.contractors[contractor_id]["currently_active"] += 1

        # If completed, record completion
        if new_status == "completed":
            job["completed_at"] = datetime.now().isoformat()

        # If paid, record payment and calculate commission
        if new_status == "paid":
            job["paid_at"] = datetime.now().isoformat()
            self._calculate_commission(job_id, job, contractor_id)

        self.pipeline_log.append(log_entry)
        self._save_pipeline_log()
        self._save_jobs()

        return {
            "success": True,
            "job_id": job_id,
            "old_status": old_status,
            "new_status": new_status,
        }

    # ========================================================================
    # COMMISSION MANAGEMENT
    # ========================================================================

    def _calculate_commission(self, job_id: str, job: Dict, contractor_id: str):
        """Calculate and record commission"""
        job_value = job.get("budget", 0)

        platform_cut = job_value * COMMISSION_CONFIG.get("platform_cut", 0.15)
        contractor_cut = job_value * COMMISSION_CONFIG.get("contractor_cut", 0.85)

        commission_record = {
            "job_id": job_id,
            "contractor_id": contractor_id,
            "job_value": job_value,
            "your_commission": platform_cut,
            "contractor_earnings": contractor_cut,
            "commission_rate": COMMISSION_CONFIG.get("platform_cut", 0.15),
            "date": datetime.now().isoformat(),
        }

        self.commissions.append(commission_record)

        # Update contractor total earnings
        if contractor_id in self.contractors:
            contractor = self.contractors[contractor_id]
            contractor["total_earnings"] = contractor.get("total_earnings", 0) + job_value
            contractor["platform_earnings"] = contractor.get("platform_earnings", 0) + platform_cut

        self._save_commissions()

    def get_commission_report(self) -> Dict:
        """Generate overall commission report"""
        total_job_value = sum(c.get("job_value", 0) for c in self.commissions)
        total_your_cut = sum(c.get("your_commission", 0) for c in self.commissions)
        total_contractor_cut = sum(c.get("contractor_earnings", 0) for c in self.commissions)

        return {
            "total_jobs_paid": len(self.commissions),
            "total_job_value": total_job_value,
            "your_total_commission": total_your_cut,
            "contractor_total_earnings": total_contractor_cut,
            "by_contractor": self._commissions_by_contractor(),
        }

    def _commissions_by_contractor(self) -> Dict:
        """Group commissions by contractor"""
        by_contractor = {}

        for commission in self.commissions:
            contractor_id = commission.get("contractor_id")
            if contractor_id not in by_contractor:
                by_contractor[contractor_id] = {
                    "jobs": 0,
                    "total_value": 0,
                    "your_cut": 0,
                    "their_cut": 0,
                }

            by_contractor[contractor_id]["jobs"] += 1
            by_contractor[contractor_id]["total_value"] += commission.get("job_value", 0)
            by_contractor[contractor_id]["your_cut"] += commission.get("your_commission", 0)
            by_contractor[contractor_id]["their_cut"] += commission.get("contractor_earnings", 0)

        return by_contractor

    # ========================================================================
    # DATA PERSISTENCE
    # ========================================================================

    def _load_jobs(self) -> Dict:
        """Load jobs from storage"""
        jobs_file = f"{self.data_dir}/jobs.json"
        if os.path.exists(jobs_file):
            with open(jobs_file, "r") as f:
                return json.load(f)
        return {}

    def _save_jobs(self):
        """Save jobs to storage"""
        jobs_file = f"{self.data_dir}/jobs.json"
        with open(jobs_file, "w") as f:
            json.dump(self.jobs, f, indent=2)

    def _load_pipeline_log(self) -> List:
        """Load pipeline log"""
        log_file = f"{self.data_dir}/pipeline_log.json"
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                return json.load(f)
        return []

    def _save_pipeline_log(self):
        """Save pipeline log"""
        log_file = f"{self.data_dir}/pipeline_log.json"
        with open(log_file, "w") as f:
            json.dump(self.pipeline_log, f, indent=2)

    def _load_commissions(self) -> List:
        """Load commission records"""
        commission_file = f"{self.data_dir}/commissions.json"
        if os.path.exists(commission_file):
            with open(commission_file, "r") as f:
                return json.load(f)
        return []

    def _save_commissions(self):
        """Save commission records"""
        commission_file = f"{self.data_dir}/commissions.json"
        with open(commission_file, "w") as f:
            json.dump(self.commissions, f, indent=2)

    # ========================================================================
    # REPORTS
    # ========================================================================

    def generate_dashboard_report(self) -> Dict:
        """Generate overall dashboard report"""
        jobs_by_status = {}
        for status in PIPELINE_STAGES:
            jobs_by_status[status] = len([j for j in self.jobs.values() if j.get("status") == status])

        commission_report = self.get_commission_report()

        return {
            "jobs_overview": jobs_by_status,
            "total_jobs": len(self.jobs),
            "active_contractors": len([c for c in self.contractors.values() if c.get("availability") == "available"]),
            "total_contractors": len(self.contractors),
            "commissions": commission_report,
            "pipeline_flow": self._calculate_conversion_rates(),
        }

    def _calculate_conversion_rates(self) -> Dict:
        """Calculate pipeline conversion rates"""
        total_jobs = len(self.jobs) or 1  # Avoid division by zero

        completed = len([j for j in self.jobs.values() if j.get("status") == "completed"])
        paid = len([j for j in self.jobs.values() if j.get("status") == "paid"])
        accepted = len([j for j in self.jobs.values() if j.get("status") == "accepted"])

        return {
            "sent_to_completed": f"{(completed / total_jobs * 100):.1f}%",
            "completed_to_paid": f"{(paid / completed * 100):.1f}%" if completed else "0%",
            "sent_to_accepted": f"{(accepted / total_jobs * 100):.1f}%",
        }
