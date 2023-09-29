from bs4 import BeautifulSoup
import requests
import re
import json
from typing import List


class Store:
    # Store Info
    store_name: str = ''
    store_description: str = ''
    store_location: str = ''
    store_logo: str = ''
    store_banner: str = ''
    store_url: str = ''
    sales_quantity: int = 0
    product_quantity: int = 0
    review_rating: float = 0.0
    review_quantity: int = 0
    admirers: int = 0
    product_titles: List[str] = []
    product_urls: List[str] = []
    product_prices: List[str] = []
    product_details: List[dict] = []


    def __init__(self, store_name: str):
        """
        Sets up which Etsy store you want to scrape data from.
        Args:
            store_name: The name of the store you would like to extract data from e.g. https://www.etsy.com/shop/AustinAsh34 is AustinAsh34
        """
        self.store_name = store_name
        self.store_url = f'https://etsy.com/shop/{self.store_name}'
        self.soup = None


    def connect(self):
        """
        Issue a GET request to the Etsy store to retrieve the HTML data.
        """
        try:
            request = requests.get(self.store_url)
            request.raise_for_status()  # checks for non-2xx status codes

            print('[?] Request was successful.')
            page_html = request.text
            self.soup = BeautifulSoup(page_html, 'html.parser')
        except requests.exceptions.RequestException as e:
            print(f'[Request Failed]: {e}')
        

    def __find_element(self, type: str, attr: str, content: str, fail_value: str = '') -> str:
        """
        Wrapper around the BeautifulSoup4 method 'find()' to carry out exception checks.
        Args:
            type: tag name e.g. span, p, img
            attr: attribute type e.g class, id
            content: info relating to the 'attr'
            fail_value: if try fails then mark relevant member as 'fail_val'
        Returns:
            String of the value retrieved from the element.
        """
        try:
            element = self.soup.find(type, {attr: content})
            return element.text.strip()
        except AttributeError:
            print(f'[AttributeError]: {fail_value}')
            return fail_value
        except Exception as e:
            print(f'[Error Occurred]: {e}')
            return fail_value


    def get_description(self) -> str:
        """
        Get the description of the store.
        Returns:
            String of the store description.
        """
        element = self.__find_element('p', 'class', 'wt-text-caption wt-hide-xs wt-show-lg wt-wrap wt-break-all', 'Description coudn\'t be found.')
        self.store_description = element
        return self.store_description


    def get_location(self) -> str:
        """
        Get the location of the store.
        Returns:
            String of the store location.
        """
        element = self.__find_element('span', 'class', 'shop-location', 'Location couldn\'t be found.')
        self.store_location = element
        return self.store_location


    def get_logo(self) -> str:
        """
        Get the store logo url.
        Returns:
            String of the URL for the store logo.
        """
        try:
            logo = self.soup.find('img', {'class': 'shop-icon-external'})
            self.store_logo = logo.get('src')
        except AttributeError:
            print('Attribute Error: Logo couldn\'t be found.')
            self.store_logo = 'Logo couldn\'t be found.'
        except Exception as e:
            print(f'[Error Occurred]: {e}')
            self.store_logo = 'Logo couldn\'t be found.'
        finally:
            return self.store_logo


    def get_banner(self) -> str:
        """
        Get the store banner url.
        Returns:
            String of the URL for the store banner.
        """
        try:
            banner = self.soup.find('img',{'class': 'wt-position-absolute wt-display-block fill-min-height wt-width-full'})
            self.store_banner = banner.get('src')
        except AttributeError:
            print('[AttributeError]: Banner couldn\'t be found.')
            self.store_banner = 'Banner couldn\'t be found.'
        except Exception as e:
            print(f'[Error Occurred]: {e}')
            self.store_banner = 'Banner couldn\'t be found.'
        finally:
            return self.store_banner


    def get_sales_quantity(self) -> int:
        """
        Extract the amount of sales the store has had.
        Returns:
            Integer of the sales quantity.
        """
        try:
            review_band = self.soup.find('div', {'class': 'shop-sales-reviews'})
            span = review_band.find('span', {'class': 'wt-text-caption wt-no-wrap'})
            self.sales_quantity = int(span.text.replace(' Sales', '').replace(',',''))
        except AttributeError:
            print('[AttributeError]: Sales quantity couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
        finally:
            return self.sales_quantity


    def get_product_quantity(self) -> int:
        """
        Extract the amount of products for sale by the store.
        Returns:
            Integer of the product quantity.
        """
        try:
            side_bar = self.soup.find('div', {'class': 'shop-home-wider-sections'})
            div = side_bar.find('div', {'class': 'wt-tab-container'})
            button = div.find('li', {'class': 'wt-tab__item'})
            span = button.find('span', {'class': 'wt-mr-md-2'})
            self.product_quantity = int(span.text)
        except AttributeError:
            print('[AttributeError]: Product quantity couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
        finally:
            return self.product_quantity


    def __get_page_quantity(self) -> int:
        """
        Get the amount of pages of products.
        Returns:
            Integer of the number of product pages.
        """
        try:
            shop_box = self.soup.find('div', {'class': 'shop-home-wider-items'})
            pagination = shop_box.find('div', {'class': 'wt-show-xl'})
            if pagination:
                buttons = pagination.find_all('li', class_='wt-action-group__item-container')
                if buttons:
                    return int(len(buttons) - 1)
                else:
                    return 0
            return 0
        except AttributeError:
            print('[AttributeError]: Page quantity couldn\'t be found.')
            return 0
        except Exception as e:
            print(f'[Error Occurred]: {e}')
            return 0


    def get_admirers(self) -> int:
        """
        Get the amount of admirers the store has.
        Returns:
            Integer of admirers.
        """
        try:
            shop_sidebar = self.soup.find('div', {'class': 'shop-home-wider-sections'})
            link_section = shop_sidebar.find(lambda tag: tag.name == 'a' and 'favoriters' in tag.get('href', ''))
            text = link_section.text
            format_text = text.replace(' Admirers', '').replace(' Admirer', '')
            self.admirers = int(format_text)
        except AttributeError:
            print('[AttributeError]: Admirers quantity couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
        finally:
            return self.admirers


    def parse_product_urls(self) -> List[str]:
        """
        Parse every url of each product from the store.
        Returns:
            List of product URLs.
        """
        base_url = self.store_url + '?page='
        page_quantity = self.__get_page_quantity()
        if page_quantity < 1:
            page_quantity = 1

        for i in range(1, page_quantity + 1):
            try:
                request = requests.get(base_url + str(i))
                request.raise_for_status()
                html = request.text
                page_soup = BeautifulSoup(html, 'html.parser')
                listings = page_soup.find('div', {'class': 'responsive-listing-grid'})
                listing_links = listings.find_all('a', {'class': 'listing-link'})
                for product in listing_links:
                    self.product_urls.append(product['href'])

            except AttributeError:
                print('[AttributeError]: Product URLs couldn\'t be found.')
            except Exception as e:
                print(f'[Error Occurred]: {e}')
        
        return self.product_urls


    def parse_product_titles(self) -> List[str]:
        """
        Parse the title of each product from the store.
        Returns:
            List of product titles.
        """
        base_url = self.store_url + '?page='
        page_quantity = self.__get_page_quantity()
        if page_quantity < 1:
            page_quantity = 1

        for i in range(1, page_quantity + 1):
            try:
                request = requests.get(base_url + str(i))
                request.raise_for_status()
                html = request.text
                page_soup = BeautifulSoup(html, 'html.parser')
                listings = page_soup.find('div', {'class': 'responsive-listing-grid'})
                listing_titles = listings.find_all('div', {'class': 'v2-listing-card__info'})
                for product in listing_titles:
                    title = product.find('h3').text
                    self.product_titles.append(title.strip())

            except AttributeError:
                print('[AttributeError]: Product titles couldn\'t be found.')
            except Exception as e:
                print(f'[Error Occurred]: {e}')
        
        return self.product_titles


    def parse_product_prices(self) -> List[str]:
        """
        Parse the price of each product from the store.
        Returns:
            List of product prices.
        """
        base_url = self.store_url + '?page='
        page_quantity = self.__get_page_quantity()
        if page_quantity < 1:
            page_quantity = 1

        for i in range(1, page_quantity + 1):
            try:
                request = requests.get(base_url + str(i))
                request.raise_for_status()
                html = request.text
                page_soup = BeautifulSoup(html, 'html.parser')
                listings = page_soup.find('div', {'class': 'responsive-listing-grid'})
                listing_prices = listings.find_all('div', {'class': 'n-listing-card__price'})
                for product in listing_prices:
                    symbol = product.find('span', {'class': 'currency-symbol'})
                    price = product.find('span', {'class': 'currency-value'})

                    self.product_prices.append(symbol.text + price.text)

            except AttributeError:
                print('[AttributeError]: Product prices couldn\'t be found.')
            except Exception as e:
                print(f'[Error Occurred]: {e}')

        return self.product_prices

    
    def __parse_product_details(self):
        """
        Collect all product details from store. This avoids making several rounds of requests to Etsy.
        """
        base_url = self.store_url + '?page='
        page_quantity = self.__get_page_quantity()
        if page_quantity < 1:
            page_quantity = 1
        
        for i in range(1, page_quantity + 1):
            try:
                print(i)
                request = requests.get(f'{base_url}{i}')
                request.raise_for_status() # exception for non-2xx status

                html = request.text
                page_soup = BeautifulSoup(html, 'html.parser')


                listings = page_soup.find('div', {'class': 'responsive-listing-grid'})
                listing_links = listings.find_all('a', {'class': 'listing-link'})
                self.product_urls.extend(product['href'] for product in listing_links)

                listing_titles = listings.find_all('div', {'class': 'v2-listing-card__info'})
                self.product_titles.extend(title.find('h3').text.strip() for title in listing_titles)

                listing_prices = listings.find_all('div', {'class': 'n-listing-card__price'})
                self.product_prices.extend(
                    symbol.text + price.text for price, symbol in ((product.find('span', {'class': 'currency-value'}), 
                                                                    product.find('span', {'class': 'currency-symbol'})) 
                                                                    for product in listing_prices)
                    )

            except requests.exceptions.RequestException as e:
                print(f'[Request Failed]: {e}')
            except AttributeError:
                print('[AttributeError]: Product data couldn\'t be found.')
            except Exception as e:
                print(f'[Error Occurred]: {e}')
        
        self.__product_details_to_dict()

    
    def __product_details_to_dict(self) -> dict:
        """
        Append dictionaries of product details to a list.
        Returns:
            Dictionary of product titles, URLs and price.
        """
        for i in range(len(self.product_titles)):
            data = {}
            data['produceTitle'] = self.product_titles[i]
            data['productURL'] = self.product_urls[i]
            data['productPrice'] = self.product_prices[i]
            self.product_details.append(data)

        return self.product_details


    def get_review_rating(self) -> float:
        """
        Get the the quantity of stars for the store.
        Returns:
            Float of review rating.
        """
        try:
            star_span = self.soup.find('span', {'class': 'stars-svg'})
            self.review_rating = float(star_span.find('input', {'name': 'rating'}).get('value'))
        except AttributeError:
                print('[AttributeError]: Review ratings couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
        finally:
            return self.review_rating


    def get_review_quantity(self) -> int:
        """
        Get the quantity of reviews for the store.
        Returns:
            Integer of review quantity.
        """
        try:
            review_row = self.soup.find('div', {'class': 'reviews-total'})
            content = review_row.find_all('div', {'class': 'wt-display-inline-block'})
            pattern = r'\((.*?)\)'
            match = re.findall(pattern, str(content))

            self.review_quantity = int(match[0])
        except AttributeError:
                print('[AttributeError]: Review quantity couldn\'t be found.')
        except Exception as e:
            print(f'[Error Occurred]: {e}')
        finally:
            return self.review_quantity


    def get_all_data(self):
        """
        Get all data from the store.
        """
        print("[?] Collecting store data, this may take a few seconds...")
        self.get_description()
        self.get_location()
        self.get_logo()
        self.get_banner()
        self.get_sales_quantity()
        self.get_product_quantity()
        self.get_admirers()
        self.__parse_product_details()
        self.get_review_rating()
        self.get_review_quantity()

    
    def generate_json(self) -> str:
        """
        Formats store data into JSON
        Returns:
            JSON formatted store data.
        """
        store_data = {
            'storeName': self.store_name,
            'storeDescription': self.store_description,
            'storeLocation': self.store_location,
            'storeLogo': self.store_logo,
            'storeBannerImage': self.store_banner,
            'storeProductQuantity': self.product_quantity,
            'storeSalesQuantity': self.sales_quantity,
            'storeAdmirers': self.admirers,
            'storeReviewQuantity': self.review_quantity,
            'storeReviewRating': self.review_rating,
            'storeProductDetails': self.product_details
        }

        json_data = json.dumps(store_data, indent=4)

        return json_data