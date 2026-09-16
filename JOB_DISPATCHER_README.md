# Job Dispatcher - Contractor Job Matching & Commission Platform

**A system that finds jobs for contractors and takes a commission on completed work.**

---

## 🎯 What This Does

Instead of finding leads FOR handymen, this system:

1. **Collects Jobs** → From homeowners, Google Maps, Craigslist, Facebook, etc.
2. **Matches Jobs to Contractors** → Uses smart algorithm (specialty, location, availability, size)
3. **Distributes to Contractors** → Sends job offers via text/email/call
4. **Tracks Pipeline** → Monitors: sent → contacted → accepted → completed → paid
5. **Calculates Commission** → You take 15%, contractors get 85%
6. **Tracks Earnings** → Shows contractor earnings and your revenue

---

## 💼 Business Model

**You are the middleman/broker:**

```
Homeowner posts job ($5,000)
        ↓
You match to best contractor
        ↓
Contractor does work
        ↓
Job paid ($5,000)
        ↓
YOU GET: $750 (15%)
Contractor GETS: $4,250 (85%)
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────┐
│  JOB SOURCES                        │
├─────────────────────────────────────┤
│ • Google Maps                       │
│ • Craigslist                        │
│ • Facebook Marketplace              │
│ • Direct homeowner submissions      │
│ • Referrals                         │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  JOB DISPATCHER (Core Engine)       │
├─────────────────────────────────────┤
│ 1. Post new job                     │
│ 2. Match to contractors (algorithm) │
│ 3. Distribute to best matches       │
│ 4. Track pipeline status            │
│ 5. Calculate commissions            │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  CONTRACTOR DATABASE                │
├─────────────────────────────────────┤
│ • Specialties (plumbing, electrical)│
│ • Service areas (Dallas, Houston)   │
│ • Job size preferences (small/med)  │
│ • Availability & capacity           │
│ • Ratings & earnings                │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  DATA STORAGE                       │
├─────────────────────────────────────┤
│ • data/jobs.json                    │
│ • data/pipeline_log.json            │
│ • data/commissions.json             │
└─────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  DASHBOARD                          │
├─────────────────────────────────────┤
│ • Jobs by status                    │
│ • Pipeline flow                     │
│ • Commission tracking               │
│ • Contractor performance            │
└─────────────────────────────────────┘
```

---

## 📁 Configuration Files

### job_dispatcher_config.py (Main Configuration)

**1. Contractor Database**
```python
CONTRACTOR_DATABASE = {
    "contractor_1": {
        "name": "ABC Handyman",
        "specialties": ["handyman", "painting"],
        "service_areas": ["Dallas", "Arlington"],
        "availability": "available",
        "job_size": ["small", "medium", "large"],
        "max_jobs_active": 5,
        "currently_active": 2,
        "rating": 4.8,
        "total_earnings": 12500,  # Lifetime earnings
        "platform_earnings": 1875,  # Your commission (15%)
    }
}
```

**2. Job Types**
```python
JOB_TYPES = {
    "bathroom": {
        "name": "Bathroom Remodeling",
        "specialties_needed": ["remodeling", "bathroom"],
        "avg_job_size": "medium",
        "avg_budget_min": 3000,
        "avg_budget_max": 12000,
    },
    # ... 9 more job types
}
```

**3. Matching Algorithm Weights**
```python
MATCHING_WEIGHTS = {
    "specialty_match": 0.40,    # Most important (40%)
    "location_match": 0.25,     # (25%)
    "availability": 0.20,       # (20%)
    "job_size_fit": 0.10,       # (10%)
    "rating_bonus": 0.05,       # (5%)
}
```

**4. Commission Settings**
```python
COMMISSION_CONFIG = {
    "platform_cut": 0.15,      # You take 15%
    "contractor_cut": 0.85,    # They get 85%
}
```

---

## 🚀 Quick Start

### Test the System (5 minutes)

```bash
cd /home/user/lead-pipeline

# Run the test
python test_job_dispatcher.py
```

**What happens:**
1. Creates a test job (Bathroom Remodel, $5,000)
2. Finds matching contractors
3. Distributes to top 5
4. Simulates pipeline: sent → accepted → completed → paid
5. Calculates commission: you get $750
6. Shows dashboard report

**Expected output:**
```
✓ Job Dispatcher initialized
✓ Loaded 2 contractors
✓ Job posted: job_20260916_150000
✓ Found 2 matching contractors
✓ Job sent to 2 contractors
✓ Contractor responded
→ Status: sent → contacted → accepted → in_progress → completed → paid
✓ Commission calculated
  Job Value: $5,000.00
  Your Commission (15%): $750.00
  Contractor Earnings: $4,250.00
✅ TEST COMPLETE
```

---

## 📋 How It Works: Step by Step

### 1. POST A JOB

```python
from job_dispatcher import JobDispatcher

dispatcher = JobDispatcher()

new_job = dispatcher.post_new_job({
    "title": "Bathroom Remodel",
    "type": "bathroom",
    "location": "Dallas",
    "budget": 5000,
    "homeowner_name": "John Smith",
    "homeowner_phone": "(214) 555-1234",
    "homeowner_email": "john@example.com",
})
```

