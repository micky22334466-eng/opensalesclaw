"""
Job Scraper Configuration
Scrapes home improvement and contractor jobs from across the internet
Sources: Craigslist, Facebook Marketplace, Google, Indeed, Nextdoor, Reddit, etc.
"""

# ============================================================================
# 1. JOB SOURCES TO SCRAPE
# ============================================================================

JOB_SOURCES = {
    "craigslist": {
        "enabled": True,
        "name": "Craigslist Services",
        "categories": [
            "services",          # General services
            "biz+services",      # Business services
        ],
        "regions": [
            "dallas",            # Dallas metro
            "houston",           # Houston metro
            "austin",            # Austin metro
            "sanantonio",        # San Antonio metro
        ],
        "keywords": [
            "handyman",
            "plumber",
            "electrician",
            "painter",
            "roofing",
            "flooring",
            "drywall",
            "hvac",
            "kitchen",
            "bathroom",
            "remodel",
            "repair",
            "installation",
        ],
        "priority": 1,
        "scrape_frequency": "hourly",  # How often to scrape
        "job_age_limit_days": 30,      # Only jobs posted in last 30 days
    },

    "facebook_marketplace": {
        "enabled": True,
        "name": "Facebook Marketplace",
        "categories": [
            "services",
            "home_services",
        ],
        "locations": [
            "Dallas, TX",
            "Houston, TX",
            "Austin, TX",
            "San Antonio, TX",
        ],
        "keywords": [
            "handyman",
            "plumber",
            "electrician",
            "painting",
            "roofing",
            "flooring",
            "drywall",
            "hvac",
            "remodeling",
            "repair",
        ],
        "priority": 2,
        "scrape_frequency": "every 6 hours",
        "job_age_limit_days": 14,
    },

    "google_maps": {
        "enabled": True,
        "name": "Google Maps Reviews",
        "description": "Extract job requests from reviews and Q&A on Google Maps",
        "search_queries": [
            "handyman near me",
            "general contractor",
            "home repair",
            "plumbing services",
            "electrical services",
            "painting services",
            "roofing services",
        ],
        "locations": [
            "Dallas, TX",
            "Houston, TX",
            "Austin, TX",
        ],
        "priority": 2,
        "scrape_frequency": "daily",
        "job_age_limit_days": 7,
    },

    "google_local_services": {
        "enabled": True,
        "name": "Google Local Services Ads",
        "description": "Jobs posted on Google Local Services (contractors posting jobs they need help with)",
        "services": [
            "Handyman",
            "Plumbing",
            "Electrical",
            "Painting",
            "Roofing",
            "Flooring",
            "Drywall",
            "HVAC",
        ],
        "priority": 1,
        "scrape_frequency": "daily",
    },

    "indeed": {
        "enabled": True,
        "name": "Indeed Job Postings",
        "description": "Contract/gig work postings",
        "job_titles": [
            "handyman",
            "general contractor",
            "carpenter",
            "electrician",
            "plumber",
            "painter",
            "roofer",
        ],
        "locations": [
            "Dallas, TX",
            "Houston, TX",
            "Austin, TX",
        ],
        "priority": 3,
        "scrape_frequency": "daily",
    },

    "nextdoor": {
        "enabled": True,
        "name": "Nextdoor",
        "description": "Neighborhood requests for handymen and contractors",
        "neighborhoods": [
            "Dallas, TX",
            "Houston, TX",
            "Austin, TX",
        ],
        "priority": 2,
        "scrape_frequency": "every 6 hours",
        "job_age_limit_days": 7,
    },

    "reddit": {
        "enabled": True,
        "name": "Reddit",
        "description": "Jobs posted in r/forhire and local subreddits",
        "subreddits": [
            "forhire",
            "Dallas",
            "Houston",
            "Austin",
            "Texas",
            "slavelabour",
        ],
        "search_terms": [
            "handyman needed",
            "contractor needed",
            "repair needed",
            "contractor jobs",
        ],
        "priority": 3,
        "scrape_frequency": "daily",
    },

    "direct_submission": {
        "enabled": True,
        "name": "Direct Submission",
        "description": "Homeowners can submit jobs directly",
        "priority": 1,
        "scrape_frequency": "real-time",
    },
}

# ============================================================================
# 2. JOB TYPES & CATEGORIES
# ============================================================================

