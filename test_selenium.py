import undetected_chromedriver as uc
import time

# Force match with your Chrome version
driver = uc.Chrome(version_main=146)

driver.get("https://www.google.com")

time.sleep(30)

driver.quit()