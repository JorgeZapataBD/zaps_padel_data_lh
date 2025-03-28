import logging
from datetime import date, timedelta
from typing import Literal

import regex as re
from airflow.models import Variable
from zaps_core.clients.http_client import HttpClient

logger = logging.getLogger(__name__)


def download_ranking_fip_file(
    date: date,
    fip_category: Literal["Male", "Female", 'Race-Male', 'Race-Female']
) -> str:
    """
    Function that downloads player ranking files from the official
    International Padel Federation (FIP) website for a given date and category.

    :param date: Date for the ranking
    :param fip_category: FIP category
    :return:  Path of downloaded file
    """
    # Set the URL of the file
    filename = f"Ranking-{fip_category}-{date.strftime('%d-%m-%Y')}.pdf"
    url = f"{Variable.get('ZAPS_PADEL_FIP_BASE_URL')}/{date.strftime('%Y')}/{date.strftime('%m')}/{filename}"
    # Make the request and save the file to disk
    response = HttpClient(url).get_data()
    source_file = f"{date.strftime('%Y-%m-%d')}_{filename}"
    with open(f"{source_file}", 'wb') as file:
        file.write(response.content)
    logger.info(f'File {filename} downloaded successfully')
    return source_file


def get_mondays_list(init_date: date) -> list:
    """
    Function to obtain a list of Mondays' dates starting from a given initial date,
    this is to get the historical files for the FIP Rankings.

    :param init_date: Initial date for calculate list of dates
    :return: List of Monday dates
    """
    # Select the first Monday from the given date
    init_date += timedelta(days=1)
    while init_date.weekday() != 0:
        init_date += timedelta(days=1)
    # Generate the list of Mondays up to today
    dates_monday = []
    while init_date <= date.today():
        dates_monday.append(init_date)
        init_date += timedelta(days=7)
    return dates_monday


def format_ranking_fip_header(s_header: str) -> list:
    """
    Function that formats the headers of different files.
    This normalization will be used to parse the content of the PDFs later.

    :param s_header: Text containing the headers (Normally the first row of the file)
    :return: List of normalized headers
    """
    map_headers = {
        'Ranking Race': 'Raceposition',
        'Points Race': 'Racepoints',
        'Title': 'Player',
        'Player Name': 'Player',
        'Name': 'Player',
        'priorPosition': 'Move',
        'ID PLAYER': 'Playerid',
        'Ranking': 'Position',
        'Nationality': 'Countries'
    }
    # Normalize the headers
    for old, new in map_headers.items():
        s_header = s_header.replace(old, new)
    l_header = s_header.split()
    # Fix headers that are not separated by spaces
    l_header = [word for item in l_header for word in re.findall(
        r'[A-Z][a-z]*', item)]
    return l_header


def get_ranking_fip_pattern(l_header: list) -> re.Pattern:
    """
    Function that selects the regular expression to use depending on the file's headers.
    This will capture the fields we need from the text using regular expressions.

    :param l_header: List of normalized headers
    :return: Regex pattern to parse the file content
    """
    options_list = [
        {"list": ['Player', 'Countries', 'Points', 'Position', 'Move'],
            "pattern": r"(?P<player>.+?)(?:\s(?P<country>[A-Z]{3}))?\s(?P<points>\d+)\s(?P<position>\d+)"},
        {"list": ['Player', 'Countries', 'Points', 'Position'],
            "pattern": r"(?P<player>.+?)(?:\s(?P<country>[A-Z]{3}))?\s(?P<points>\d+)\s(?P<position>\d+)"},
        {"list": ['Player', 'Countries', 'Gender', 'Points', 'Playerid', 'Position'],
            "pattern": r"(?P<player>.+?)(?:\s(?P<country>[A-Z]{3}))?\s(?:Male|Female)\s(?P<points>\d+)\s?(?P<player_id>[A-Za-z0-9]+)\s(?P<position>\d+)"},
        {"list": ['Player', 'Countries', 'Gender', 'Points', 'Position', 'Move'],
            "pattern": r"(?P<player>.+?)(?:\s(?P<country>[A-Z]{3}))?\s(?:Male|Female)\s(?P<points>\d+)\s(?P<position>\d+)"},
        {"list": ['Position', 'Player', 'Countries', 'Points'],
            "pattern": r"(?P<position>\d+)\s(?P<player>.+?)(?:\s(?P<country>[A-Z]{3}))?\s(?P<points>\d+)"},
        {"list": ['Position', 'Countries', 'Player', 'Points'],
            "pattern": r"(?P<position>\d+)(?:\s?(?P<country>[A-Z]{3}))?\s(?P<player>.+?)\s(?P<points>\d+)"},
        {"list": ['Playerid', 'Player', 'Raceposition', 'Racepoints'],
            "pattern": r"(?P<player_id>[A-Za-z0-9]+)\s(?P<player>.+?)\s?(?P<position>\d+)\s(?P<points>\d+)"},
        {"list": ['Playerid', 'Player', 'Racepoints', 'Raceposition'],
            "pattern": r"(?P<player_id>[A-Za-z0-9]+)\s(?P<player>.+?)\s?(?P<points>\d+)\s(?P<position>\d+)"},
        {"list": ['Player', 'Racepoints', 'Raceposition'],
            "pattern": r"(?P<player>.+?)\s?(?P<points>\d+)\s(?P<position>\d+)"}
    ]
    for option in options_list:
        if l_header == option["list"]:
            pattern = re.compile(option["pattern"])
            return pattern
    return None
