#!/usr/bin/env python3
"""
Quick Test: Job Dispatcher System
Posts a test job, matches contractors, tracks pipeline, and calculates commission
"""

from job_dispatcher import JobDispatcher
from datetime import datetime

def main():
    print("\n" + "="*70)
    print("  JOB DISPATCHER - QUICK TEST")
    print("="*70 + "\n")

    # Initialize dispatcher
    dispatcher = JobDispatcher()
    print("✓ Job Dispatcher initialized")
    print(f"✓ Loaded {len(dispatcher.contractors)} contractors")
    print(f"✓ Existing jobs: {len(dispatcher.jobs)}\n")

    # ========================================================================
    # STEP 1: POST A NEW JOB
    # ========================================================================
    print("STEP 1: POST NEW JOB")
    print("-" * 70)

    new_job = dispatcher.post_new_job({
        "title": "Bathroom Remodel",
        "type": "bathroom",
        "location": "Dallas",
        "budget": 5000,
        "description": "Full bathroom renovation including tile, fixtures, and paint",
        "timeline": "2 weeks",
        "homeowner_name": "Sarah Johnson",
        "homeowner_phone": "(214) 555-9876",
        "homeowner_email": "sarah@example.com",
        "source": "direct_submission",
    })

    print(f"✓ Job posted: {new_job['id']}")
    print(f"  • Type: {new_job['type']}")
    print(f"  • Location: {new_job['location']}")
    print(f"  • Budget: ${new_job['budget']:.2f}")
    print(f"  • Status: {new_job['status']}\n")

    # ========================================================================
    # STEP 2: MATCH TO CONTRACTORS
    # ========================================================================
    print("STEP 2: FIND MATCHING CONTRACTORS")
    print("-" * 70)

    matches = dispatcher.find_matching_contractors(new_job)
    print(f"✓ Found {len(matches)} matching contractors\n")
    print(f"{'Rank':<6} {'Contractor':<35} {'Match %':<10}")
    print("-" * 70)

    for i, (contractor_id, score) in enumerate(matches[:5], 1):
        contractor = dispatcher.contractors[contractor_id]
        name = contractor['name'][:30]
        print(f"{i:<6} {name:<35} {score:>6.1f}%")
    print()

    # ========================================================================
    # STEP 3: DISTRIBUTE JOB
    # ========================================================================
    print("STEP 3: DISTRIBUTE JOB TO CONTRACTORS")
    print("-" * 70)

    distribution = dispatcher.distribute_job_to_contractors(new_job['id'])
    print(f"✓ Job sent to {distribution['contacted']} contractors")
    print(f"  • Using contact methods: {DISTRIBUTION_CONFIG.get('contact_methods')}\n")

    for contact in distribution['contacts'][:3]:
        print(f"  → {contact['contractor_name']}")
        print(f"    Match: {contact['match_score']:.1f}%")
        print(f"    Methods: {', '.join(contact['methods'])}\n")

    # ========================================================================
    # STEP 4: TRACK PIPELINE
    # ========================================================================
    print("STEP 4: TRACK PIPELINE (Contractor responds)")
    print("-" * 70)

    # Simulate contractor accepting
    accepting_contractor_id = matches[0][0]  # Best match
    accepting_contractor = dispatcher.contractors[accepting_contractor_id]

    print(f"✓ Contractor responded: {accepting_contractor['name']}")

    # Update status: sent → contacted
    dispatcher.update_job_status(new_job['id'], "contacted", accepting_contractor_id)
    print(f"  → Status: sent → contacted")

    # Update status: contacted → accepted
    dispatcher.update_job_status(new_job['id'], "accepted", accepting_contractor_id)
    print(f"  → Status: contacted → accepted")

    # Update status: accepted → in_progress
    dispatcher.update_job_status(new_job['id'], "in_progress", accepting_contractor_id)
    print(f"  → Status: accepted → in_progress")

    # Update status: in_progress → completed
    dispatcher.update_job_status(new_job['id'], "completed", accepting_contractor_id)
    print(f"  → Status: in_progress → completed")

    # Update status: completed → paid
    dispatcher.update_job_status(new_job['id'], "paid", accepting_contractor_id)
    print(f"  → Status: completed → paid\n")

    # ========================================================================
    # STEP 5: COMMISSION CALCULATION
    # ========================================================================
    print("STEP 5: COMMISSION CALCULATED")
    print("-" * 70)

    updated_job = dispatcher.jobs[new_job['id']]
    job_value = updated_job['budget']
    your_cut = job_value * 0.15
    their_cut = job_value * 0.85

    print(f"✓ Job completed and paid")
    print(f"  Job Value:           ${job_value:>10.2f}")
    print(f"  Your Commission (15%): ${your_cut:>10.2f}")
    print(f"  Contractor Earnings:  ${their_cut:>10.2f}\n")

    # ========================================================================
    # STEP 6: DASHBOARD REPORT
    # ========================================================================
    print("STEP 6: DASHBOARD OVERVIEW")
    print("-" * 70)

    report = dispatcher.generate_dashboard_report()

    print("Jobs by Status:")
    for status, count in report['jobs_overview'].items():
        print(f"  • {status:<15} {count:>3}")

    print(f"\nPipeline Summary:")
    print(f"  Total Jobs: {report['total_jobs']}")
    print(f"  Active Contractors: {report['active_contractors']}/{report['total_contractors']}")

    print(f"\nConversion Rates:")
    for rate_name, rate_value in report['pipeline_flow'].items():
        print(f"  • {rate_name}: {rate_value}")

    commission_info = report['commissions']
    print(f"\nCommissions Earned:")
    print(f"  Total Jobs Completed: {commission_info['total_jobs_paid']}")
    print(f"  Total Job Value: ${commission_info['total_job_value']:,.2f}")
    print(f"  YOUR TOTAL COMMISSION: ${commission_info['your_total_commission']:,.2f}")
    print(f"  Contractor Earnings: ${commission_info['contractor_total_earnings']:,.2f}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "="*70)
    print("✅ JOB DISPATCHER TEST COMPLETE")
    print("="*70)
    print("\nSummary:")
    print(f"  ✓ Job posted and distributed")
    print(f"  ✓ Matched to top contractors")
    print(f"  ✓ Contractor accepted work")
    print(f"  ✓ Job completed and paid")
    print(f"  ✓ Commission calculated: ${your_cut:.2f}")
    print(f"  ✓ Data saved to data/ directory")

    print("\nNext Steps:")
    print("  1. Open the dashboard: punchlist-lead-desk.html")
    print("  2. View jobs by status")
    print("  3. Track commissions per contractor")
    print("  4. Generate daily/weekly reports")

    print("\nFiles Created:")
    print("  • data/jobs.json - All jobs")
    print("  • data/pipeline_log.json - Pipeline movements")
    print("  • data/commissions.json - Commission records")
    print("\n")


if __name__ == "__main__":
    # Need to import config
    from job_dispatcher_config import DISTRIBUTION_CONFIG
    main()
