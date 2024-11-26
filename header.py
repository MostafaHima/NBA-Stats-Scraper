from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import csv

class Header:
    def __init__(self, url, driver):
        """
        Initializes the Header class with the required parameters.
        - url: The target URL of the page.
        - driver: Selenium WebDriver instance.
        """
        self.url = url
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.headers = []  # Stores the header elements.
        self.header_names = []  # Stores the header names as text.

    def fetch_page(self):
        """
        Fetches the headers from the table on the page.
        Retries loading the headers if the page needs to be refreshed.
        """
        try:
            # Locate the headers using CSS selectors.
            self.headers = self.wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".Crom_table__p1iZz thead tr th")
            )
            print("Headers loaded successfully.")
        except Exception:
            # Refresh the page if an exception occurs and try again.
            self.driver.refresh()
            self.headers = self.wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".Crom_table__p1iZz thead tr th")
            )
            print("Headers loaded successfully after refresh.")

    def get_column_names(self):
        """
        Extracts and returns the names of the columns from the header elements.
        """
        self.header_names = [header.text.strip() for header in self.headers]
        return self.header_names

    def upload_to_csv(self, file_name):
        """
        Writes the headers to a CSV file if it's not already present.
        - file_name: Name of the CSV file to write to.
        """
        with open(file_name, newline="", mode="a", encoding="utf-8") as nba_header_data:
            writer = csv.writer(nba_header_data)
            # Write headers only if the file is empty.
            if nba_header_data.tell() == 0:
                writer.writerow(self.header_names)
        print("Headers uploaded successfully.")

