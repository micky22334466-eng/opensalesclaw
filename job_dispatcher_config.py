"""
Job Dispatcher Configuration
Matches homeowner jobs to contractor specialists
Handles distribution, tracking, and commission calculation
"""

# ============================================================================
# 1. CONTRACTOR PROFILES
# ============================================================================

CONTRACTOR_DATABASE = {
    "contractor_1": {
        "name": "ABC Handyman Services",
        "phone": "(214) 555-0101",
        "email": "info@abchandyman.com",
        "specialties": ["handyman", "general_repair", "painting"],  # Job types they do
        "service_areas": ["Dallas", "Arlington", "Irving"],  # Where they work
        "availability": "available",  # available, booked, on_break
        "job_size": ["small", "medium", "large"],  # What size jobs they take
        "max_jobs_active": 5,  # Max concurrent jobs
        "currently_active": 2,  # Jobs in progress now
        "rating": 4.8,
        "reviews": 87,
        "total_earnings": 12500.00,  # Lifetime earnings before commission
        "platform_earnings": 1875.00,  # Your commission (15% of $12500)
        "commission_rate": 0.15,  # You take 15%, they get 85%
    },
    "contractor_2": {
        "name": "Dallas Plumbing Pros",
        "phone": "(214) 555-0102",
        "email": "contact@dallasplumbing.com",
        "specialties": ["plumbing", "water_damage"],
        "service_areas": ["Dallas", "Plano", "Frisco"],
        "availability": "available",
        "job_size": ["small", "medium"],  # Only small-medium
        "max_jobs_active": 3,
        "currently_active": 1,
        "rating": 4.6,
        "reviews": 142,
        "total_earnings": 18500.00,
        "platform_earnings": 2775.00,
        "commission_rate": 0.15,
    },
    # Add more contractors...
}

# ============================================================================
# 2. JOB CATEGORIES & MATCHING RULES
# ============================================================================

JOB_TYPES = {
    "handyman": {
        "name": "General Handyman Work",
        "specialties_needed": ["handyman", "general_repair"],
        "avg_job_size": "medium",
        "avg_budget_min": 500,
        "avg_budget_max": 3000,
    },
    "plumbing": {
        "name": "Plumbing Services",
        "specialties_needed": ["plumbing"],
        "avg_job_size": "small",
        "avg_budget_min": 300,
        "avg_budget_max": 2000,
    },
    "electrical": {
        "name": "Electrical Work",
        "specialties_needed": ["electrical"],
        "avg_job_size": "small",
        "avg_budget_min": 400,
        "avg_budget_max": 2500,
    },
    "painting": {
        "name": "Painting Services",
        "specialties_needed": ["painting", "general_repair"],
        "avg_job_size": "medium",
        "avg_budget_min": 800,
        "avg_budget_max": 4000,
    },
    "roofing": {
        "name": "Roofing Work",
        "specialties_needed": ["roofing"],
        "avg_job_size": "large",
        "avg_budget_min": 3000,
        "avg_budget_max": 15000,
    },
    "kitchen": {
        "name": "Kitchen Remodeling",
        "specialties_needed": ["remodeling", "kitchen"],
        "avg_job_size": "large",
        "avg_budget_min": 5000,
        "avg_budget_max": 25000,
    },
    "bathroom": {
        "name": "Bathroom Remodeling",
        "specialties_needed": ["remodeling", "bathroom"],
        "avg_job_size": "medium",
        "avg_budget_min": 3000,
        "avg_budget_max": 12000,
    },
    "flooring": {
        "name": "Flooring Installation",
        "specialties_needed": ["flooring"],
        "avg_job_size": "medium",
        "avg_budget_min": 1000,
        "avg_budget_max": 5000,
    },
    "hvac": {
        "name": "HVAC Services",
        "specialties_needed": ["hvac"],
        "avg_job_size": "medium",
        "avg_budget_min": 800,
        "avg_budget_max": 4000,
    },
    "drywall": {
        "name": "Drywall & Finishing",
        "specialties_needed": ["drywall"],
        "avg_job_size": "small",
        "avg_budget_min": 500,
        "avg_budget_max": 2500,
    },
}

# ============================================================================
# 3. JOB SIZE DEFINITIONS
# ============================================================================

JOB_SIZES = {
    "small": {
        "name": "Small Job",
        "duration": "1-2 days",
        "budget_range": "$300-2000",
        "complexity": "Low",
        "examples": ["faucet repair", "outlet installation", "touch-up painting"],
    },
    "medium": {
        "name": "Medium Job",
        "duration": "3-7 days",
        "budget_range": "$2000-8000",
        "complexity": "Medium",
        "examples": ["bathroom remodel", "kitchen upgrade", "deck repair"],
    },
    "large": {
        "name": "Large Job",
        "duration": "2+ weeks",
        "budget_range": "$8000+",
        "complexity": "High",
        "examples": ["full kitchen remodel", "roof replacement", "major renovation"],
    },
}

