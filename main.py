"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie

author: Štěpán Pala
email: Palast@seznam.cz
"""

import csv
import sys

import requests
from bs4 import BeautifulSoup


def get_parsed_page(page_url) -> BeautifulSoup:
    """
    Downloads the page from the given URL and returns the parsed content.

    Args:
        page_url (str): The URL of the page to download and parse.

    Returns:
        BeautifulSoup: The parsed content of the page or None if an error
        occurred.
    """
    try:
        response = requests.get(page_url, timeout=10)
        response.raise_for_status() # Checks if the response status code is 200
        return BeautifulSoup(response.content, "html.parser")
    except requests.exceptions.RequestException as e:
        print(f"Download error: {e}")
        return None


def _extract_codes(parsed_soup: BeautifulSoup, table_index: int) -> list[str]:
    """
    Extracts the codes from the table using CSS selectors.

    Args:
        parsed_soup (BeautifulSoup): The parsed HTML content of the page.
        table_index (int): The index of the table to extract data from.

    Returns:
        list: A list of extracted codes.
    """
    codes = [
        code_tag.text.strip()
        for code_tag in parsed_soup.select(
            f"td.cislo[headers='t{table_index}sa1 t{table_index}sb1']"
        )
    ]
    return codes


def _extract_locations(
        parsed_soup: BeautifulSoup, table_index: int
    ) -> list[str]:
    """
    Extracts the locations from the table using CSS selectors.

    Args:
        parsed_soup (BeautifulSoup): The parsed HTML content of the page.
        table_index (int): The index of the table to extract data from.

    Returns:
        list: A list of extracted locations.
    """
    # Creates an empty list to store the locations
    locations = []
    # Finds all td tags containing the location data
    location_tags = parsed_soup.find_all(
        "td", headers=[f"t{table_index}sa1 t{table_index}sb2"]
    )
    # Checks if the location is a link or plain text
    for location_tag in location_tags:
        a_tag = location_tag.find("a")
        if a_tag:
            # Extracts and appends the text if the location is a link
            locations.append(a_tag.text.strip())
        else:
            # Extracts and appends the text if the location is plain text
            locations.append(location_tag.text.strip())
    return locations


def _extract_links(parsed_soup: BeautifulSoup, table_index: int) -> list[str]:
    """
    Extracts the links from the table using CSS selectors.

    Args:
        parsed_soup (BeautifulSoup): The parsed HTML content of the page.
        table_index (int): The index of the table to extract data from.

    Returns:
        list: A list of extracted links.
    """
    # Finds all the links to the detail pages
    links = [
        link_tag.find("a")["href"]
        for link_tag in parsed_soup.select(
            f"td.cislo[headers='t{table_index}sa1 t{table_index}sb1']"
        ) if link_tag.find("a")
            and "ps311" in link_tag.find("a")["href"]
    ]
    return links


def extract_table_data(
        parsed_soup: BeautifulSoup, table_index: int
    ) -> tuple[list[str], list[str], list[str]]:
    """
    Extracts data from the main table for the given table index.

    Args:
        parsed_soup (BeautifulSoup): The parsed HTML content of the page.
        table_index (int): The index of the table to extract data from.

    Returns:
        list: A tuple containing three lists with the extracted data: codes,
        locations, and links.
    """
    codes = _extract_codes(parsed_soup, table_index)
    locations = _extract_locations(parsed_soup, table_index)
    links = _extract_links(parsed_soup, table_index)
    return codes, locations, links


def _extract_registered_voters(detail_soup: BeautifulSoup) -> str:
    """
    Extracts the number of registered voters from the detail page.

    Args:
        detail_soup (BeautifulSoup): The parsed HTML content of the detail

    Returns:
        str: The number of registered voters.
    """
    registered = (
        detail_soup.find("td", {"class": "cislo"}, headers="sa2").text.strip()
        if detail_soup.find("td", {"class": "cislo"}, headers="sa2")
        else None
    )
    return registered


def _extract_envelopes(detail_soup: BeautifulSoup) -> str:
    """
    Extracts the number of envelopes from the detail page.

    Args:
        detail_soup (BeautifulSoup): The parsed HTML content of the detail

    Returns:
        str: The number of envelopes.
    """
    envelopes = (
        detail_soup.find("td", {"class": "cislo"}, headers="sa3").text.strip()
        if detail_soup.find("td", {"class": "cislo"}, headers="sa3")
        else None
    )
    return envelopes


def _extract_valid_votes(detail_soup: BeautifulSoup) -> str:
    """
    Extracts the number of valid votes from the detail page.

    Args:
        detail_soup (BeautifulSoup): The parsed HTML content of the detail

    Returns:
        str: The number of valid votes.
    """
    valid = (
        detail_soup.find("td", {"class": "cislo"}, headers="sa6").text.strip()
        if detail_soup.find("td", {"class": "cislo"}, headers="sa6")
        else None
    )
    return valid


def _extract_party_results(detail_soup: BeautifulSoup) -> dict[str, str]:
    """
    Extracts the party results from the detail page.

    Args:
        detail_soup (BeautifulSoup): The parsed HTML content of the detail

    Returns:
        dict: A dictionary containing the party results.
    """
    party_results = {}
    # Iterates over the two tables with party results
    for party_table_index in range(1, 3):
        # Extracts the party names
        party_names = [
            party_tag.text.strip()
            for party_tag in detail_soup.select(
                f"td.overflow_name[headers='t{party_table_index}sa1 "
                f"t{party_table_index}sb2']"
            )
        ]
        # Extracts the party votes
        party_votes = [
            party_tag.text.strip()
            for party_tag in detail_soup.select(
                f"td.cislo[headers='t{party_table_index}sa2 "
                f"t{party_table_index}sb3']"
            )
        ]
        # Updates the party results dictionary with the party names and votes
        party_results.update(dict(zip(party_names, party_votes)))
    return party_results


def extract_detail_page_data(
        detail_soup: BeautifulSoup
    ) -> dict[str, str]:
    """
    Extracts data from the detail page.

    Args:
        detail_soup (BeautifulSoup): The parsed HTML content of the detail
        page.

    Returns:
        tuple: A tuple containing the extracted data:
        registered, envelopes, valid, and party_results.
    """
    registered = _extract_registered_voters(detail_soup)
    envelopes = _extract_envelopes(detail_soup)
    valid = _extract_valid_votes(detail_soup)
    party_results = _extract_party_results(detail_soup)
    return {
        "Registered": registered,
        "Envelopes": envelopes,
        "Valid": valid,
        **party_results,
    }


def extract_data(
        parsed_soup: BeautifulSoup, detail_base_url: str, page_url: str
    ) -> list[dict]:
    """
    Extracts relevant information from the parsed data.
    
    Args:
        parsed_soup (BeautifulSoup): The parsed HTML content of the page.
        detail_base_url (str): The base URL for the detail pages.
        page_url (str): The URL of the page to extract data from.
        
    Returns:
        list: A list containing the extracted data.
    """
    print(f"Extracting data from {page_url}...")
    extracted_data = []

    for table_index in range(1, 4):
        codes, locations, links = extract_table_data(parsed_soup, table_index)

        # Iterates over the codes, locations, and links
        for code, location, link in zip(codes, locations, links):

            # Parses the detail page
            detail_soup = get_parsed_page(detail_base_url + link)

            # Extracts data from the detail page
            detail_data = extract_detail_page_data(detail_soup) if detail_soup else {}

            # Joins the data from both pages
            extracted_data.append(
                {
                    "Code": code,
                    "Location": location,
                    **detail_data,
                }
            )

    print("Data extracted successfully.")
    return extracted_data


def save_to_csv(extracted_data: list[dict], filename: str):
    """
    Saves the extracted data to a CSV file.

    Args:
        extracted_data (list): The extracted data to save.
        filename (str): The name of the output file.
    """
    print(f"Saving data to {filename}...")
    with open(filename, mode="w", encoding="utf-8", newline="") as csvfile:
        fieldnames = extracted_data[0].keys() if extracted_data else []
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(extracted_data)
    print("Data saved successfully.")


def get_command_line_arguments() -> tuple[str, str]:
    """
    Gets the URL and the output filename from the command line arguments.

    Returns:
        tuple: A tuple containing the URL and the output filename.
    """
    if len(sys.argv) != 3:
        print(
            "Invalid number of arguments." 
            "Please provide the URL and the output filename."
        )
        sys.exit(1)

    input_url = sys.argv[1]
    output_file = sys.argv[2]

    # Checks if the URL is valid
    if not (
        input_url.startswith("http://") or input_url.startswith("https://")
    ):
        print(
            "Invalid URL or arguments in the wrong order. "
            "Please provide the valid URL and the output filename."
        )
        sys.exit(1)

    return input_url, output_file


def process_election_data(page_url: str, output_file: str):
    """
    Downloads and extracts data from the given URL and saves it to a CSV file.

    Args:
        url (str): The URL of the page to download and extract data from.
        output_filename (str): The name of the output file.
    """
    soup = get_parsed_page(page_url)
    if soup:
        # Extracts the first five parts of the URL to create the base URL
        base_url = "/".join(page_url.split("/")[:5]) + "/"
        data = extract_data(soup, base_url, page_url)
        save_to_csv(data, output_file)
        print("Terminating Elections Scraper...")
    else:
        print("Failed to download or parse data from the URL.")


if __name__ == "__main__":
    url, output_filename = get_command_line_arguments()
    process_election_data(url, output_filename)
