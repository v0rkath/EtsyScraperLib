from bs4 import BeautifulSoup
import requests
from typing import List, Union
from text_format import format_title, format_description

class Product:
    # Product info
    page_html: str = ''
    product_title: str = ''
    description: str = ''
    review_quantity: int = 0
    media_urls: List[str] = []
    
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

            print('[?] Request was successful.')
            self.page_html = request.text
            self.soup = BeautifulSoup(self.page_html, 'html.parser')

        except requests.exceptions.RequestException as e:
            print('[!] Request failed', e)
    

    def get_title(self):
        """
        Extract the title of the product.
        """
        self.product_title = format_title(self.soup.title.text)

    
    def get_description(self):
        """
        Extract the description of the product. 
        """
        description_toggle = self.soup.find('div', {'d': 'wt-content-toggle-product-details-read-more'})
        paragraph = description_toggle.find('p').text

        self.description = format_description(paragraph)


    def get_review_quantity(self):
        """
        Extract the quantity of reviews for this product.
        """
        review_quantity = self.soup.find('span', {'class': 'wt-badge--statusInformational'})
        self.review_quantity = int(review_quantity.text.lstrip().rstrip())


    def __parse_images(self, li: str):
        """
        Parse through the product images and add to the media list.
        Args:
            li: The li element for the media.
        """
        image = li.find('img', {'class': 'carousel-image'})
        if image is not None and 'srcset' in image.attrs:
            links = image['srcset']
            split_urls = links.split(',')

            for url in split_urls:
                if '2x' in url:
                    url = url.strip().split(' ')[0]
                    self.media_urls.append(url)


    def __parse_videos(self, li:str):
        """
        Parse through the product videos and add to the media list.
        Args:
            The li element for the media.
        """
        video = li.find('video')
        if video is not None:
            source = video.find('source').get('src')
            self.media.append(source)


    def parse_media(self):
        """
        Parse the product images & video links (highest quality).
        """
        try:
            ul = self.soup.find('ul', {'class': 'carousel-pane-list'})
            all_li = ul.find_all('li', {'class': 'carousel-pane'})

            for li in all_li:
                self.__parse_images(li)
                self.__parse_videos(li)

        except Exception as e:
            # Handle any exceptions that may occur during parsing
            print(f"An error occurred: {e}")
        
