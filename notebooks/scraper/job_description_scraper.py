# =========================================================
# INDEED JOB DESCRIPTION SCRAPER
# =========================================================

import undetected_chromedriver as uc

from bs4 import BeautifulSoup

import pandas as pd

import time
import random


# =========================================================
# LOAD JOB LINKS DATASET
# =========================================================

df = pd.read_csv("Combined_indeed_jobs.csv")

print("TOTAL JOBS:", len(df))


# =========================================================
# CHROME OPTIONS
# =========================================================

options = uc.ChromeOptions()

# your trusted browser session
options.add_argument(
    r"--user-data-dir=C:/selenium_profile"
)

# reduce automation detection
options.add_argument(
    "--disable-blink-features=AutomationControlled"
)

# optional
options.add_argument("--start-maximized")


# =========================================================
# DRIVER
# =========================================================

driver = uc.Chrome(
    version_main=147,
    options=options
)

driver.maximize_window()


# =========================================================
# STORAGE
# =========================================================

descriptions = []


# =========================================================
# SCRAPING LOOP
# =========================================================

for i, link in enumerate(df['link']):

    print(f"\nSCRAPING JOB {i+1}/{len(df)}")

    # -----------------------------------------------------
    # INVALID LINK CHECK
    # -----------------------------------------------------

    if pd.isna(link) or link == "":

        descriptions.append("")

        continue

    try:

        # -------------------------------------------------
        # OPEN JOB PAGE
        # -------------------------------------------------

        driver.get(link)

        # human-like delay
        time.sleep(random.uniform(5, 8))

        # -------------------------------------------------
        # CAPTCHA DETECTION
        # -------------------------------------------------

        page_text = driver.page_source.lower()

        if "verify you are human" in page_text \
        or "additional verification required" in page_text:

            print("\nCAPTCHA DETECTED")
            input("Solve CAPTCHA manually then press ENTER...")

            time.sleep(5)

        # -------------------------------------------------
        # PAGE HTML
        # -------------------------------------------------

        html = driver.page_source

        soup = BeautifulSoup(html, "html.parser")

        # -------------------------------------------------
        # JOB DESCRIPTION
        # -------------------------------------------------

        desc_tag = soup.select_one(
            "#jobDescriptionText"
        )

        if desc_tag:

            description = desc_tag.get_text(
                separator=" ",
                strip=True
            )

            # clean extra spaces
            description = " ".join(description.split())

        else:

            description = ""

        # -------------------------------------------------
        # STORE
        # -------------------------------------------------

        descriptions.append(description)

        # preview
        print(description[:10])

    except Exception as e:

        print("ERROR:", e)

        descriptions.append("")

    # -----------------------------------------------------
    # SAVE BACKUP AFTER EVERY 5 JOBS
    # -----------------------------------------------------

    if (i + 1) % 5 == 0:

        temp_df = df.copy()

        temp_df['description'] = descriptions + [""] * (
            len(df) - len(descriptions)
        )

        temp_df.to_csv(
            "backup_jobs.csv",
            index=False
        )

        print("BACKUP SAVED")

    # -----------------------------------------------------
    # EXTRA HUMAN-LIKE WAIT
    # -----------------------------------------------------

    time.sleep(random.uniform(4, 7))


# =========================================================
# CLOSE DRIVER
# =========================================================

driver.quit()


# =========================================================
# FINAL DATAFRAME
# =========================================================

df['description'] = descriptions


# =========================================================
# CLEANING
# =========================================================

# remove empty descriptions
df = df[df['description'] != ""]

# remove duplicates
df.drop_duplicates(inplace=True)

# reset index
df.reset_index(drop=True, inplace=True)


# =========================================================
# SAVE FINAL DATASET
# =========================================================

df.to_csv(
    "indeed_jobs_with_descriptions.csv",
    index=False
)

print("\nDATA SAVED SUCCESSFULLY")

print(df.shape)

print(df.head())