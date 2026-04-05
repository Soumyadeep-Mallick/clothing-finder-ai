import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_flipkart(query):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")

    driver = uc.Chrome(options=options, version_main=146)
    driver.get(f"https://www.flipkart.com/search?q={query}")
    time.sleep(3)

    products = []
    items = driver.find_elements(By.XPATH, "//div[@data-id]")

    for item in items:
        try:
            text = item.text.split("\n")
            title = text[0]

            price = None
            for t in text:
                if "₹" in t and "off" not in t.lower():
                    price = t
                    break

            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

            try:
                image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image = None

            if title and price:
                products.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "image": image,
                    "source": "Flipkart"
                })

        except:
            continue

    driver.quit()
    return products