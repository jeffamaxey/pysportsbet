import requests
import openpyxl
import time
from datetime import datetime, timedelta


class TheOddsAPIClient:
    """
    A client for interacting with The Odds API, fetching data such as odds, scores, player props,
    and historical data, and saving it to Excel files.
    """

    def __init__(self, api_key, spreadsheet_file):
        """
        Initialize the Odds API client.

        Args:
            api_key (str): Your API key for The Odds API.
            spreadsheet_file (str): Path to the Excel file for saving data.
        """
        self.api_key = api_key
        self.spreadsheet_file = spreadsheet_file

    def fetch_data(self, url, params):
        """
        Fetch data from a specified URL.

        Args:
            url (str): The API endpoint URL.
            params (dict): The parameters for the API request.

        Returns:
            dict: The JSON response from the API.
        """
        response = requests.get(url, params=params, headers={"content-type": "application/json"})
        response.raise_for_status()
        return response.json()

    def fetch_scores(self, sport_key, days_from, date_format):
        """
        Fetch scores data from The Odds API.

        Args:
            sport_key (str): Sport key (e.g., 'americanfootball_nfl').
            days_from (int): Number of days in the past to fetch scores.
            date_format (str): Format of the date ('iso' or 'unix').

        Returns:
            dict: Metadata and formatted event data.
        """
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores"
        params = {"apiKey": self.api_key, "daysFrom": days_from, "dateFormat": date_format}
        return self.fetch_data(url, params)

    def fetch_player_props(self, sport_key, markets, regions, odds_format, date_format):
        """
        Fetch player props data for a sport.

        Args:
            sport_key (str): Sport key for querying player props.
            markets (str): Comma-separated list of player prop markets.
            regions (str): Regions for bookmakers.
            odds_format (str): Odds format ('american' or 'decimal').
            date_format (str): Date format ('iso' or 'unix').

        Returns:
            list: Player props data for all events.
        """
        url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds"
        params = {
            "apiKey": self.api_key,
            "markets": markets,
            "regions": regions,
            "oddsFormat": odds_format,
            "dateFormat": date_format,
        }
        return self.fetch_data(url, params)

    def format_scores(self, events):
        """
        Format the scores data for spreadsheet output.

        Args:
            events (list): List of events with score data.

        Returns:
            list: Formatted rows for spreadsheet output.
        """
        rows = [
            ["id", "commence_time", "completed", "last_update", "home_team", "home_score", "away_team", "away_score"]
        ]
        for event in events:
            home_score = next(
                (score["score"] for score in event.get("scores", []) if score["name"] == event["home_team"]), None)
            away_score = next(
                (score["score"] for score in event.get("scores", []) if score["name"] == event["away_team"]), None)
            rows.append([
                event["id"], event["commence_time"], event.get("completed", False),
                event.get("last_update"), event["home_team"], home_score,
                event["away_team"], away_score,
            ])
        return rows

    def save_to_excel(self, data, headers, sheet_name="Sheet1"):
        """
        Save data to an Excel file.

        Args:
            data (list): List of rows to save.
            headers (list): List of column headers.
            sheet_name (str): Name of the sheet in the Excel file.
        """
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = sheet_name

        # Write headers
        ws.append(headers)

        # Write data rows
        for row in data:
            ws.append(row)

        # Save workbook
        wb.save(self.spreadsheet_file)

    def run_scores_loop(self, sport_key, days_from, date_format, updates_per_minute):
        """
        Periodically fetch and save scores data to an Excel file.

        Args:
            sport_key (str): Sport key for querying scores.
            days_from (int): Number of days in the past to fetch scores.
            date_format (str): Date format ('iso' or 'unix').
            updates_per_minute (int): Number of updates per minute.
        """
        headers = ["id", "commence_time", "completed", "last_update", "home_team", "home_score", "away_team",
                   "away_score"]
        for _ in range(updates_per_minute):
            scores_data = self.fetch_scores(sport_key, days_from, date_format)
            formatted_scores = self.format_scores(scores_data)
            self.save_to_excel(formatted_scores, headers, sheet_name="Scores")
            time.sleep(60 / updates_per_minute)

    def fetch_and_save_player_props(self, sport_key, markets, regions, odds_format, date_format):
        """
        Fetch and save player props data to an Excel file.

        Args:
            sport_key (str): Sport key for querying player props.
            markets (str): Comma-separated list of player prop markets.
            regions (str): Regions for bookmakers.
            odds_format (str): Odds format ('american' or 'decimal').
            date_format (str): Date format ('iso' or 'unix').
        """
        headers = [
            "id", "commence_time", "bookmaker", "last_update", "home_team",
            "away_team", "market", "outcome_name", "description", "price", "point"
        ]
        events = self.fetch_player_props(sport_key, markets, regions, odds_format, date_format)
        rows = []
        for event in events:
            for bookmaker in event.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        rows.append([
                            event["id"], event["commence_time"], bookmaker["key"],
                            bookmaker["last_update"], event["home_team"], event["away_team"],
                            market["key"], outcome.get("name"), outcome.get("description"),
                            outcome.get("price"), outcome.get("point")
                        ])
        self.save_to_excel(rows, headers, sheet_name="PlayerProps")


# Example usage
if __name__ == "__main__":
    api_client = TheOddsAPIClient(api_key="YOUR_API_KEY", spreadsheet_file="odds_data.xlsx")

    # Run scores loop
    api_client.run_scores_loop(
        sport_key="americanfootball_nfl",
        days_from=1,
        date_format="iso",
        updates_per_minute=2
    )

    # Fetch and save player props
    api_client.fetch_and_save_player_props(
        sport_key="americanfootball_nfl",
        markets="player_pass_tds,player_pass_yds,player_pass_completions",
        regions="us",
        odds_format="american",
        date_format="iso"
    )
