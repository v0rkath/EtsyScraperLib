from store import Store
from product import Product

product = Product("https://www.etsy.com/uk/listing/1310127372/build-your-own-bullet-resin-board")
product.connect()

product.get_description()
product.get_review_quantity()
print(product.review_quantity)
