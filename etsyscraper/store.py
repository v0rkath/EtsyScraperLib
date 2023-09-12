from bs4 import BeautifulSoup
import requests
from typing import List
from text_format import format_admirers


class Store:
    # Store Info
    store_name: str = ""
    store_url: str = ""
    page_html: str = ""
    sales_quantity: int = 0
    product_quantity: int = 0
    review_rating: int = 0
    admirers: int = 0
    product_titles: List[str] = []
    product_urls: List[str] = []
    product_prices: List[int] = []

    # Beautiful Soup
    soup: str = ""

    def __init__(self, store_name: str):
        """
        Sets up which Etsy store you want to scrape data from.
        Args:
            store_name: The name of the store you would like to extract data from e.g. https://www.etsy.com/shop/AustinAsh34 is AustinAsh34
        """
        self.store_name = store_name
        self.store_url = f"https://etsy.com/shop/{self.store_name}"


    def connect(self):
        """
        Issue a GET request to the Etsy store to retrieve the HTML data.
        """
        try:
            request = requests.get(self.store_url)
            request.raise_for_status()  # checks for non-2xx status codes

            print("[?] Request was successful.")
            self.page_html = request.text
            self.soup = BeautifulSoup(self.page_html, "html.parser")

        except requests.exceptions.RequestException as e:
            print("[!] Request failed", e)


    def print_html(self):
        """
        Print the HTML from the connection.
        """
        print(self.page_html)


    def get_sales_quantity(self):
        """
        Extract the amount of sales the store has had.
        """
        review_band = self.soup.find("div", {"class": "shop-sales-reviews"})
        span = review_band.find("span", {"class": "wt-text-caption wt-no-wrap"})
        a = span.find("a")
        self.sales_quantity = a.text.replace(" Sales", "")


    def print_sales_quantity(self):
        """
        Print the number of products sold by the store.
        """
        print(self.sales_quantity)


    def get_product_quantity(self):
        """
        Extract the amount of products for sale by the store.
        """
        side_bar = self.soup.find("div", {"class": "shop-home-wider-sections"})
        div = side_bar.find("div", {"class": "wt-tab-container"})
        button = div.find("button")
        span = button.find("span", {"class": "wt-mr-md-2"})
        self.product_quantity = span.text


    def print_product_quantity(self):
        """
        Print the number of products for sale by the store.
        """
        print(self.product_quantity)


    def __get_page_quantity(self) -> int:
        """
        Get the amount of pages of products.
        Returns:
            Integer of the number of product pages.
        """
        pagination = self.soup.find("div", {"class": "wt-show-xl"})
        buttons = pagination.find_all(
            "li", class_="wt-action-group__item-container"
        )

        i = 0
        for button in buttons:
            i += 1

        return i - 1


    def get_admirers(self):
        """
        Get the amount of admirers the store has.
        """
        shop_sidebar = self.soup.find("div", {"class": "shop-home-wider-sections"})
        link_section = shop_sidebar.find(lambda tag: tag.name == "a" and "favoriters" in tag.get("href", ""))
        if link_section:
            text = link_section.text
            format_text = text.replace(" Admirers", "")
            self.admirers = int(format_text)
        else:
            print("No admirers found.")