import requests
from bs4 import BeautifulSoup


def get_html_content(url, save=False):
    response = requests.get(url)
    if response.status_code == 200:
        if save:  
            with open("data/website_recipe.html", 'w', encoding='utf-8') as f:
                f.write(response.text)
                    
        return response.content
    else:
        print(f"Failed to retrieve content. Status code: {response.status_code}")
        return None

