#!/usr/bin/env python3
"""
Job Scraper Quick Test
Posts sample jobs, demonstrates filtering and retrieval
"""

from job_scraper_engine import JobScraperEngine
from datetime import datetime

def main():
    print("\n" + "="*70)
    print("  JOB SCRAPER - QUICK TEST")
    print("="*70 + "\n")

    # Initialize scraper
    engine = JobScraperEngine()
    print("✓ Job Scraper Engine initialized")
    print(f"✓ Existing jobs in database: {len(engine.jobs)}\n")

    # ========================================================================
    # STEP 1: ADD SAMPLE JOBS (Simulating scraped jobs)
    # ========================================================================
    print("STEP 1: ADDING SAMPLE JOBS (From various sources)")
    print("-" * 70)

    sample_jobs = [
        {
            "title": "Bathroom remodel needed - Dallas",
            "category": "bathroom",
            "location": "Dallas, TX",
            "budget": 5000,
            "description": "Full bathroom renovation including tile, fixtures, paint. Need contractor ASAP.",
            "homeowner_name": "John Smith",
            "phone": "(214) 555-1234",
            "email": "john@example.com",
        },
        {
            "title": "Leaky faucet repair and plumbing inspection",
            "category": "plumbing",
            "location": "Arlington, TX",
            "budget": 300,
            "description": "Kitchen faucet leaking, need plumber to inspect and fix. Available this weekend.",
            "homeowner_name": "Sarah Johnson",
            "phone": "(817) 555-5678",
            "email": "sarah@example.com",
        },
        {
            "title": "House painting - interior walls",
            "category": "painting",
            "location": "Dallas, TX",
            "budget": 1500,
            "description": "Interior painting for 3 bedrooms and living room. Light gray color.",
            "homeowner_name": "Mike Davis",
            "phone": "(214) 555-9999",
            "email": "mike@example.com",
        },
        {
            "title": "Kitchen remodel with new cabinets",
            "category": "kitchen",
            "location": "Houston, TX",
            "budget": 12000,
            "description": "Full kitchen remodel. New cabinets, countertop, flooring. 6-week timeline.",
            "homeowner_name": "Lisa Anderson",
            "phone": "(713) 555-2222",
            "email": "lisa@example.com",
        },
        {
            "title": "Electrical outlet installation",
            "category": "electrical",
            "location": "Arlington, TX",
            "budget": 400,
            "description": "Need 4 new outlets installed in garage. Licensed electrician preferred.",
            "homeowner_name": "Tom Wilson",
            "phone": "(817) 555-3333",
            "email": "tom@example.com",
        },
        {
            "title": "Roof repair - water damage",
            "category": "roofing",
            "location": "Austin, TX",
            "budget": 3000,
            "description": "Storm damage to roof. Need assessment and repair quote. Damage visible from inside.",
            "homeowner_name": "Emma Brown",
            "phone": "(512) 555-4444",
            "email": "emma@example.com",
        },
    ]

    added = 0
    for job in sample_jobs:
        result = engine.add_job_directly(job)
        if result.get("success"):
            added += 1
            print(f"✓ {job['title']}")
            print(f"  Location: {job['location']} | Budget: ${job['budget']}\n")

    print(f"✓ Added {added} jobs\n")

    # ========================================================================
    # STEP 2: GET ALL ACTIVE JOBS
    # ========================================================================
    print("STEP 2: RETRIEVE ALL ACTIVE JOBS")
    print("-" * 70)

    active_jobs = engine.get_active_jobs()
    print(f"✓ {len(active_jobs)} active jobs available\n")

    # ========================================================================
    # STEP 3: FILTER BY CATEGORY
    # ========================================================================
    print("STEP 3: FILTER JOBS BY CATEGORY")
    print("-" * 70)

    # Show jobs by category
    by_category = engine.get_jobs_by_category()
    print("Jobs available by category:\n")
    for category, count in sorted(by_category.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {category:<20} {count:>3} jobs")
    print()

    # ========================================================================
    # STEP 4: FILTER BY LOCATION
    # ========================================================================
    print("STEP 4: FILTER JOBS BY LOCATION")
    print("-" * 70)

    by_location = engine.get_jobs_by_location()
    print("Jobs available by location:\n")
    for location, count in sorted(by_location.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {location:<25} {count:>3} jobs")
    print()

    # ========================================================================
    # STEP 5: CONTRACTOR-SPECIFIC FILTERS
    # ========================================================================
    print("STEP 5: FILTER FOR SPECIFIC CONTRACTOR")
    print("-" * 70)

    # Example: Plumber in Dallas area looking for jobs $200-2000
    plumber_filters = {
        "category": "plumbing",
        "location": "Dallas",
        "min_budget": 200,
        "max_budget": 2000,
    }

    plumber_jobs = engine.get_active_jobs(plumber_filters)
    print(f"Jobs matching plumber in Dallas ($200-$2000):\n")

    for job in plumber_jobs:
        print(f"  • {job['title']}")
        print(f"    Location: {job['location']}")
        print(f"    Budget: ${job['budget']}")
        print(f"    Contact: {job['contact_info'].get('name')} - {job['contact_info'].get('phone')}\n")

    # ========================================================================
    # STEP 6: CONTRACTOR WOULD APPLY/BID
    # ========================================================================
    print("STEP 6: CONTRACTOR APPLIES FOR JOB (Simulated)")
    print("-" * 70)

    if plumber_jobs:
        job_to_bid = plumber_jobs[0]
        print(f"✓ Plumber applies for: {job_to_bid['title']}")
        print(f"  Job ID: {job_to_bid['id']}")
        print(f"  Budget: ${job_to_bid['budget']}")
        print(f"  Contractor Commission: ${job_to_bid['budget'] * 0.85:.2f} (85%)")
        print(f"  Platform Commission: ${job_to_bid['budget'] * 0.15:.2f} (15%)\n")

        # Mark as completed to show commission tracking
        print("  → Contractor completes job")
        engine.mark_job_completed(job_to_bid['id'], "contractor_known_123")
        print(f"  → Status: completed")
        print(f"  → Platform earned: ${job_to_bid['budget'] * 0.15:.2f}\n")

    # ========================================================================
    # STEP 7: STATISTICS DASHBOARD
    # ========================================================================
    print("STEP 7: DASHBOARD STATISTICS")
    print("-" * 70)

    report = engine.generate_scrape_report()

    print(f"Total Jobs in Database: {report['total_jobs']}")
    print(f"Active Jobs: {report['active_jobs']}")
    print(f"Completed Jobs: {report['completed_jobs']}")
    print(f"Expired Jobs: {report['expired_jobs']}\n")

    print(f"Total Budget Available (active jobs): ${report['total_available_budget']:,.2f}")
    print(f"Average Job Value: ${report['average_job_value']:.2f}\n")

    print("Jobs by Source:")
    for source, count in report['jobs_by_source'].items():
        print(f"  • {source:<25} {count:>3} jobs")
    print()

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("="*70)
    print("✅ JOB SCRAPER TEST COMPLETE")
    print("="*70)
    print("\nWhat Just Happened:")
    print("  1. Added 6 sample jobs to the database")
    print("  2. Retrieved all active jobs")
    print("  3. Filtered jobs by category")
    print("  4. Filtered jobs by location")
    print("  5. Showed how contractors filter for their specialty")
    print("  6. Demonstrated contractor applying and commission calculation")
    print("  7. Generated dashboard statistics")

    print("\nNext Steps:")
    print("  1. Configure scrapers for each source (Craigslist, Facebook, Google, etc.)")
    print("  2. Run scrapers to pull real jobs from the internet")
    print("  3. Set up contractor portal to browse jobs")
    print("  4. Enable contractor applications/bidding")
    print("  5. Track job completions and commissions")
    print("  6. Scale to multiple contractors")

    print("\nFiles Created:")
    print("  • data/jobs/all_jobs.json - All jobs database")
    print("  • data/jobs/scrape_log.json - Scraping history")

    print("\n")


if __name__ == "__main__":
    main()
