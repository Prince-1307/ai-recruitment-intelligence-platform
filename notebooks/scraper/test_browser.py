import undetected_chromedriver as uc

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
# OPEN INDEED
# -----------------------------------

driver.get("https://in.indeed.com")

input("Press ENTER after verification/login...")

driver.quit()