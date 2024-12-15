import requests
import openpyxl
import time

# Configuration constants
SPREADSHEET_FILE = "odds_data.xlsx"  # Path to the output Excel file
SHEET_NAME = "Sheet1"  # Name of the sheet in the Excel file
API_KEY = "YOUR_API_KEY"  # Replace with your API key from The Odds API
SPORT_KEY = "americanfootball_nfl"  # Sport key for the desired sport
MARKETS = "h2h,spreads"  # Comma-separated list of betting markets
REGIONS = "us"  # Supported regions: us, uk, eu, au
ODDS_FORMAT = "american"  # Odds format: 'american' or 'decimal'
DATE_FORMAT = "iso"  # Date format: 'iso' or 'unix'
UPDATES_PER_MINUTE = 12  # Number of updates per minute (e.g., 12 updates = every 5 seconds)


def fetch_odds(api_key, sport_key, markets, regions, odds_format, date_format):
    """
    Fetch odds data from The Odds API for the specified parameters.

    Args:
        api_key (str): The Odds API key.
        sport_key (str): Sport key (e.g., 'americanfootball_nfl').
        markets (str): Comma-separated list of betting markets (e.g., 'h2h,spreads').
        regions (str): Comma-separated list of regions (e.g., 'us').
        odds_format (str): Format of the odds ('american' or 'decimal').
        date_format (str): Format of the date ('iso' or 'unix').

    Returns:
        dict: A dictionary containing 'metaData' and 'eventData' for spreadsheet output.
    """
    url = (
        f"https://api.the-odds-api.com/v4/sports/{sport_key}/odds?"
        f"apiKey={api_key}&regions={regions}&markets={markets}&oddsFormat={odds_format}&dateFormat={date_format}"
    )
    response = requests.get(url, headers={"content-type": "application/json"})
    response.raise_for_status()
    return {
        "metaData": format_response_meta_data(response.headers),
        "eventData": format_events(response.json()),
    }


def format_events(events):
    """
    Format the odds API response into a tabular structure for Excel output.

    Args:
        events (list): List of events from the API response.

    Returns:
        list: A 2D list where each sublist is a row for spreadsheet output.
    """
    rows = [
        [
            "id",
            "commence_time",
            "bookmaker",
            "last_update",
            "market",
            "home_team",
            "home_odd",
            "home_point",
            "away_team",
            "away_odd",
            "away_point",
            "draw_odd",
        ]
    ]
    for event in events:
        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                outcome_home = next((o for o in market["outcomes"] if o["name"] == event["home_team"]), {})
                outcome_away = next((o for o in market["outcomes"] if o["name"] == event["away_team"]), {})
                outcome_draw = next((o for o in market["outcomes"] if o["name"] == "Draw"), {})
                rows.append([
                    event["id"],
                    event["commence_time"],
                    bookmaker["key"],
                    bookmaker["last_update"],
                    market["key"],
                    outcome_home.get("name"),
                    outcome_home.get("price"),
                    outcome_home.get("point"),
                    outcome_away.get("name"),
                    outcome_away.get("price"),
                    outcome_away.get("point"),
                    outcome_draw.get("price"),
                ])
    return rows


def format_response_meta_data(headers):
    """
    Extract metadata from the response headers.

    Args:
        headers (dict): Response headers from the API request.

    Returns:
        list: A list of metadata rows for spreadsheet output.
    """
    return [
        ["Requests Used", headers.get("x-requests-used")],
        ["Requests Remaining", headers.get("x-requests-remaining")],
    ]


def main():
    """
    Main function to fetch odds data periodically and save them to an Excel file.

    This function clears the spreadsheet and updates it with new odds data at intervals
    determined by `UPDATES_PER_MINUTE`.

    Writes:
        An Excel file with metaData and eventData saved to `SPREADSHEET_FILE`.
    """
    # Initialize the Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME

    for _ in range(UPDATES_PER_MINUTE):
        # Fetch odds data
        data = fetch_odds(API_KEY, SPORT_KEY, MARKETS, REGIONS, ODDS_FORMAT, DATE_FORMAT)

        # Clear the spreadsheet content
        ws.delete_rows(1, ws.max_row)

        # Write metadata
        for row in data["metaData"]:
            ws.append(row)

        # Write an empty row as spacing
        ws.append([])

        # Write event data
        for row in data["eventData"]:
            ws.append(row)

        # Save the workbook to a file
        wb.save(SPREADSHEET_FILE)
        print(f"Updated data saved to {SPREADSHEET_FILE}")

        # Pause before the next update
        time.sleep(60 / UPDATES_PER_MINUTE)


if __name__ == "__main__":
    main()