# ============================================================================
# 4. MATCHING ALGORITHM WEIGHTS
# ============================================================================

MATCHING_WEIGHTS = {
    "specialty_match": 0.40,      # Most important: Do they do this type of work?
    "location_match": 0.25,       # Are they in the service area?
    "availability": 0.20,         # Do they have capacity?
    "job_size_fit": 0.10,         # Do they take this size of job?
    "rating_bonus": 0.05,         # Higher rated = slight preference
}

# ============================================================================
# 5. DISTRIBUTION SETTINGS
# ============================================================================

DISTRIBUTION_CONFIG = {
    "contact_methods": ["text", "email", "call"],  # How to reach contractors
    "text_delay": 0,              # Send SMS immediately
    "email_delay": 0,             # Send email immediately
    "call_delay": 300,            # Call 5 minutes after text/email
    "max_contractors_per_job": 5, # Send to top 5 matches
    "resend_delay_hours": 24,     # Resend to available contractors after 24h
    "response_timeout_hours": 2,  # How long to wait for response
}

# ============================================================================
# 6. COMMISSION SETTINGS
# ============================================================================

COMMISSION_CONFIG = {
    "platform_cut": 0.15,         # You take 15%
    "contractor_cut": 0.85,       # They get 85%
    "min_job_value": 100,         # Don't track jobs under $100
    "tax_form_threshold": 20000,  # Send 1099 if contractor earns $20k+
}

# ============================================================================
# 7. PIPELINE TRACKING STAGES
# ============================================================================

PIPELINE_STAGES = [
    "new",           # Job just posted
    "sent",          # Sent to contractors
    "contacted",     # Contractor responded
    "accepted",      # Contractor accepted job
    "in_progress",   # Work started
    "completed",     # Work finished
    "paid",          # Payment processed
    "cancelled",     # Job cancelled
]

# ============================================================================
# 8. SERVICE AREAS (GEOGRAPHIC TARGETING)
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
]

# ============================================================================
# 9. DATA SOURCES FOR JOBS
# ============================================================================

JOB_SOURCES = {
    "google_maps": {
        "enabled": True,
        "description": "Jobs from Google Maps (homeowner posts, reviews)",
        "priority": 1,
    },
    "craigslist": {
        "enabled": True,
        "description": "Jobs from Craigslist services section",
        "priority": 2,
    },
    "facebook_marketplace": {
        "enabled": True,
        "description": "Jobs from Facebook Marketplace",
        "priority": 3,
    },
    "direct_submission": {
        "enabled": True,
        "description": "Homeowners submit projects directly",
        "priority": 1,
    },
    "referral": {
        "enabled": True,
        "description": "Referrals from contractors/networks",
        "priority": 2,
    },
}

# ============================================================================
# 10. NOTIFICATION TEMPLATES
# ============================================================================

NOTIFICATION_TEMPLATES = {
    "job_offer_text": """
Hey {contractor_name}!

NEW JOB AVAILABLE:
{job_type} in {location}
Budget: ${budget}
Size: {job_size}

Your match score: {match_score}%

Reply YES to accept or NO to pass.
    """,

    "job_offer_email": """
Subject: New {job_type} Job Available - {location}

Hi {contractor_name},

A new job matching your skills is available:

Job Type: {job_type}
Location: {location}
Budget: ${budget}
Size: {job_size}
Timeline: {timeline}

Match Score: {match_score}%
(Based on your specialties, location, and availability)

Click to accept: {acceptance_link}

Your 15% Commission: ${your_cut}
Platform Fee: ${platform_cut}

Best,
The Job Dispatcher Team
    """,

    "completion_notification": """
Subject: Payment Processed - {job_type} Job

Hi {contractor_name},

Job completed! Payment has been processed.

Job: {job_type} in {location}
Job Value: ${total_value}
Your Earnings: ${contractor_earnings} (85%)
Platform Fee: ${platform_earnings} (15%)

Total Lifetime Earnings: ${lifetime_earnings}

Thanks for your work!
    """,
}

# ============================================================================
# 11. QUALITY THRESHOLDS
# ============================================================================

QUALITY_FILTERS = {
    "min_contractor_rating": 3.5,   # Only work with contractors 3.5+ rated
    "min_contractor_reviews": 5,    # At least some history
    "min_job_budget": 300,          # Don't take jobs under $300
    "require_homeowner_contact": True,  # Must have contact info
}

# ============================================================================
# 12. REPORTS & ANALYTICS
# ============================================================================

ANALYTICS_CONFIG = {
    "track_metrics": [
        "jobs_posted",
        "jobs_distributed",
        "jobs_accepted",
        "jobs_completed",
        "completion_rate",
        "avg_commission",
        "contractor_utilization",
        "job_matching_quality",
    ],
}
