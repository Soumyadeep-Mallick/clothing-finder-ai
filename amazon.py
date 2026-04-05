import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_amazon(query):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")

    driver = uc.Chrome(options=options, version_main=146)
    driver.get(f"https://www.amazon.in/s?k={query}")
    time.sleep(3)

    products = []
    items = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")

    for item in items:
        try:
            title = item.find_element(By.TAG_NAME, "h2").text
            price = item.find_element(By.CLASS_NAME, "a-price-whole").text
            link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

            try:
                image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image = None

            products.append({
                "title": title,
                "price": f"₹{price}",
                "link": link,
                "image": image,
                "source": "Amazon"
            })

        except:
            continue

    driver.quit()
    return products