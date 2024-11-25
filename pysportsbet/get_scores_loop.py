import requests
import openpyxl
import time

# Configuration constants
SPREADSHEET_FILE = "scores_data.xlsx"  # Path to the output Excel file
SHEET_NAME = "Scores"  # Name of the sheet in the Excel file
API_KEY = "YOUR_API_KEY"  # Replace with your API key from The Odds API
SPORT_KEY = "americanfootball_nfl"  # Sport key for querying scores
DAYS_FROM = 1  # Number of days in the past to fetch scores (0 for live games only)
DATE_FORMAT = "iso"  # Date format: 'iso' or 'unix'
UPDATES_PER_MINUTE = 2  # Number of updates per minute (e.g., 2 updates = every 30 seconds)


def fetch_scores(api_key, sport_key, days_from, date_format):
    """
    Fetch scores data from The Odds API.

    Args:
        api_key (str): The Odds API key.
        sport_key (str): Sport key (e.g., 'americanfootball_nfl').
        days_from (int): Return scores from this many days in the past (valid values: 0-3).
        date_format (str): Format of the date ('iso' or 'unix').

    Returns:
        dict: A dictionary containing metadata and event data.
    """
    url = f"https://api.the-odds-api.com/v4/sports/{sport_key}/scores?apiKey={api_key}&dateFormat={date_format}"
    if days_from != 0:
        url += f"&daysFrom={days_from}"

    response = requests.get(url, headers={"content-type": "application/json"})
    response.raise_for_status()
    return {
        "metaData": format_response_meta_data_scores(response.headers),
        "eventData": format_events_scores(response.json()),
    }


def format_events_scores(events):
    """
    Format the scores data into a tabular structure for Excel output.

    Args:
        events (list): List of events from the API response.

    Returns:
        list: A 2D list where each sublist is a row for spreadsheet output.
    """
    rows = [
        [
            "id", "commence_time", "completed", "last_update",
            "home_team", "home_score", "away_team", "away_score"
        ]
    ]
    for event in events:
        home_score = next(
            (score["score"] for score in event.get("scores", []) if score["name"] == event["home_team"]),
            None
        )
        away_score = next(
            (score["score"] for score in event.get("scores", []) if score["name"] == event["away_team"]),
            None
        )
        rows.append([
            event["id"],
            event["commence_time"],
            event.get("completed", False),
            event.get("last_update"),
            event["home_team"],
            home_score,
            event["away_team"],
            away_score,
        ])
    return rows


def format_response_meta_data_scores(headers):
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
    Main function to fetch scores periodically and save them to an Excel file.

    This function fetches scores data, updates the spreadsheet, and spaces out
    requests based on `UPDATES_PER_MINUTE`.

    Writes:
        An Excel file with metadata and scores data saved to `SPREADSHEET_FILE`.
    """
    # Initialize the Excel workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = SHEET_NAME

    for _ in range(UPDATES_PER_MINUTE):
        # Fetch scores data
        data = fetch_scores(API_KEY, SPORT_KEY, DAYS_FROM, DATE_FORMAT)

        # Clear existing content
        ws.delete_rows(1, ws.max_row)

        # Write metadata
        for row in data["metaData"]:
            ws.append(row)

        # Add an empty row for spacing
        ws.append([])

        # Write scores data
        for row in data["eventData"]:
            ws.append(row)

        # Save the workbook to a file
        wb.save(SPREADSHEET_FILE)
        print(f"Scores data updated and saved to {SPREADSHEET_FILE}")

        # Pause before the next update
        time.sleep(60 / UPDATES_PER_MINUTE)


if __name__ == "__main__":
    main()
