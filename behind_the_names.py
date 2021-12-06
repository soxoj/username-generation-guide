#!/usr/bin/env python3
import argparse
import requests
from bs4 import BeautifulSoup as BS

URL = 'https://www.behindthename.com/name/{username}'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36',
}
TYPES = {
    'variants': 'Variants',
    'diminutives': 'Diminutives',
    'alternatives': 'Other Languages & Cultures',
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

    html = requests.get(URL.format(username=username), headers=HEADERS).text
    soup = BS(html, 'html.parser')

    parent = soup.find('span', string=TYPES[args.mode]).parent

    names = [a.text for a in parent.find_all('a')]

    print('\n'.join(names))
