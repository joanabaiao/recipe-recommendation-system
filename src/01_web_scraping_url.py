import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import os
from constants import *


def get_html_content(url, save=False):
    response = requests.get(url)
    if response.status_code == 200:
        if save:
            file_path = os.path.join(HTML_DIR, "website_content.html")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(response.text)
                print(f"Recipes HTML page saved to {file_path}")

        return response.content
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return None


def extract_recipe_urls(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    script_tags = soup.find_all("script", type="application/ld+json")

    recipe_urls = []

    for tag in script_tags:
        try:
            json_data = json.loads(tag.string)
            if json_data.get("@type") == "ItemList":
                for item in json_data["itemListElement"]:
                    if item.get("@type") == "ListItem" and "url" in item:
                        recipe_urls.append(item["url"])
        except (json.JSONDecodeError, KeyError):
            continue

    return recipe_urls


def save_urls_to_file(urls, file_path):
    df = pd.DataFrame({"recipe_urls": urls})
    df.to_csv(file_path, index=False, encoding="utf-8")
    print(f"URLs saved to {file_path}")


################################################################


def main():
    html_content = get_html_content(BASE_URL, save=True)

    if html_content:
        recipe_urls = extract_recipe_urls(html_content)
        save_urls_to_file(recipe_urls, file_path=URLS_PATH)


if __name__ == "__main__":
    main()
