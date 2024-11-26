"""
Project: NBA Player Stats Scraper
Description:
    This script automates the process of scraping NBA player stats from the NBA Stats website.
    It navigates through the website, collects player data, and saves it in both CSV and JSON formats.
    The script handles pagination, dynamic page content loading, and consent button clicks.

    Files Created:
        - CSV file for structured tabular data.
        - JSON file for flexible data handling.

Author: [Mostafa Ibrahim]
Date: [27/11/2024]
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from header import Header
from body import Body
from datetime import date


def next_page():
    """
    Navigates to the next page by clicking the 'Next' button on the NBA Stats website.
    """
    next_button = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[5]/button[2]")
        )
    )
    time.sleep(1.5)  # Adding a small delay to ensure the button is ready for interaction
    next_button.click()
    print("Next button clicked successfully!")


def accept():
    """
    Clicks the 'Accept' button for consent if it appears on the page.
    """
    accept_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='onetrust-accept-btn-handler']"))
    )
    accept_button.click()
    print("Accept button clicked successfully!")


# Initialize Chrome WebDriver with options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

# URL for NBA player stats
url = 'https://www.nba.com/stats/players/boxscores'

# File names for today's scraped data
today_file_csv = f"{date.today()}.csv"
today_file_json = f"{date.today()}.json"

# Open the NBA stats website
driver.get(url)

# Initialize Body object for scraping player stats
body = Body(url, driver)

# ========================================== GET HEADERS NAME ==========================================
# Fetch column names for the data table
header = Header(url, driver)
header.fetch_page()
get_headers = header.get_column_names()

# ======================================= GET ALL PAGES NUMBER =========================================
# Get the total number of pages from the pagination element
all_pages_element = wait.until(
    EC.visibility_of_element_located(
        (By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[4]")
    )
).text
ALL_PAGES_NUMBER = int(all_pages_element.split(" ")[-1])

# Get the current page number options from the dropdown
CURRENT_PAGE = driver.find_elements(
    By.XPATH, "//*[@id='__next']/div[2]/div[2]/div[3]/section[2]/div/div[2]/div[2]/div[1]/div[3]/div/label/div/select"
)
CURRENT_PAGE_NUMBER = [current.text for current in CURRENT_PAGE]
INT_CURRENT_NUMBERS = [
    int(num) for num in CURRENT_PAGE_NUMBER[0].replace("All", "").split("\n") if num.isdigit()
]

# ===================================== SCRAPE EACH PAGE DATA =========================================
for number_of_page in INT_CURRENT_NUMBERS:
    print(f"Page number: {number_of_page}")

    # Fetch the current page content
    body.fetch_page()
    x = body.get_body()

    # Handle 'Accept' button if it appears
    try:
        accept()
    except Exception:
        pass

    # Navigate to the next page
    try:
        next_page()
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        next_page()

    # Ask user if they want to continue scraping
    if input(f"Do you want to scrape page {number_of_page + 1}? [Y or N]: ").lower() == "y":
        continue
    else:
        break

# ====================================== UPLOAD DATA TO FILES =========================================
print("\nNow We're Going To Upload Data\n")

# Save data to CSV and JSON files
header.upload_to_csv(today_file_csv)
body.upload_data_to_csv(today_file_csv)
body.upload_data_json(today_file_json)


