import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import time

base_url = "https://www.umass.edu/counseling/"

visited_links = set()
linkstosave = set()

def normalize_url(url):
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def get_links(url, depth=0, max_depth=2):
    if depth >= max_depth or url in visited_links:
        return

    try:
        visited_links.add(url)
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        refs = soup.find_all("a", href=True)
        relevant = [urljoin(url, link["href"]) for link in refs if 'counseling' in link['href']]

        for href in relevant:
            normalized = normalize_url(href)
            if normalized not in visited_links:
                print(normalized)
                linkstosave.add(normalized)
                time.sleep(0.3)
                get_links(normalized, depth=depth+1, max_depth=max_depth)

    except Exception as e:
        print(f"Failed to process {url}: {e}")

get_links(base_url)

with open('urls.txt', 'w') as f:
    for link in linkstosave:
        f.write(link.strip() + "\n")

print(f"Total relevant links found: {len(visited_links)}")

