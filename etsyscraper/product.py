from bs4 import BeautifulSoup
import requests
from typing import List, Union
from text_format import format_title, format_description

class Product:
    # Product info
    page_html: str = ""
    product_title: str = ''
    description: str = ""
    review_quantity: int = 0
    
    # Beautiful Soup info
    soup: str = ""


    def __init__(self, product_url: str):
        """
        Sets up the product you want to scrape data from.
        Args:
            product_url: The URL of the product you want to scrape data from.
        """
        self.product_url = product_url

    
    def connect(self):
        """
        Issue a GET request to the Etsy store to retrieve the HTML data.
        """
        try:
            request = requests.get(self.product_url)
            request.raise_for_status()  # checks for non-2xx status codes

            print("[?] Request was successful.")
            self.page_html = request.text
            self.soup = BeautifulSoup(self.page_html, "html.parser")

        except requests.exceptions.RequestException as e:
            print("[!] Request failed", e)
    

    def get_title(self):
        """
        Extract the title of the product.
        """
        self.product_title = format_title(self.soup.title.text)

    
    def get_description(self):
        """
        Extract the description of the product. 
        """
        description_toggle = self.soup.find("div", {"id": "wt-content-toggle-product-details-read-more"})
        paragraph = description_toggle.find("p").text

        self.description = format_description(paragraph)


    def get_review_quantity(self):
        """
        Extract the quantity of reviews for this product.
        """
        review_quantity = self.soup.find("span", {"class": "wt-badge--statusInformational"})
        self.review_quantity = int(review_quantity.text.lstrip().rstrip())

        