JOB_CATEGORIES = {
    "handyman": {
        "name": "General Handyman",
        "keywords": ["handyman", "odd jobs", "general repairs", "maintenance"],
        "avg_budget_min": 300,
        "avg_budget_max": 3000,
    },
    "plumbing": {
        "name": "Plumbing",
        "keywords": ["plumber", "plumbing", "pipe", "faucet", "toilet", "leak"],
        "avg_budget_min": 200,
        "avg_budget_max": 2500,
    },
    "electrical": {
        "name": "Electrical Work",
        "keywords": ["electrician", "electrical", "wiring", "outlet", "switch"],
        "avg_budget_min": 300,
        "avg_budget_max": 2500,
    },
    "painting": {
        "name": "Painting",
        "keywords": ["painter", "painting", "paint", "interior paint", "exterior paint"],
        "avg_budget_min": 500,
        "avg_budget_max": 4000,
    },
    "roofing": {
        "name": "Roofing",
        "keywords": ["roofer", "roofing", "roof", "leak", "shingles"],
        "avg_budget_min": 2000,
        "avg_budget_max": 15000,
    },
    "flooring": {
        "name": "Flooring",
        "keywords": ["flooring", "floor", "tile", "hardwood", "laminate"],
        "avg_budget_min": 1000,
        "avg_budget_max": 8000,
    },
    "drywall": {
        "name": "Drywall",
        "keywords": ["drywall", "sheetrock", "walls", "mudding", "taping"],
        "avg_budget_min": 400,
        "avg_budget_max": 3000,
    },
    "hvac": {
        "name": "HVAC",
        "keywords": ["hvac", "air conditioning", "heating", "ac repair", "furnace"],
        "avg_budget_min": 500,
        "avg_budget_max": 3500,
    },
    "kitchen": {
        "name": "Kitchen Remodeling",
        "keywords": ["kitchen", "remodel", "renovation", "cabinets", "countertop"],
        "avg_budget_min": 3000,
        "avg_budget_max": 25000,
    },
    "bathroom": {
        "name": "Bathroom Remodeling",
        "keywords": ["bathroom", "bath", "tile", "remodel", "renovation"],
        "avg_budget_min": 2000,
        "avg_budget_max": 12000,
    },
    "general_contractor": {
        "name": "General Contracting",
        "keywords": ["contractor", "construction", "build", "home renovation"],
        "avg_budget_min": 5000,
        "avg_budget_max": 50000,
    },
    "cleaning": {
        "name": "Cleaning & Maintenance",
        "keywords": ["cleaning", "pressure wash", "gutter", "yard work"],
        "avg_budget_min": 100,
        "avg_budget_max": 2000,
    },
}

# ============================================================================
# 3. SCRAPER SETTINGS
# ============================================================================

SCRAPER_SETTINGS = {
    # Craigslist
    "craigslist_base_url": "https://craigslist.org",
    "craigslist_headers": {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    },

    # Facebook (requires scraping library)
    "facebook_use_api": False,  # Set to True if you have API access
    "facebook_use_browser": True,  # Use Selenium for browser automation

    # Google Maps
    "google_maps_use_official_api": False,
    "google_maps_scraping_method": "browser",  # or "api"

    # Reddit API
    "reddit_use_official_api": True,  # Uses PRAW library
    "reddit_client_id": "${REDDIT_CLIENT_ID}",  # Set via environment
    "reddit_client_secret": "${REDDIT_CLIENT_SECRET}",

    # General scraping settings
    "rate_limit_per_source": 10,  # Max requests per minute per source
    "request_timeout": 30,        # Seconds
    "retry_on_failure": 3,        # Number of retries
    "user_agent_rotation": True,  # Rotate user agents
    "proxy_rotation": False,      # Use rotating proxies (optional)
}

# ============================================================================
# 4. JOB DEDUPLICATION RULES
# ============================================================================

DEDUPLICATION_RULES = {
    "exact_title_match": True,      # Same title = same job
    "location_radius_miles": 5,     # Jobs within 5 miles = same location
    "budget_variance_percent": 10,  # Budget within 10% = same job
    "date_window_days": 2,          # Posted within 2 days = likely same job
    "similarity_threshold": 0.85,   # 85% text similarity = likely duplicate
}

# ============================================================================
# 5. QUALITY FILTERS
# ============================================================================

