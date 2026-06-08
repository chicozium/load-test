import xml.etree.ElementTree as ET
import requests
from urllib.parse import urljoin, urlparse
from html.parser import HTMLParser
from locust import HttpUser, task, constant

NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

def parse_sitemap(url, base_url):
    urls = []
    try:
        r = requests.get(url, timeout=5)
        root = ET.fromstring(r.content)
        for sitemap in root.findall("sm:sitemap/sm:loc", NS):
            urls += parse_sitemap(sitemap.text, base_url)
        for loc in root.findall("sm:url/sm:loc", NS):
            path = loc.text.replace(base_url, "") or "/"
            urls.append(path)
    except Exception:
        pass
    return urls

class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            for attr, val in attrs:
                if attr == "href" and val:
                    self.links.append(val)

def crawl(base_url, max_pages=100):
    visited, queue = set(), ["/"]
    while queue and len(visited) < max_pages:
        path = queue.pop(0)
        if path in visited:
            continue
        visited.add(path)
        try:
            r = requests.get(urljoin(base_url, path), timeout=5)
            parser = LinkParser()
            parser.feed(r.text)
            for link in parser.links:
                parsed = urlparse(link)
                if not parsed.netloc or parsed.netloc in base_url:
                    p = parsed.path or "/"
                    if p not in visited:
                        queue.append(p)
        except Exception:
            pass
    print(f"[CRAWL] {len(visited)} pages trouvées")
    return list(visited)

import os
BASE_URL = os.getenv("TARGET_URL", "https://ton-site.com")

def get_all_urls():
    urls = set()
    # sitemap
    for path in ["/sitemap_index.xml", "/sitemap.xml"]:
        found = parse_sitemap(f"{BASE_URL}{path}", BASE_URL)
        urls.update(found)
        if found:
            break
    # crawl HTML
    urls.update(crawl(BASE_URL))
    return list(urls) or ["/"]

URLS = get_all_urls()
print(f"[INFO] {len(URLS)} URLs totales trouvées")

class MonSite(HttpUser):
    wait_time = constant(0)
    connection_timeout = 1
    network_timeout = 1
    host = BASE_URL
    _index = 0

    @task
    def parcourir(self):
        url = URLS[MonSite._index % len(URLS)]
        MonSite._index += 1
        with self.client.get(url, timeout=1, catch_response=True) as r:
            r.success()
