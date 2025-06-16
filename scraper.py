import requests
from bs4 import BeautifulSoup

# Simplified enrichment scraper aligned to QC Engage protocol
def run_scraper(company_name, website):
    try:
        findings = []

        # --- CAREERS PAGE (multi-path fallback) ---
        career_paths = ["/careers", "/jobs", "/work-with-us", "/join-us", "/open-roles"]
        careers_checked = False

        for path in career_paths:
            try:
                url = website.rstrip('/') + path
                resp = requests.get(url, timeout=6, allow_redirects=True)

                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    text = soup.get_text().lower()
                    careers_checked = True

                    if any(term in text for term in ["workday", "adp", "ukg", "paychex"]):
                        findings.append(f"HCM vendor mentioned at {url}")

                    if any(term in text for term in ["payroll", "hr", "human capital", "scheduling"]):
                        findings.append(f"HR/payroll terms found at {url}")

                    if "hcm" in text or "applicant tracking" in text:
                        findings.append(f"HCM/ATS signal found at {url}")
                    break
            except Exception as e:
                continue

        if not careers_checked:
            findings.append("No accessible careers/jobs page found.")

        # --- JOB BOARD ---
        try:
            job_boards = ["/jobs", "/work-with-us", "/join-us", "/open-roles"]
            for path in job_boards:
                resp = requests.get(website.rstrip('/') + path, timeout=5)
                if resp.status_code == 200 and any(v in resp.text.lower() for v in ["lever.co", "greenhouse.io"]):
                    findings.append("Job board detected with embedded ATS platform")
                    break
        except Exception as e:
            findings.append(f"Job board check failed: {str(e)}")

        # --- Stubs / Hand-offs ---
        findings.append("LinkedIn validation required for HRIS roles – offloaded to Quota Crusher Persona")
        findings.append("10-K filings must be reviewed – handled via external compliance function")
        findings.append("Third-party validation (ZoomInfo/Surfe/HG Insights) required for system confirmation")

        return "\n".join(findings)

    except Exception as e:
        return f"Error during scraping: {str(e)}"
