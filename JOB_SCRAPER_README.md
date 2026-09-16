# Job Scraper Platform for Contractors & Handymen

**Find home improvement jobs from across the internet and connect contractors with opportunities.**

---

## 🎯 What This Does

Your personal **job aggregator** that:

1. **Scrapes jobs** from Craigslist, Facebook Marketplace, Google, Reddit, Nextdoor, and more
2. **Consolidates opportunities** into one database
3. **Eliminates duplicates** across all sources
4. **Contractors browse** and apply for jobs
5. **You earn commission** (15%) on completed jobs

```
JOBS FROM:
├─ Craigslist (services section)
├─ Facebook Marketplace (services)
├─ Google Maps (homeowner reviews)
├─ Google Local Services
├─ Indeed (gig work)
├─ Nextdoor (neighborhood posts)
├─ Reddit (r/forhire, local subreddits)
├─ Direct submissions (homeowners)
└─ Other sources
        ↓
   Job Scraper Engine
   (Deduplication, consolidation)
        ↓
   Live Job Board
        ↓
   Contractors Browse & Apply
        ↓
   Job Completed
        ↓
   YOU EARN 15% COMMISSION
```

---

## 💼 Business Model

**You're the marketplace operator taking a commission:**

```
Job posted ($1,000)
        ↓
Contractor applies and completes
        ↓
YOU GET: $150 (15%)
Contractor GETS: $850 (85%)
```

**With 20 jobs/month average $2,000:**
```
20 × $2,000 = $40,000 total job value
Your 15% = $6,000/month profit
```

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────┐
│  JOB SOURCES (Multiple Platforms)           │
├─────────────────────────────────────────────┤
│ • Craigslist Scraper (Browser + API)        │
│ • Facebook Marketplace (Selenium)           │
│ • Google Maps (API or scraping)             │
│ • Reddit (PRAW library)                     │
│ • Nextdoor (Scraping)                       │
│ • Indeed (Job board scraping)               │
│ • Direct form submissions                   │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  JOB SCRAPER ENGINE                         │
├─────────────────────────────────────────────┤
│ 1. Scrape jobs from all sources            │
│ 2. Validate job quality                     │
│ 3. Detect job category                      │
│ 4. Find & remove duplicates                │
│ 5. Consolidate into database               │
│ 6. Make searchable/filterable              │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  JOB DATABASE                               │
├─────────────────────────────────────────────┤
│ • data/jobs/all_jobs.json (all jobs)       │
│ • data/jobs/scrape_log.json (history)      │
│ • Indexed by: category, location, source   │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  CONTRACTOR JOB BOARD                       │
├─────────────────────────────────────────────┤
│ • Browse by category/location              │
│ • Filter by budget range                   │
│ • Apply/bid on jobs                        │
│ • Track applications                       │
└────────────┬────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────┐
│  COMMISSION TRACKING                        │
├─────────────────────────────────────────────┤
│ • Job completed by contractor              │
│ • Auto-calculate your 15% cut              │
│ • Contractor gets 85%                      │
│ • Track total earnings                     │
└─────────────────────────────────────────────┘
```

---

## 📁 Configuration Files

### job_scraper_config.py (Main Configuration)

```python
JOB_SOURCES = {
    "craigslist": {...},           # Dallas, Houston, Austin
    "facebook_marketplace": {...}, # Facebook services
    "google_maps": {...},          # Google Maps jobs
    "reddit": {...},               # r/forhire, local subreddits
    "nextdoor": {...},             # Neighborhood jobs
    # ... and more
}

JOB_CATEGORIES = {
    "handyman": {...},
    "plumbing": {...},
    "electrical": {...},
    "painting": {...},
    "roofing": {...},
    "kitchen": {...},
    "bathroom": {...},
    "flooring": {...},
    "hvac": {...},
    "drywall": {...},
    # ... 12 total categories
}

SERVICE_AREAS = [
    "Dallas", "Arlington", "Irving", "Fort Worth",
    "Houston", "Austin", "San Antonio"
]
```

---

## 🚀 Quick Start (5 minutes)

### 1. Test the System

```bash
cd /home/user/lead-pipeline

# Run the test
python test_job_scraper.py
```

**What happens:**
- ✓ Creates 6 sample jobs (bathroom, plumbing, painting, kitchen, electrical, roofing)
- ✓ Shows all active jobs
- ✓ Filters by category (plumbing)
- ✓ Filters by location (Dallas)
- ✓ Filters by budget range
- ✓ Simulates contractor applying for job
- ✓ Calculates your commission (15%)
- ✓ Generates dashboard stats

**Expected output:**
```
✓ Job Scraper Engine initialized
✓ Added 6 jobs
✓ 6 active jobs available