**Job details stored:**
- Job type & location
- Budget & timeline
- Homeowner contact info
- Source (Google, Craigslist, direct, etc.)
- Status tracking from new → paid

### 2. MATCH CONTRACTORS

The matching algorithm scores each contractor 0-100:

```
Specialty Match (40%): Do they do this type of work?
  ✓ Bathroom = "remodeling" specialty → HIGH SCORE
  ✗ Plumbing = no remodeling → LOW SCORE

Location Match (25%): Do they service this area?
  ✓ Dallas in service_areas → +25%
  ✗ Houston not in service_areas → +0%

Availability (20%): Do they have capacity?
  ✓ 2 active of 5 max → 60% available → +12%
  ✗ 5 active of 5 max → full → +0%

Job Size (10%): Do they take this size?
  ✓ Medium job in job_size list → +10%
  ✗ Large only, not small → +0%

Rating Bonus (5%): Are they highly rated?
  ✓ 4.8 rating → +5%
  ✗ 3.2 rating → +1%

Total Score: 0-100%
```

### 3. DISTRIBUTE JOB

Send to top 5 matches:

```python
distribution = dispatcher.distribute_job_to_contractors(job_id)

# Results in:
# → Text message to contractors
# → Email with job details
# → Optional: Call contractor if no response
```

**Notification includes:**
- Job type and location
- Budget range
- Timeline
- Match score (why this job is good for them)
- Your commission (15%) vs their cut (85%)

### 4. TRACK PIPELINE

As contractor responds, update status:

```python
# Contractor responds to offer
dispatcher.update_job_status(job_id, "contacted", contractor_id)

# Contractor accepts job
dispatcher.update_job_status(job_id, "accepted", contractor_id)

# Work starts
dispatcher.update_job_status(job_id, "in_progress", contractor_id)

# Work finished
dispatcher.update_job_status(job_id, "completed", contractor_id)

# Payment processed
dispatcher.update_job_status(job_id, "paid", contractor_id)
```

**Pipeline stages:**
```
new → sent → contacted → accepted → in_progress → completed → paid
```

### 5. COMMISSION CALCULATION

When job is marked as "paid":

```
Job Value: $5,000
Your Commission (15%): $750 ← YOU EARN THIS
Contractor (85%): $4,250 ← THEY EARN THIS
```

**Recorded in:**
- data/commissions.json
- Contractor's total_earnings
- Contractor's platform_earnings (your commission)

---

## 🎯 Configuration Options

### Change Contractor Availability

```python
CONTRACTOR_DATABASE["contractor_1"]["availability"] = "available"  # or "booked", "on_break"
CONTRACTOR_DATABASE["contractor_1"]["currently_active"] = 2  # Out of max_jobs_active
```

### Adjust Matching Weights

Emphasize specialization over location:

```python
MATCHING_WEIGHTS = {
    "specialty_match": 0.50,    # Increase from 0.40
    "location_match": 0.15,     # Decrease from 0.25
    "availability": 0.20,
    "job_size_fit": 0.10,
    "rating_bonus": 0.05,
}
```

### Change Commission Rate

```python
COMMISSION_CONFIG = {
    "platform_cut": 0.20,    # Take 20% instead of 15%
    "contractor_cut": 0.80,  # They get 80%
}
```

### Add Service Areas

```python
SERVICE_AREAS = [
    "Dallas",
    "Arlington",
    "Irving",
    "Fort Worth",
    "Houston",  # NEW
    "Austin",   # NEW
]
```

---

## 📊 Dashboard Metrics

### Jobs Overview

```
Status        Count
─────────────────────
new            5      (Posted, not sent)
sent          12      (Sent to contractors)
contacted      8      (Contractors responded)
accepted       6      (Contractors accepted)
in_progress    4      (Currently being worked)
completed      3      (Finished)
paid           2      (Payment processed, YOU EARNED COMMISSION)
cancelled      1      (Cancelled)
```

### Pipeline Conversion Rates

```
sent → completed: 25%    (Of jobs sent, 25% get completed)
completed → paid: 100%   (All completions result in payment)
sent → accepted: 50%     (Half of jobs get accepted)
```

### Commission Report

```
Total Jobs Completed: 2
Total Job Value: $10,750
YOUR TOTAL COMMISSION: $1,612.50
Contractor Total Earnings: $9,137.50

By Contractor:
  ABC Handyman
    • Jobs: 1
    • Value: $5,000
    • Your Cut: $750
    • Their Cut: $4,250

  Dallas Plumbing
    • Jobs: 1
    • Value: $5,750
    • Your Cut: $862.50
    • Their Cut: $4,887.50
```

---

## 🔄 Real-World Workflow

### Day 1: Jobs Come In

```
Morning:
  1. Homeowner submits: "Need bathroom remodel, $5k, Dallas"
  2. Job posted to system (job_001)
  3. Algorithm finds matches
  4. Job sent to 5 contractors

Afternoon:
  - Contractor ABC Handyman responds: "I can do this!"
  - Status: contacted
  - Update: "Great! Here's the contract"
```

