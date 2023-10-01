
<p align="center">
  <img width="600" height="180" src="https://i.imgur.com/86M0L8W.png">
</p>
<p align="center">
A versatile Python package crafted with the BeautifulSoup4, Requests, and JSON libraries. With just a few lines of Python code, the scraper can seamlessly extract comprehensive data from any Etsy store. Retrieve essential information such as product listings, pricing, descriptions and seller details.
</p>

# Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install EtsyScraperLib.
```bash
pip install EtsyScraperLib
```

## Usage: Store Data
```python
from EtsyScraperLib import Store

a_store = Store('TempStore') # name of the store
a_store.connect() # get html from the store page

a_store.get_description() # returns a string of the store description.
a_store.get_location() # returns a string of the store location.
a_store.get_logo() # returns a string of the store logo URL.
a_store.get_banner() # returns a string of the store banner URL.
a_store.get_sales_quantity() # returns an int of the sales quantity
a_store.get_product_quantity() # returns an int of the product quantity.
a_store.get_admirers() # returns an int of the quantity of store admirers.
a_store.parse_product_urls() # returns a list of product URLs.
a_store.parse_product_titles() # returns a list of product titles.
a_store.parse_product_prices() # returns a list of product prices.
a_store.get_review_rating() # returns a float of the store's review rating.
a_store.get_review_quantity() # returns an int of the quantity of reviews.
a_store.get_all_data() # collects all of the above data and places it in the object's members. This is intended to be used with the below function.
a_store.generate_json() # will generate JSON depending on the data you've collected.
```

### JSON Output
```python
from EtsyScraperLib import Store

a_store = Store('TempStore')
a_store.connect()

a_store.get_all_data()
print(a_store.generate_json())

##### Output #####

{
    "storeName": "TempStore",
    "storeDescription": "",
    "storeLocation": "London, United Kingdom",
    "storeLogo": "https://i.etsystatic.com/isla/999999/99999999/isla_180x180.66383585_elel5og3.jpg?version=0",
    "storeBannerImage": "Banner couldn't be found.",
    "storeProductQuantity": 2,
    "storeSalesQuantity": 0,
    "storeAdmirers": 1,
    "storeReviewQuantity": 0,
    "storeReviewRating": 0.0,
    "storeProductDetails": [
        {
            "produceTitle": "Item Title 1",
            "productURL": "https://www.etsy.com/listing/1573434449/item-title-1",
            "productPrice": "$19.16"
        },
        {
            "produceTitle": "Item Title 2",
            "productURL": "https://www.etsy.com/listing/1559244379/item-title-2",
            "productPrice": "$47.92"
        }
    ]
}
```

## Usage: Product Data
```python
from EtsyScraperLib import Product

a_product = Product('https://www.etsy.com/uk/listing/1479000279/item-title-1') # URL of the product
a_product.connect() # get html from the product page

a_product.get_title() # returns a string of the product title.
a_product.get_description() # returns a string of the product description.
a_product.get_price() # returns a string of the product price.
a_product.get_review_quantity() # returns an int of the quantity of reviews.
a_product.parse_media() # returns a list of image & video URLs
a_product.get_all_data() # collects all of the above data and places it in the object's members. This is intended to be used with the below function.
```

```python
from EtsyScraperLib import Product

a_product = Product('https://www.etsy.com/uk/listing/1479000279/item-title-1') 
a_product.connect() 

a_product.get_all_data()
print(a_product.generate_json())

##### Output #####
{
    "productName": "Item Title 1",
    "productDescription": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin velit turpis, vehicula eu interdum eu, dignissim quis risus. Duis ultricies purus a dapibus elementum. Vivamus risus erat, imperdiet vitae urna et, dictum tempus dolor. Aliquam felis eros, feugiat vitae neque in, rhoncus vestibulum libero. Suspendisse quis purus sit amet felis malesuada rhoncus eget vitae nulla. Mauris efficitur nunc in facilisis suscipit. Pellentesque in magna eget velit eleifend ultrices. Maecenas malesuada leo risus, id pellentesque nisl aliquet sit amet.",
    "productPrice": "$314.99",
    "productReviews": 0,
    "media": [
        "https://i.etsystatic.com/39539439/r/il/455858/5323849019/il_1588xN.5323848888.jpg",
        "https://i.etsystatic.com/39539439/r/il/26f969/5372017159/il_1588xN.5372018888.jpg",
        "https://i.etsystatic.com/39539439/r/il/6f0539/5323848409/il_1588xN.5323848888.jpg"
    ]
}

```


## License

[MIT](https://choosealicense.com/licenses/mit/)

## Todo
- Include `async` for getting all data to increase speed.
- Code needs a good bit of tidying up.
