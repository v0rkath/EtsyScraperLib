from bs4 import BeautifulSoup
import requests
from typing import List


class Store:
    # Store Info
    store_name: str = ""
    store_description: str = ""
    store_location: str = ""
    store_logo: str = ""
    store_banner: str = ""
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


    def get_description(self):
        """
        Get the description of the store.
        """
        description = self.soup.find("p", {"class": "wt-text-caption wt-hide-xs wt-show-lg wt-wrap wt-break-all"})
        self.store_description = description.text.rstrip()


    def get_location(self):
        """
        Get the location of the store.
        """
        location = self.soup.find("span", {"class": "shop-location"})
        self.store_location = location.text


    def get_logo(self):
        """
        Get the store logo url.
        """
        logo = self.soup.find("img", {"class": "shop-icon-external"})
        self.store_logo = logo.get('src')


    def get_banner(self):
        """
        Get the store banner url.
        """
        banner = self.soup.find("img", {"class": "wt-position-absolute wt-display-block fill-min-height wt-width-full"})
        self.store_banner = banner.get('src')


    def get_sales_quantity(self):
        """
        Extract the amount of sales the store has had.
        """
        review_band = self.soup.find("div", {"class": "shop-sales-reviews"})
        span = review_band.find("span", {"class": "wt-text-caption wt-no-wrap"})
        a = span.find("a")
        self.sales_quantity = a.text.replace(" Sales", "")


    def get_product_quantity(self):
        """
        Extract the amount of products for sale by the store.
        """
        side_bar = self.soup.find("div", {"class": "shop-home-wider-sections"})
        div = side_bar.find("div", {"class": "wt-tab-container"})
        button = div.find("button")
        span = button.find("span", {"class": "wt-mr-md-2"})
        self.product_quantity = span.text


    def __get_page_quantity(self) -> int:
        """
        Get the amount of pages of products.
        Returns:
            Integer of the number of product pages.
        """
        pagination = self.soup.find("div", {"class": "wt-show-xl"})
        buttons = pagination.find_all("li", class_="wt-action-group__item-container")

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


    def parse_product_url(self):
        """
        Parse every url of each product from the store.
        """
        base_url = self.store_url + "?page="
        page_quantity = self.__get_page_quantity()

        i = 1
        while i <= page_quantity:
            request = requests.get(base_url + str(i))
            html = request.text
            page_soup = BeautifulSoup(html, "html.parser")
            listings = page_soup.find("div", {"class": "responsive-listing-grid"})
            listing_links = listings.find_all("a", {"class": "listing-link"})
            for product in listing_links:
                self.product_urls.append(product["href"])

            i += 1