import pandas as pd

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

import warnings
warnings.filterwarnings("ignore")


def start_driver():

    # specifies the path to the chromedriver.exe
    driver = webdriver.Chrome(
        "C:\\Users\\nick.sieraad\\Documents\\Projects\\match-private-labels-maxaro\\executables\\chromedriver.exe"
    )

    # opens chrome in full screen
    driver.maximize_window()

    # navigates to website competitor
    driver.get("https://www.maxaro.nl/")

    return driver


def wait(selector, element, driver):
    # Function that waits till element is detected
    delay = 10
    try:
        WebDriverWait(driver, delay).until(ec.presence_of_element_located((selector, element)))
    except TimeoutException:
        print("wait Loading took too much time!")


def get_product_specs(driver, product_urls):

    max_dict = {}
    for url in product_urls["product_url"][:3]:
        driver.get(url)

        art_nr = driver.find_elements_by_class_name("product-header__sub")[1].text
        max_dict[art_nr] = {}
        max_dict[art_nr]["URL"] = url
        max_dict[art_nr]["Name"] = driver.find_elements_by_class_name("product-header__title")[1].text

        wait(By.CLASS_NAME, "breadcrumbs", driver)
        breadcrumbs = driver.find_element_by_class_name("breadcrumbs").text.split("\n")
        if len(breadcrumbs) == 4:
            max_dict[art_nr]["Sub category"] = breadcrumbs[-2]
        else:
            max_dict[art_nr]["Sub category"] = ""

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        wait(By.CLASS_NAME, "product-detail-section__show-more", driver)
        driver.find_elements_by_class_name("product-detail-section__show-more")[1].click()
        wait(By.CLASS_NAME, "product-detail-specifications__key", driver)
        keys = driver.find_elements_by_class_name("product-detail-specifications__key")
        values = driver.find_elements_by_class_name("product-specification-value")

        for key, value in zip(keys, values):
            max_dict[art_nr][key.text] = value.text

        return max_dict


def create_dataframe(max_dict):

    df = pd.DataFrame.from_dict(max_dict)
    maxaro_product_specs = df.T.reset_index(0).rename(columns={'index': 'Art. nr. Maxaro'})
    maxaro_product_specs.to_csv('Maxaro_assortment_product_specs_new.csv')


def main(product_urls):

    driver = start_driver()
    max_dict = get_product_specs(driver, product_urls)
    create_dataframe(max_dict)


if __name__ == '__main__':
    main()
