from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import csv

def extract_reviews(product_id, output_file='./reviews.csv'):
    # Initialize the Chrome WebDriver
    driver_path = "./node_modules/chromedriver/lib/chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(service=Service(driver_path))
    
    # Open the Myntra product review page
    url = f'https://www.myntra.com/reviews/{product_id}'
    driver.get(url)
    
    try:
        # Open a file to store reviews
        with open(output_file, 'a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Review'])  # Header for the CSV file

            while True:
                # Find elements containing reviews
                reviews_elements = driver.find_elements(By.CLASS_NAME, "user-review-reviewTextWrapper")
                ratings_elements = driver.find_elements(By.CLASS_NAME, "user-review-rating")  # Class for ratings

                # Extract and write reviews and ratings
                for review_element in reviews_elements:
                    review_text = review_element.text.strip()
                    rating = "Not Available"  # Default value if rating is not available
                    try:
                        # Find the corresponding rating for this review
                        index = reviews_elements.index(review_element)
                        rating_element = ratings_elements[index]
                        rating = rating_element.text.strip()
                    except IndexError:
                        # Handle the case where rating is not available
                        pass
                    
                    if review_text:  # Check if review text is not empty
                        cleaned_review = clean_text(review_text)  # Clean the review text
                        writer.writerow([cleaned_review])  # Write each cleaned review and rating to a new line in the file

                # Scroll down to load more reviews
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Check if we have reached the end of the page
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the browser window
        driver.quit()

def clean_text(text):
    # Remove special characters and punctuation
    text = re.sub(r"[^\w\s]", " ", text)

    # Remove single characters
    text = re.sub(r"\b[a-zA-Z]\b", " ", text)

    # Remove HTML tags
    text = re.sub(r"<[^>]*>", " ", text)

    # Lowercase the text
    text = text.lower()

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    # Trim leading and trailing spaces
    text = text.strip()

    return text
