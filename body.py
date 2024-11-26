import csv
import json
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

class Body:
    def __init__(self, url, driver):
        """
        Initializes the Body class with required parameters.
        - url: The target URL of the page.
        - driver: Selenium WebDriver instance.
        """
        self.url = url
        self.driver = driver
        self.table_rows = []  # Stores rows of the table body.
        self.extracted_data = []  # Stores extracted player data.
        self.wait = WebDriverWait(self.driver, 10)
        self.players_data = {}  # Stores player data for JSON.

    def fetch_page(self):
        """
        Fetches the table rows (body) from the page.
        Retries loading rows if an exception occurs.
        """
        try:
            # Locate the table rows in the body.
            self.table_rows = self.wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".Crom_table__p1iZz tbody tr")
            )
            print("Table body loaded successfully.")
        except Exception:
            # Refresh the page and try again in case of an error.
            self.driver.refresh()
            self.table_rows = self.wait.until(
                lambda d: d.find_elements(By.CSS_SELECTOR, ".Crom_table__p1iZz tbody tr")
            )
            print("Table body loaded successfully after refresh.")

    def get_body(self):
        """
        Extracts data for each player from the table rows.
        Ensures duplicate data is not added to the extracted data list.
        """
        if self.table_rows:
            for index, row in enumerate(self.table_rows):
                # Get all cell data for the current row.
                cells = row.find_elements(By.CSS_SELECTOR, value="td")
                # Create a dictionary for player data.
                player_data = {
                    "PLAYER": cells[0].text,
                    "TEAM": cells[1].text,
                    "MATCH_UP": cells[2].text,
                    "DATE": cells[3].text,
                    "W/L": cells[4].text,
                    "MIN": cells[5].text,
                    "PTS": cells[6].text,
                    "FGM": cells[7].text,
                    "FGA": cells[8].text,
                    "FG%": cells[9].text,
                    "3PM": cells[10].text,
                    "3PA": cells[11].text,
                    "3P%": cells[12].text,
                    "FTM": cells[13].text,
                    "FTA": cells[14].text,
                    "FT%": cells[15].text,
                    "OREB": cells[16].text,
                    "DREB": cells[17].text,
                    "REB": cells[18].text,
                    "AST": cells[19].text,
                    "STL": cells[20].text,
                    "BLK": cells[21].text,
                    "TOV": cells[22].text,
                    "PF": cells[23].text,
                    "+/-": cells[24].text,
                    "FP": cells[25].text
                }
                # Avoid duplicate entries.
                if player_data not in self.extracted_data:
                    self.extracted_data.append(player_data)
                    print(f"Player {index}: {player_data}\n")
        else:
            print("No data found in the table body.")
        return self.extracted_data

    def upload_data_to_csv(self, file_name):
        """
        Uploads player data to a CSV file, ensuring no duplicate players are added.
        - file_name: The target CSV file name.
        """
        # Check if the file exists and is not empty.
        if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
            with open(file_name, mode="r", newline="", encoding="utf-8") as data_file:
                reader = csv.DictReader(data_file)
                existing_players = set()
                for row in reader:
                    if 'PLAYER' in row:
                        existing_players.add(row['PLAYER'])
                    else:
                        print("Warning: Column 'PLAYER' is missing in some rows.")
        else:
            existing_players = set()

        # Append new player data to the file.
        with open(file_name, mode="a", newline="", encoding="utf-8") as data_file:
            writer = csv.writer(data_file)
            for data in self.extracted_data:
                player_name = data["PLAYER"]
                if player_name not in existing_players:
                    writer.writerow(data.values())
                    existing_players.add(player_name)
            print("Player data successfully uploaded to CSV.")

    def upload_data_json(self, file_name):
        """
        Uploads player data to a JSON file, ensuring no duplicate players are added.
        - file_name: The target JSON file name.
        """
        # Load existing data if the file exists.
        if os.path.exists(file_name) and os.stat(file_name).st_size > 0:
            with open(file_name, 'r', encoding='utf-8') as file:
                self.players_data = json.load(file)
        else:
            print("JSON file does not exist or is empty. Creating a new file.")
            self.players_data = {}

        # Add new player data to the JSON dictionary.
        for player in self.extracted_data:
            player_name = player["PLAYER"]
            if player_name not in self.players_data:
                self.players_data[player_name] = player

        # Save the updated data back to the JSON file.
        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(self.players_data, file, indent=2)
        print("Player data successfully uploaded to JSON.")





