"""
This module contains the functionality to scrape API endpoints based on a provided configuration file.

The scraper checks a base URL against a list of known endpoint snippets and specific endpoints, generating a
report on which endpoints are active or inactive based on their HTTP response status.
"""

import requests
import os
import itertools
import toml

def read_endpoints_config():
    """
    Reads the endpoint configurations from a TOML file.

    :return: A dictionary containing the configuration for versions, resources, and known endpoints.
    """
    config_path = os.path.join(os.path.dirname(__file__), 'endpoints_config.toml')
    with open(config_path, 'r') as toml_file:
        return toml.load(toml_file)

def generate_combinations(config):
    """
    Generates combinations of version and resource snippets from the configuration.

    :param config: Configuration dictionary containing versions and resources lists.
    :return: A generator yielding combined endpoint paths.
    """
    versions = config['snippets']['versions']
    resources = config['snippets']['resources']
    for version, resource in itertools.product(versions, resources):
        if version or resource:  # Exclude the empty/empty combination
            yield f"{version}{resource}"

def scrape_endpoints(base_url, config):
    """
    Scrapes the specified base URL for the configured endpoints.

    :param base_url: The base URL to scrape.
    :param config: Configuration dictionary.
    :return: A list of tuples containing the endpoint and its status ('Existing' or 'Not Found').
    """
    found_endpoints = []

    # Check combined endpoints from snippets
    for endpoint in generate_combinations(config):
        status = check_endpoint(f"{base_url}{endpoint}")
        if status != 'Not Found':
            found_endpoints.append((endpoint, status))

    # Check full known endpoints
    for endpoint in config['full']['known']:
        status = check_endpoint(f"{base_url}{endpoint}")
        if status != 'Not Found':
            found_endpoints.append((endpoint, status))

    return found_endpoints

def check_endpoint(url):
    """
    Checks the specified URL and categorizes it based on the HTTP response status.

    :param url: The URL to check.
    :return: 'Existing' if the endpoint responds with any status code other than 404, 408, or 410. 'Not Found' otherwise.
    """
    try:
        print(f"Checking {url}")
        response = requests.get(url)
        print(f"Status: {response.status_code}")
        if response.status_code in [404, 408, 410]:
            return 'Not Found'
        else:
            return f'Existing (Status: {response.status_code})'
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return 'Not Found'

def display_results(found_endpoints):
    """
    Displays the found endpoints in a tree-like structure, along with their status.

    :param found_endpoints: A list of tuples containing endpoints and their statuses.
    """
    print("Found Endpoints:")
    for endpoint, status in found_endpoints:
        print(f"└── {endpoint}: {status}")

def format_base_url(input_url):
    """
    Formats the input URL to ensure it has 'http://' as the default scheme
    and trims any leading or trailing whitespace.

    Parameters:
    - input_url (str): The input URL potentially with leading/trailing whitespace
                       and missing 'http://' prefix.

    Returns:
    - str: The formatted URL with 'http://' added if no scheme was present and
           any whitespace removed.
    """
    # Trim whitespace
    trimmed_url = input_url.strip()

    # Check if the scheme is missing
    if not trimmed_url.startswith(('http://', 'https://')):
        formatted_url = 'http://' + trimmed_url
    else:
        formatted_url = trimmed_url

    return formatted_url

def main():
    """
    Main function to execute the scraper from the command line.
    """
    import sys
    if len(sys.argv) != 2:
        print("Usage: python scraper.py <base_url>")
        sys.exit(1)
    base_url = format_base_url(sys.argv[1])
    config = read_endpoints_config()
    print(f"Searching for endpoints at {base_url}...")
    endpoints = scrape_endpoints(base_url, config)
    display_results(endpoints)

if __name__ == "__main__":
    main()
