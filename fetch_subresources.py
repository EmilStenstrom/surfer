import re
import urlparse
import requests

def run(response):
    responses = []

    content = response.content

    # Remove conditional comments to avoice fetching IE stuff
    content = re.sub(r"(<!--.*?-->)", "", content, flags=re.DOTALL)

    # Assume first <link rel="stylesheet" href=""> is the one we want
    link_match = re.search(r'<link rel="stylesheet"[^>]+href="([^"]+)">', content)
    if link_match:
        link_url = urlparse.urljoin(response.url, link_match.group(1))
        responses += [requests.get(link_url)]

    # Assume first <script src=""> is the one we want
    script_match = re.search(r'<script[^>]+src="([^"]+)">', content)
    if script_match:
        script_url = urlparse.urljoin(response.url, script_match.group(1))
        responses += [requests.get(script_url)]

    return responses