QUALITY_FILTERS = {
    "min_budget": 100,              # Ignore jobs under $100
    "max_budget": 150000,           # Ignore jobs over $150k
    "require_contact_info": True,   # Must have phone or email
    "exclude_keywords": [
        "spam",
        "scam",
        "fake",
        "test",
        "deleted",
    ],
    "minimum_description_length": 20,  # Description must be at least 20 chars
}

# ============================================================================
# 6. SERVICE AREAS (GEOGRAPHIC)
# ============================================================================

SERVICE_AREAS = [
    "Dallas",
    "Arlington",
    "Irving",
    "Fort Worth",
    "Plano",
    "Frisco",
    "McKinney",
    "Houston",
    "Austin",
    "San Antonio",
]

SERVICE_AREA_COORDINATES = {
    "Dallas": {"lat": 32.7767, "lon": -96.7970},
    "Houston": {"lat": 29.7604, "lon": -95.3698},
    "Austin": {"lat": 30.2672, "lon": -97.7431},
    "San Antonio": {"lat": 29.4241, "lon": -98.4936},
}

# ============================================================================
# 7. PAYMENT & COMMISSION
# ============================================================================

COMMISSION_SETTINGS = {
    "platform_commission": 0.15,    # You take 15%
    "contractor_cut": 0.85,         # They get 85%
    "payment_methods": [
        "stripe",
        "paypal",
        "direct_deposit",
    ],
    "contractor_payout_frequency": "weekly",
    "minimum_payout_amount": 100,
}

# ============================================================================
# 8. JOB MATCHING FOR CONTRACTORS
# ============================================================================

CONTRACTOR_MATCHING = {
    "enabled": True,
    "match_by_specialty": True,     # Match by contractor skills
    "match_by_location": True,      # Match by service area
    "match_by_availability": True,  # Match by workload capacity
    "match_by_rating": True,        # Prefer higher rated
    "show_top_matches": 5,          # Show top 5 matches
    "auto_notify": True,            # Auto-notify matching contractors
}

# ============================================================================
# 9. NOTIFICATION SETTINGS
# ============================================================================

NOTIFICATION_TEMPLATES = {
    "new_job_for_contractor": """
NEW JOB POSTED - {category}

Location: {location}
Budget: ${budget_min} - ${budget_max}
Posted: {posted_date}
Match Score: {match_percent}%

Description:
{description}

Contact Info:
{contact_info}

View Full Posting: {job_url}

Your Commission: You keep 85%, Platform 15%
    """,

    "job_status_update": """
JOB STATUS UPDATE: {job_id}

Status: {status}
Category: {category}
Location: {location}
Budget: ${budget}

Latest Activity: {latest_activity}
    """,
}

# ============================================================================
# 10. ANALYTICS & REPORTING
# ============================================================================

ANALYTICS_CONFIG = {
    "track_metrics": [
        "jobs_scraped_daily",
        "unique_jobs_found",
        "duplicates_removed",
        "jobs_by_source",
        "jobs_by_category",
        "jobs_by_budget_range",
        "contractors_notified",
        "job_applications",
        "completion_rate",
        "average_commission_per_job",
        "total_platform_revenue",
    ],
    "daily_report": True,
    "weekly_report": True,
    "monthly_report": True,
}

# ============================================================================
# 11. CONTRACTOR PROFILE FIELDS
# ============================================================================

CONTRACTOR_PROFILE_TEMPLATE = {
    "name": "",
    "phone": "",
    "email": "",
    "specialties": [],              # Jobs they do
    "service_areas": [],            # Where they work
    "bio": "",
    "website": "",
    "social_media": {},
    "rating": 0.0,
    "reviews_count": 0,
    "completed_jobs": 0,
    "average_job_value": 0,
    "availability": "available",    # available, booked, on_break
    "job_preferences": {
        "min_budget": 100,
        "max_budget": 50000,
        "job_size": ["small", "medium", "large"],
    },
    "response_time_hours": 24,
}

# ============================================================================
# 12. DATA RETENTION POLICY
# ============================================================================

DATA_RETENTION = {
    "keep_jobs_days": 90,           # Keep job listings for 90 days
    "archive_completed_jobs": True,
    "cleanup_frequency": "weekly",
    "auto_remove_expired": True,
}
