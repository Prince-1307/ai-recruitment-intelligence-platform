import undetected_chromedriver as uc

from bs4 import BeautifulSoup

import pandas as pd

import time
import random


# -----------------------------------
# CHROME OPTIONS
# -----------------------------------

options = uc.ChromeOptions()

options.add_argument(
    r"--user-data-dir=C:/selenium_profile"
)

options.add_argument(
    "--disable-blink-features=AutomationControlled"
)

# -----------------------------------
# DRIVER
# -----------------------------------

driver = uc.Chrome(
    version_main=147,
    options=options
)

driver.maximize_window()

# -----------------------------------
# SEARCH QUERIES
# -----------------------------------

queries = [

    "data scientist",
    "machine learning engineer",
    "data analyst",
    "python developer",
    "ai engineer"

]

# -----------------------------------
# STORAGE
# -----------------------------------

data = []

# -----------------------------------
# SCRAPING LOOP
# -----------------------------------


for query in queries:

    print(f"\nSCRAPING QUERY: {query}")

    # --------------------------------
    # MULTIPLE PAGES
    # --------------------------------

    for start in range(0, 30, 10):

        print(f"PAGE START: {start}")

        url = f"https://in.indeed.com/jobs?q={query}&start={start}"

        driver.get(url)

        # human-like delay
        time.sleep(random.uniform(6, 10))

        # --------------------------------
        # PARSE HTML
        # --------------------------------

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        jobs = soup.select("[data-testid='slider_item']")

        print("TOTAL JOBS:", len(jobs))

        # --------------------------------
        # SCRAPE JOBS
        # --------------------------------

        for job in jobs:

            # TITLE
            title_tag = job.select_one("span[title]")

            title = title_tag.get_text(strip=True) if title_tag else ""

            # COMPANY
            company_tag = job.select_one(
                "span[data-testid='company-name']"
            )

            company = company_tag.get_text(strip=True) if company_tag else ""

            # LOCATION
            location_tag = job.select_one(
                "div[data-testid='text-location']"
            )

            location = location_tag.get_text(strip=True) if location_tag else ""

            # LINK
            link_tag = job.select_one("a")

            if link_tag:

                link = link_tag.get("href", "")

                if link.startswith("/"):

                    link = "https://in.indeed.com" + link

            else:

                link = ""

            # STORE
            data.append({

                "title": title,
                "company": company,
                "location": location,
                "link": link

            })

        # --------------------------------
        # EXTRA HUMAN-LIKE WAIT
        # --------------------------------

        time.sleep(random.uniform(5, 8))

# -----------------------------------
# CLOSE DRIVER
# -----------------------------------

driver.quit()

# -----------------------------------
# DATAFRAME
# -----------------------------------

df = pd.DataFrame(data)

# -----------------------------------
# CLEANING
# -----------------------------------

df.drop_duplicates(inplace=True)

df = df[df['title'] != ""]

df.reset_index(drop=True, inplace=True)

# -----------------------------------
# SAVE CSV
# -----------------------------------

df.to_csv("indeed_jobs.csv", index=False)

print("\nDATA SAVED SUCCESSFULLY")
print(df.shape)

print(df.head())


