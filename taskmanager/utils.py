from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class CoinMarketCap:
    BASE_URL = "https://coinmarketcap.com/currencies/"

    def __init__(self, coin):
        self.coin = coin
        self.driver = webdriver.Firefox()

    def fetch_data(self):
        url = f"{self.BASE_URL}{self.coin}/"
        self.driver.get(url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        error_elements = self.driver.find_elements(By.CSS_SELECTOR, "div.sc-404__StyledError-ic5ef7-0")
        if error_elements:
            return {"data": None} 
        
        #Scraping for Price

        price = self.driver.find_element(By.ID, "section-coin-overview").find_element(By.XPATH, '//div[contains(@class, "sc-d1ede7e3-0") and contains(@class, "gNSoet") and contains(@class, "flexStart") and contains(@class, "alignBaseline")]').find_element(By.CSS_SELECTOR, "span.sc-d1ede7e3-0").text
        price_float = float(price.replace('$', '').replace(',', ''))

        #Scraping for Change Rate

        change_rate_element = self.driver.find_element(By.ID, "section-coin-overview").find_element(By.XPATH, '//div[contains(@class, "sc-d1ede7e3-0") and contains(@class, "gNSoet") and contains(@class, "flexStart") and contains(@class, "alignBaseline")]').find_element(By.CSS_SELECTOR, "div.sc-d1ede7e3-0").find_element(By.XPATH, '//div[@data-sensors-click="true"]//p')
        text = change_rate_element.text
        color = change_rate_element.get_attribute('color')
        change_rate_text = text.split('(')[0].strip()
        change_rate_float = float(change_rate_text.replace('%', ''))

        if color == 'green':
            change_rate_float = change_rate_float

        else:
            change_rate_float = -change_rate_float

        #Scraping for Stats

        stats_div = self.driver.find_element(By.ID, "section-coin-stats").find_element(By.CSS_SELECTOR, "div.sc-d1ede7e3-0").find_elements(By.CSS_SELECTOR, "div.sc-d1ede7e3-0")

        for div in stats_div:
            dt_elements = div.find_elements(By.TAG_NAME, "dt")
            dd_elements = div.find_elements(By.TAG_NAME, "dd")

            for dt, dd in zip(dt_elements, dd_elements):
                label = dt.text.strip()
                value = dd.text.strip()

                if label == "Market cap":
                    market_cap = value.split('\n')[1].replace(',', '').replace('$', '')
                elif label == "Volume (24h)":
                    volume_24h = value.split('\n')[1].replace(',', '').replace('$', '')
                elif label == "Volume/Market cap (24h)":
                    volume_market_cap_24h = float(value.replace('%', ''))
                elif label == "Circulating supply":
                    circulating_supply = value.replace(' BTC', '')
                elif label == "Total supply":
                    total_supply = value.replace(' BTC', '')
                elif label == "Max. supply":
                    max_supply = value.replace(' BTC', '')
                elif label == "Fully diluted market cap":
                    fully_diluted_market_cap = value.replace(',', '').replace('$', '')

        #Stats Data

        stats = {
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "volume_market_cap_24h": volume_market_cap_24h,
            "circulating_supply": circulating_supply,
            "total_supply": total_supply,
            "max_supply": max_supply,
            "fully_diluted_market_cap": fully_diluted_market_cap
        }


        #Scraping for Links

        link_div = self.driver.find_element(By.XPATH, '//div[@class="sc-d1ede7e3-0 cvkYMS coin-info-links"]')

        links = {}

        for sub_div in link_div.find_elements(By.XPATH, './/div[@data-role="stats-block"]'):
            header_div = sub_div.find_element(By.XPATH, './/div[@data-role="header"]')
            header_text = header_div.find_element(By.TAG_NAME, 'span').text

            body_div = sub_div.find_element(By.XPATH, './/div[@data-role="body"]')

            body_links = {}

            for link_div in body_div.find_elements(By.XPATH, './/a'):
                link_text = link_div.text
                link_href = link_div.get_attribute('href')
                body_links[link_text] = link_href

            links[header_text] = body_links

        links = {k: v for k, v in links.items() if v}


        return {
            "price": price_float,
            "change_rate": change_rate_float,
            "stats": stats,
            "links": links
        }