### Day 2-7: Work Happens

```
Day 2: Contractor accepts (status: accepted)
Day 3-6: Contractor works (status: in_progress)
Day 7: Contractor finished (status: completed)
  - YOU: "Great work! How much do I owe?"
  - Contract value: $5,000
```

### Day 8: Get Paid

```
Homeowner pays: $5,000
System calculates:
  • Your commission (15%): $750 ✓ YOUR PROFIT
  • Contractor (85%): $4,250 (pay them)

Status: paid
Commission recorded in data/commissions.json
```

---

## 📈 Expected Monthly Revenue

### Example with 10 Jobs/Month

```
Month 1: 10 jobs average $3,000 each
  Total value: $30,000
  Your commission (15%): $4,500
  Contractor earnings: $25,500

Month 2: 20 jobs (scaling up)
  Total value: $60,000
  Your commission (15%): $9,000
  Contractor earnings: $51,000

Month 3: 30+ jobs
  Total value: $100,000
  Your commission (15%): $15,000
  Contractor earnings: $85,000
```

---

## 🔧 Customization Guide

### Add a New Contractor

In `job_dispatcher_config.py`:

```python
CONTRACTOR_DATABASE["contractor_3"] = {
    "name": "Elite Electrical",
    "phone": "(214) 555-0103",
    "email": "info@eliteelectrical.com",
    "specialties": ["electrical", "general_repair"],
    "service_areas": ["Dallas", "Arlington", "Irving", "Fort Worth"],
    "availability": "available",
    "job_size": ["small", "medium"],
    "max_jobs_active": 4,
    "currently_active": 1,
    "rating": 4.9,
    "reviews": 156,
    "total_earnings": 0,
    "platform_earnings": 0,
    "commission_rate": 0.15,
}
```

### Add a New Job Type

In `job_dispatcher_config.py`:

```python
JOB_TYPES["landscaping"] = {
    "name": "Landscaping Services",
    "specialties_needed": ["landscaping", "outdoor"],
    "avg_job_size": "medium",
    "avg_budget_min": 1500,
    "avg_budget_max": 6000,
}
```

### Add a New Service Area

In `job_dispatcher_config.py`:

```python
SERVICE_AREAS.append("Garland")
SERVICE_AREAS.append("Mesquite")
```

---

## 📁 Data Files

### data/jobs.json

Stores all jobs with full details:

```json
{
  "job_20260916_150000": {
    "id": "job_20260916_150000",
    "title": "Bathroom Remodel",
    "type": "bathroom",
    "location": "Dallas",
    "budget": 5000,
    "status": "paid",
    "accepted_by": "contractor_1",
    "sent_to": [...],
    "completed_at": "2026-09-17T14:30:00",
    "paid_at": "2026-09-18T10:00:00"
  }
}
```

### data/pipeline_log.json

Tracks every status change:

```json
[
  {
    "job_id": "job_001",
    "stage": "sent",
    "contractor_id": "contractor_1",
    "timestamp": "2026-09-16T09:00:00",
    "job_value": 5000
  },
  {
    "job_id": "job_001",
    "stage": "accepted",
    "contractor_id": "contractor_1",
    "timestamp": "2026-09-16T10:15:00",
    "job_value": 5000
  }
]
```

### data/commissions.json

Stores commission records:

```json
[
  {
    "job_id": "job_001",
    "contractor_id": "contractor_1",
    "job_value": 5000,
    "your_commission": 750,
    "contractor_earnings": 4250,
    "commission_rate": 0.15,
    "date": "2026-09-18T10:00:00"
  }
]
```

---

## ✅ Quick Commands

### Test the system
```bash
python test_job_dispatcher.py
```

### Post a job
```python
from job_dispatcher import JobDispatcher
dispatcher = JobDispatcher()
job = dispatcher.post_new_job({...})
```

### Get matching contractors
```python
matches = dispatcher.find_matching_contractors(job)
```

### Distribute job
```python
dispatcher.distribute_job_to_contractors(job_id)
```

### Update status
```python
dispatcher.update_job_status(job_id, "accepted", contractor_id)
```

### Get commission report
```python
report = dispatcher.get_commission_report()
```

### Get dashboard
```python
dashboard = dispatcher.generate_dashboard_report()
```

---

## 🎯 Next Steps

1. ✅ Run `python test_job_dispatcher.py` to test the system
2. ✅ Review contractor database in `job_dispatcher_config.py`
3. ✅ Customize matching weights if needed
4. ✅ Set up job sources (Google Maps scraper, Craigslist scraper, etc.)
5. ✅ Build integration to post jobs to the system
6. ✅ Create contractor notification system (SMS/email)
7. ✅ Deploy dashboard for real-time tracking
8. ✅ Start getting jobs and matching contractors
9. ✅ Track commissions and pay contractors

---

**Status:** ✅ Complete & Ready to Test  
**Created:** 2026-09-16  
**Version:** 1.0

