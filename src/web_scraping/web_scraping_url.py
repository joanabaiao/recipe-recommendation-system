from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

from src.constants import *

COOKIE_ACCEPT_BUTTON_XPATH = "//button[contains(span/text(), 'ACCEPT ALL')]"
LOAD_MORE_BUTTON_CSS_SELECTOR = "a.type-button.w-full.astro-b4fc5k6u"
RECIPE_CARD_CSS_SELECTOR = "div.content-grid-item[data-test-id='content_item'] a.card"


#####################################
# ACCEPT COOKIES
#####################################
def accept_cookies(driver):
    try:
        cookie_accept_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, COOKIE_ACCEPT_BUTTON_XPATH))
        )
        cookie_accept_button.click()
        time.sleep(1)
        print("Cookies accepted.")
    except Exception as e:
        print("Error occurred while accepting cookies:", e)


#####################################
# LOAD ALL RECIPES IN PAGE
#####################################
def load_more_recipes(driver):
    try:
        # Wait for the "Load More" button to be visible and clickable using its CSS selector
        load_more_button = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, LOAD_MORE_BUTTON_CSS_SELECTOR)
            )
        )
        load_more_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, "a.type-button.w-full.astro-b4fc5k6u")
            )
        )

        # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)

        # Click the button using JavaScript to bypass any overlay issues
        driver.execute_script("arguments[0].click();", load_more_button)

        time.sleep(3)  # Wait for new recipes to load
        return True
    except Exception as e:
        print("No more recipes or error:", e)
        return False


#####################################
# EXTRACT URL OF ALL RECIPES
#####################################
def extract_recipe_links(driver):
    try:
        recipe_cards = driver.find_elements(By.CSS_SELECTOR, RECIPE_CARD_CSS_SELECTOR)

        recipe_links = [card.get_attribute("href") for card in recipe_cards]

        return recipe_links

    except Exception as e:
        print("Error:", e)
        return []


#####################################
# SAVE CSV FILE WITH URLS
#####################################
def save_urls_to_file(urls, file_path):
    try:
        df = pd.DataFrame({"recipe_urls": urls})
        df.to_csv(file_path, index=False, encoding="utf-8")
        print(f"URLs saved to {file_path}")
    except Exception as e:
        print(f"Error occurred while saving URLs to file: {e}")


################################################################


def main():
    driver = webdriver.Chrome()

    driver.get(BASE_URL)
    accept_cookies(driver)

    while load_more_recipes(driver):
        pass

    recipe_links = extract_recipe_links(driver)

    print(f"Number of recipes extracted: {len(recipe_links)}")
    save_urls_to_file(recipe_links, file_path=URLS_PATH)

    driver.quit()


if __name__ == "__main__":
    main()
