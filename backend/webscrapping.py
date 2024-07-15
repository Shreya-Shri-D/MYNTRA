import os
import urllib.request
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re

def scrape_myntra_data(base_url, num_pages, driver_path, save_dir):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    # Create lists to store the data from scraping
    brand_name = []
    summary = []
    size = []
    price = []
    product_images = []

    # Run the loop to retrieve data and store data as DataFrame
    for page in range(1, num_pages + 1):
        driver.get(base_url + '?p=' + str(page))
        driver.maximize_window()

        product_brands = driver.find_elements(By.CLASS_NAME, "product-brand")
        product_summaries = driver.find_elements(By.CLASS_NAME, "product-product")
        product_sizes = driver.find_elements(By.CLASS_NAME, "product-sizes")
        product_prices = driver.find_elements(By.CLASS_NAME, "product-price")
        product_images_elements = driver.find_elements(By.CSS_SELECTOR, ".product-base img")

        # Ensure all lists have the same length before accessing elements
        min_length = min(len(product_brands), len(product_summaries), len(product_sizes), len(product_prices), len(product_images_elements))

        for i in range(min_length):
            brand_name.append(product_brands[i].text)
            summary.append(product_summaries[i].text)
            size.append(product_sizes[i].get_attribute('innerText')[7:])
            price.append(product_prices[i].text)
            product_images.append(product_images_elements[i].get_attribute('src'))

        print(f'Page no: {page} completed')

    driver.quit()

    # Save images
    images_dir = os.path.join(save_dir, "images")
    if not os.path.exists(images_dir):
        os.makedirs(images_dir)
    
    for product, img_url in zip(summary, product_images):
        sanitized_product_name = re.sub(r'[\\/*?:"<>|]', "", product)
        urllib.request.urlretrieve(img_url, os.path.join(images_dir, f"{sanitized_product_name}.jpg"))

   
# Usage example
scrape_myntra_data(
    base_url='https://www.myntra.com/men-tshirts',
    num_pages=2,
    driver_path='D:\chromedriver-win64\chromedriver.exe',
    save_dir='C:/Users/SHREYA/Desktop/Myntra Fashion/frontend/'
)
scrape_myntra_data(
    base_url='https://www.myntra.com/saree',
    num_pages=2,
    driver_path='D:\chromedriver-win64\chromedriver.exe',
    save_dir='C:/Users/SHREYA/Desktop/Myntra Fashion/frontend/'
)
scrape_myntra_data(
    base_url='https://www.myntra.com/women-kurtas-kurtis-suits',
    num_pages=2,
    driver_path='D:\chromedriver-win64\chromedriver.exe',
    save_dir='C:/Users/SHREYA/Desktop/Myntra Fashion/frontend/'
)
scrape_myntra_data(
    base_url='https://www.myntra.com/women-jeans',
    num_pages=2,
    driver_path='D:\chromedriver-win64\chromedriver.exe',
    save_dir='C:/Users/SHREYA/Desktop/Myntra Fashion/frontend/'
)
