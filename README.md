Missouri House Legislative Bio Scraper

A lightweight, ethical Python web scraper designed to extract biographical details and search for specific religious affiliations, civic backgrounds, and key terms across official profile pages of the Missouri House of Representatives.

Overview

Official legislative roster pages often present high-level details (such as district numbers and political party), while member-specific details like church involvement, educational background, or civic memberships are nested within individual biography pages.

This script:

Crawls the main Missouri House Roster index page (https://house.mo.gov/MemberRoster.aspx).

Collects links to each individual legislator's detail page (MemberDetails.aspx).

Parses individual bios using regular expressions (re) to locate targeted keywords (e.g., Catholic, Baptist, Methodist, Church, Parish).

Outputs structured summary results highlighting matching terms for each representative.

Features

Robust Parsing: Uses BeautifulSoup 4 to parse HTML structure cleanly.

Regex Keyword Matching: Incorporates regex word boundaries (\b) to prevent false positive matches.

Polite Scraping: Implements request throttling (time.sleep) and custom user-agent headers to adhere to web scraping best practices and avoid server strain.

Configurable Search Terms: Easily customize the list of keywords to search for alternative demographic, occupational, or civic criteria.

Prerequisites

Python 3.8+

pip package manager

Installation

Clone the repository:

git clone https://github.com/YOUR-USERNAME/missouri-house-scraper.git
cd missouri-house-scraper


(Optional) Create a virtual environment:

python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate


Install required dependencies:

pip install requests bs4


Usage

Run the main script directly from your terminal:

python scraper.py


Output Example

Fetching roster page: https://house.mo.gov/MemberRoster.aspx?year=2026&code=R
Found 163 member links.

[1/163] Checking bio for: Representative Name...
   --> Matched terms: Baptist, Church
[2/163] Checking bio for: Representative Name...
   --> Matched terms: Catholic, Parish

==================================================
SUMMARY RESULTS:
==================================================
Name: Representative Name
  URL: https://house.mo.gov/MemberDetails.aspx?year=2026&code=R&district=...
  Matches: Baptist, Church


Configuration & Customization

To modify the keywords being searched, open scraper.py and update the RELIGIOUS_TERMS list:

RELIGIOUS_TERMS = [
    r"\bcatholic\b",
    r"\bbaptist\b",
    r"\bmethodist\b",
    r"\bpresbyterian\b",
    r"\blutheran\b",
    # Add custom terms here
]


Ethics & Disclaimer

This project is intended for educational and open-data research purposes only.

Please respect the target website's terms of service and robots.txt directives.

Always keep the delay (time.sleep) enabled to prevent sending excessive requests to government servers.

License

This project is open-source and available under the MIT License.
