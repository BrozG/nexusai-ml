import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

base_url = "https://smit.smu.edu.in/"

visited = set()
to_visit = [base_url]

data = []

def clean_text(soup):

    # remove unwanted elements
    for tag in soup(["script","style","nav","footer","header","aside","form"]):
        tag.extract()

    text = soup.get_text(separator=" ")

    # remove extra spaces
    text = " ".join(text.split())

    return text


while to_visit:

    url = to_visit.pop(0)

    if url in visited:
        continue

    visited.add(url)

    print("Scraping:", url)

    try:
        response = requests.get(url, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        text = clean_text(soup)

        if len(text) > 300:

            data.append({
                "url": url,
                "text": text
            })

        # collect internal links
        for link in soup.find_all("a", href=True):

            full_link = urljoin(base_url, link["href"])

            if base_url in full_link and full_link not in visited:
                to_visit.append(full_link)

    except:
        print("Error:", url)


print("Total pages scraped:", len(data))

with open("smit_raw_text.json","w",encoding="utf-8") as f:
    json.dump(data,f,indent=2)

print("Scraping completed.")