Jobs available by category:
  • bathroom          1 jobs
  • plumbing          1 jobs
  • painting          1 jobs
  • kitchen           1 jobs
  • electrical        1 jobs
  • roofing           1 jobs

Jobs available by location:
  • Dallas, TX        3 jobs
  • Arlington, TX     2 jobs
  • Houston, TX       1 job

Jobs matching plumber in Dallas ($200-$2000):
  • Leaky faucet repair and plumbing inspection
    Location: Arlington, TX
    Budget: $300
    Contact: Sarah Johnson - (817) 555-5678

✓ Plumber applies for: Leaky faucet repair
  Budget: $300
  Contractor Commission: $255.00 (85%)
  Platform Commission: $45.00 (15%)
  → Status: completed

✅ TEST COMPLETE
```

---

## 📊 How It Works: Step by Step

### Step 1: Scrape Jobs from Internet

```python
from job_scraper_engine import JobScraperEngine

engine = JobScraperEngine()

# Scrape from Craigslist
result = engine.scrape_craigslist()
print(f"Found {result['scraped']} jobs")

# Scrape from Facebook
result = engine.scrape_facebook_marketplace()

# Scrape from Google Maps
result = engine.scrape_google_maps()

# Scrape from Reddit
result = engine.scrape_reddit()
```

### Step 2: Add Jobs Directly (Homeowner Submission)

```python
# Homeowner fills out form and submits job
job = engine.add_job_directly({
    "title": "Bathroom remodel needed",
    "category": "bathroom",
    "location": "Dallas, TX",
    "budget": 5000,
    "description": "Full bathroom renovation...",
    "homeowner_name": "John Smith",
    "phone": "(214) 555-1234",
    "email": "john@example.com",
})

# Result: Job added to database, deduplication checked
```

### Step 3: Contractor Browses & Filters

```python
# Plumber looking for jobs
plumber_filters = {
    "category": "plumbing",
    "location": "Dallas",
    "min_budget": 200,
    "max_budget": 2000,
}

jobs = engine.get_active_jobs(plumber_filters)
# Returns: [job1, job2, job3] matching criteria
```

### Step 4: Contractor Applies

```python
# Contractor applies for job
# System records: contractor_id, job_id, bid_amount

# Contractor selected and completes work
engine.mark_job_completed(job_id, contractor_id)

# Commission automatically calculated:
#   Job value: $1,000
#   You get: $150 (15%)
#   Contractor gets: $850 (85%)
```

### Step 5: Payment & Commission

```python
# Get commission report
report = engine.generate_scrape_report()
report['total_available_budget']  # $50,000 in active jobs
report['completed_jobs']           # 5 jobs done
report['jobs_by_category']         # {"plumbing": 2, "electrical": 3}
report['jobs_by_location']         # {"Dallas": 7, "Houston": 3}
```

---

## 🔍 Job Deduplication

Smart deduplication removes duplicates across all sources:

```python
# Checks for duplicates using:
DEDUPLICATION_RULES = {
    "exact_title_match": True,      # Same title = duplicate
    "similarity_threshold": 0.85,   # 85% similar = duplicate
    "location_radius_miles": 5,     # Same location ±5 miles
    "budget_variance_percent": 10,  # Budget within 10%
    "date_window_days": 2,          # Posted within 2 days
}

# Example:
# Job A (Craigslist): "Bathroom remodel $5000 Dallas"
# Job B (Facebook): "Bath remodel $4900 Dallas" → DUPLICATE FOUND
# Result: Only Job A kept, Job B discarded
```

---

## 🎯 Job Categories & Matching

### Auto-Categorization

System automatically detects job type from title/description:

```python
# Title: "Leaky faucet repair and pipe inspection"
# Auto-detected as: "plumbing"

# Title: "Interior painting 3 bedrooms"
# Auto-detected as: "painting"

# Title: "Full bathroom renovation"
# Auto-detected as: "bathroom"
```

### Contractor Matching

Contractors can filter by:
- **Category** (their specialty)
- **Location** (where they work)
- **Budget** (job size they prefer)
- **Days posted** (fresh jobs only)

---

## 📈 Revenue Examples

### Month 1: Start Building

```
10 jobs scraped/week = 40 jobs/month
Average job value: $2,000
Total job value: $80,000

Your commission (15%): $12,000/month ✓
Contractor earnings (85%): $68,000/month
```

### Month 2: Scaling

```
20 jobs scraped/week = 80 jobs/month
Average job value: $2,500
Total job value: $200,000

Your commission (15%): $30,000/month ✓
Contractor earnings (85%): $170,000/month
```

### Month 3: Full Scale

```
30+ jobs scraped/week = 150+ jobs/month
Average job value: $2,500
Total job value: $375,000+

