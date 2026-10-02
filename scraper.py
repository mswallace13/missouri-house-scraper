import re
import time
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

# Base URL and target roster URL
BASE_URL = "https://house.mo.gov/"
ROSTER_URL = "https://house.mo.gov/MemberRoster.aspx?year=2026&code=R"

# Target terms to search for (case-insensitive)
RELIGIOUS_TERMS = [
    r"\bcatholic\b",
    r"\bbaptist\b",
    r"\bmethodist\b",
    r"\bpresbyterian\b",
    r"\blutheran\b",
    r"\bchristian\b",
    r"\bprotestant\b",
    r"\bepiscopal\b",
    r"\bchurch\b",
    r"\bparish\b",
    r"\bcongregation\b",
]

# Set a polite User-Agent header
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def get_member_links(roster_url):
    """Parses the roster page to find links to individual member detail pages."""
    print(f"Fetching roster page: {roster_url}")
    response = requests.get(roster_url, headers=HEADERS)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    member_links = []

    # Look for links containing MemberDetails.aspx
    for a_tag in soup.find_all("a", href=True):
        href = a_tag["href"]
        if "MemberDetails.aspx" in href:
            full_url = urljoin(BASE_URL, href)
            member_name = a_tag.get_text(strip=True)
            if full_url not in [m["url"] for m in member_links]:
                member_links.append({"name": member_name, "url": full_url})

    return member_links


def scan_profile_for_religion(member_url):
    """Fetches an individual member profile and checks for religious terminology."""
    try:
        res = requests.get(member_url, headers=HEADERS, timeout=10)
        res.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching {member_url}: {e}")
        return []

    soup = BeautifulSoup(res.text, "html.parser")

    # Focus on biography or personal information container if present, or fallback to body text
    bio_container = soup.find("div", id=re.compile(r"bio|details|content", re.I))
    page_text = bio_container.get_text() if bio_container else soup.body.get_text()

    # Find matching keywords
    matches = []
    for term in RELIGIOUS_TERMS:
        found = re.findall(term, page_text, re.IGNORECASE)
        if found:
            # Capitalize matched term for clean reporting
            matches.extend([f.capitalize() for f in found])

    # Return unique matched terms
    return list(set(matches))


def main():
    members = get_member_links(ROSTER_URL)
    print(f"Found {len(members)} member links.\n")

    results = []

    for idx, member in enumerate(members, start=1):
        print(
            f"[{idx}/{len(members)}] Checking bio for: {member['name']}..."
        )

        matches = scan_profile_for_religion(member["url"])

        if matches:
            results.append(
                {
                    "name": member["name"],
                    "url": member["url"],
                    "terms": ", ".join(matches),
                }
            )
            print(f"   --> Matched terms: {', '.join(matches)}")

        # Respectful delay between requests to avoid overloading the state server
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print("SUMMARY RESULTS:")
    print("=" * 50)
    for r in results:
        print(f"Name: {r['name']}\n  URL: {r['url']}\n  Matches: {r['terms']}\n")


if __name__ == "__main__":
    main()
