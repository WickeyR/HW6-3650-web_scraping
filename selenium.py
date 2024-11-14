from parsel import Selector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set options to run in headless mode and disable image loading
options = Options()
options.headless = False
options.add_argument("--window-size=1920,1080")
options.add_argument("start-maximized")
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

# Create the driver variable to scrape Chrome
driver = webdriver.Chrome(options=options)

try:
    # Set the website for the driver to load
    driver.get("https://twitch.tv/directory/game/Art")

    # Wait for the page to fully load by waiting for a specific element
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-target="directory-first-item"]'))
    )

    # Parse the page source with Parsel
    sel = Selector(text=driver.page_source)

    # Stores all data parsed in selector
    parsed = []

    # Loop through each item in the specified selector and extract data
    for item in sel.xpath("//div[contains(@class,'tw-tower')]/div[@data-target]"):
        parsed.append({
            'title': item.css('h3::text').get(),
            'url': item.css('.tw-link::attr(href)').get(),
            'username': item.css('.tw-link::text').get(),
            'tags': item.css('.tw-tag ::text').getall(),
            'viewers': ''.join(item.css('.tw-media-card-stat::text').re(r'(\d+)')),
        })

    # Output the parsed data
    print(parsed)

finally:
    # Quit the driver after scraping
    driver.quit()