Your commission (15%): $56,000+/month ✓
Contractor earnings (85%): $319,000+/month
```

---

## 🔧 Scraper Setup

### Craigslist (Easiest - HTML Scraping)

```bash
pip install requests beautifulsoup4
```

No API key needed. Just scrapes public listings.

### Facebook Marketplace

```bash
pip install selenium
# Requires: Chromedriver or geckodriver
```

Uses Selenium to access dynamic content.

### Google Maps

```bash
# Option 1: Official API (requires API key)
pip install googlemaps

# Option 2: Web scraping
pip install selenium
```

### Reddit (PRAW Library)

```bash
pip install praw

# Create Reddit app at: https://www.reddit.com/prefs/apps
# Get: client_id, client_secret
```

### Nextdoor

```bash
pip install selenium
# Note: Nextdoor is tricky, requires login
```

---

## 💾 Data Storage

### data/jobs/all_jobs.json
Stores all jobs with full details:

```json
{
  "direct_20260916_150000": {
    "id": "direct_20260916_150000",
    "title": "Bathroom remodel",
    "category": "bathroom",
    "location": "Dallas, TX",
    "budget": 5000,
    "description": "Full bathroom renovation...",
    "posted_date": "2026-09-16T15:00:00",
    "source": "direct_submission",
    "status": "active",
    "contact_info": {
      "name": "John Smith",
      "phone": "(214) 555-1234",
      "email": "john@example.com"
    }
  }
}
```

### data/jobs/scrape_log.json
Track what was scraped when:

```json
[
  {
    "source": "craigslist",
    "scraped": 45,
    "errors": [],
    "timestamp": "2026-09-16T09:00:00"
  }
]
```

---

## 🎯 Contractor Testing

You have a handyman you know personally. Here's how to test:

1. **Add sample job** he might do:
```python
engine.add_job_directly({
    "title": "Kitchen cabinet repair",
    "category": "handyman",
    "location": "Dallas",
    "budget": 600,
    "description": "Cabinet hinges broken, need repair",
    "homeowner_name": "Test Customer",
    "phone": "(214) 555-0000",
    "email": "test@example.com",
})
```

2. **He browses jobs**:
```python
his_jobs = engine.get_active_jobs({
    "category": "handyman",
    "location": "Dallas",
    "min_budget": 300,
    "max_budget": 5000,
})
```

3. **He applies/completes**:
```python
engine.mark_job_completed(job_id, "his_contractor_id")
# You instantly earn 15% commission
```

4. **Test with real scraped jobs** once scrapers are live

---

## ✅ Setup Checklist

- [ ] Python 3.7+ installed
- [ ] Required libraries installed:
  - [ ] `pip install requests beautifulsoup4` (Craigslist)
  - [ ] `pip install selenium` (Facebook, Google)
  - [ ] `pip install praw` (Reddit)
- [ ] Run `python test_job_scraper.py` to verify
- [ ] Test adding a job directly
- [ ] Test filtering jobs
- [ ] Configure each scraper source
- [ ] Run scrapers for first time
- [ ] Monitor job database growth
- [ ] Invite contractors to browse

---

## 🚀 Next Steps

1. **Immediate (Today)**
   - ✓ Run test script
   - ✓ Understand the flow
   - ✓ Add sample jobs

2. **This Week**
   - Configure Craigslist scraper
   - Configure Facebook scraper
   - Set up scraping schedule

3. **Next Week**
   - Start scraping real jobs
   - Invite your handyman to test
   - Create contractor job board UI
   - Set up application system

4. **Week 3-4**
   - Add more scrapers (Google, Reddit)
   - Invite more contractors
   - Track first commissions
   - Optimize filters

5. **Month 2**
   - Scale to multiple contractors
   - Expand service areas
   - Automate daily scraping
   - Build payment system

---

## 📊 Expected Growth

```
Week 1:    10 jobs/day     → 70/week
Week 2:    20 jobs/day     → 140/week  
Week 3:    30 jobs/day     → 210/week
Week 4:    50 jobs/day     → 350/week

Month 2:   100 jobs/day    → 700/week   (5,000/month)
Month 3:   150 jobs/day    → 1,050/week (7,500/month)

At 1,500 jobs/month × $2,000 avg:
Your 15% commission = $450,000/month 💰
```

---

## 🎯 Key Files

- **job_scraper_config.py** - All configuration
- **job_scraper_engine.py** - Core scraping & management engine
- **test_job_scraper.py** - Quick test script
- **data/jobs/all_jobs.json** - Job database
- **data/jobs/scrape_log.json** - Scraping history

---

**Status:** ✅ Complete & Ready to Test  
**Created:** 2026-09-16  
**Business Model:** 15% commission on all completed jobs  
**First Test:** With your personal handyman contact

🚀 **Ready to find every home improvement job on the internet!**

