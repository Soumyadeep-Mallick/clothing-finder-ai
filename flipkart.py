import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time

def scrape_flipkart(query):

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--disable-blink-features=AutomationControlled")

    # ✅ FORCE VERSION MATCH (146)
    driver = uc.Chrome(
        options=options,
        version_main=146,
        use_subprocess=True
    )

    products = []

    try:
        url = f"https://www.flipkart.com/search?q={query}"
        driver.get(url)
        time.sleep(3)

        items = driver.find_elements(By.CSS_SELECTOR, "div._1AtVbE")[:10]

        for item in items:
            try:
                title = item.find_element(By.CSS_SELECTOR, "a.IRpwTa").text
                price = item.find_element(By.CSS_SELECTOR, "div._30jeq3").text
                link = item.find_element(By.TAG_NAME, "a").get_attribute("href")

                try:
                    image = item.find_element(By.TAG_NAME, "img").get_attribute("src")
                except:
                    image = None

                products.append({
                    "title": title,
                    "price": price,
                    "link": link,
                    "image": image,
                    "source": "Flipkart"
                })

            except:
                continue

    finally:
        driver.quit()

    return products