from bs4 import BeautifulSoup
import requests
import json
import re
from typing import List, Union
from text_format import format_title, format_description

class Product:
    # Product info
    title: str = ''
    price: str = ''
    description: str = ''
    review_quantity: int = 0
    media_urls: List[str] = []
    
    # Beautiful Soup info
    soup: str = ''


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
            page_html = request.text
            self.soup = BeautifulSoup(page_html, 'html.parser')

        except requests.exceptions.RequestException as e:
            print('[!] Request failed', e)
    

    def get_title(self):
        """
        Extract the title of the product.
        """
        try:
            self.title = format_title(self.soup.title.text)
        except AttributeError:
            print('[AttributeError]: Title couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')

    
    def get_description(self):
        """
        Extract the description of the product. 
        """
        try:
            description_toggle = self.soup.find('div', {'id': 'wt-content-toggle-product-details-read-more'})
            paragraph = description_toggle.find('p').text
            self.description = format_description(paragraph)
        except AttributeError:
            print('[AttributeError]: Description couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')


    def get_price(self):
        """
        Extract the price of the product.
        """
        try:
            price_box = self.soup.find('div', {'data-buy-box-region': 'price'})
            price = price_box.find('p', {'class': re.compile(r'\btitle\b', re.I)})
            format_price = price.text.replace('Price:', '').strip()
            self.price = format_price
        except AttributeError:
            print('[AttributeError]: Price couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')


    def get_review_quantity(self):
        """
        Extract the quantity of reviews for this product.
        """
        try:
            review_quantity = self.soup.find('span', {'class': 'wt-badge--statusInformational'})
            self.review_quantity = int(review_quantity.text.lstrip().rstrip())
        except AttributeError:
            print('[AttributeError]: Reviews couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
            

    def __parse_images(self, li: str):
        """
        Parse through the product images and add to the media list.
        Args:
            li: The li element for the media.
        """
        try:
            image = li.find('img', {'class': 'carousel-image'})
            if image is not None and 'srcset' in image.attrs:
                links = image['srcset']
                split_urls = links.split(',')

                for url in split_urls:
                    if '2x' in url:
                        url = url.strip().split(' ')[0]
                        self.media_urls.append(url)
        except AttributeError:
            print(f'[AttributeError]: Images couldn\'t be parsed.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')


    def __parse_videos(self, li:str):
        """
        Parse through the product videos and add to the media list.
        Args:
            The li element for the media.
        """
        try:
            video = li.find('video')
            if video is not None:
                source = video.find('source').get('src')
                self.media.append(source)
        except AttributeError:
            print('[AttributeError]: Videos couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')


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
            print(f'[Error Occurred]: {e}')


    def get_all_data(self):
        """
        Get all data from the store.
        """
        print("[?] Collecting product data, this may take a few seconds...")
        self.get_title()
        self.get_description()
        self.get_price()
        self.get_review_quantity()
        self.parse_media()

    
    def generate_json(self):
        """
        Formats product data into JSON.
        Returns:
            JSON formatted store data.
        """
        product_data = {
            'productName': self.title,
            'productDescription': self.description,
            'productPrice': self.price,
            'productReviews': self.review_quantity,
            'media': self.media_urls
        }

        json_data = json.dumps(product_data, indent=4)

        return json_data