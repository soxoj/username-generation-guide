#!/usr/bin/env python3
import argparse
import sys
import requests
from bs4 import BeautifulSoup as BS

URL = 'https://www.behindthename.com/name/{username}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
}
TYPES = {
    'variants': 'Variant',
    'diminutives': 'Diminutive',
    'alternatives': 'Other Language',
}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="BehindTheName parser script",
    )
    parser.add_argument(
        'username',
        help="Username to search",
    )
    parser.add_argument(
        'mode',
        choices=list(TYPES.keys()),
        help="Similar usernames search mode",
    )
    args = parser.parse_args()

    username = args.username

    response = requests.get(URL.format(username=username), headers=HEADERS)
    if response.status_code != 200:
        sys.exit(f'BehindTheName has no page for {username} (HTTP {response.status_code})')
    soup = BS(response.text, 'html.parser')

    # titles are singular when there is only one name: "Variant" vs "Variants"
    title = soup.find('span', string=lambda s: s and s.startswith(TYPES[args.mode]))
    if not title:
        sys.exit(f'BehindTheName has no {args.mode} for {username}')

    names = [a.text for a in title.parent.find_all('a')]

    print('\n'.join(names))
