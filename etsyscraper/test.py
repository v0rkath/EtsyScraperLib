from store import Store
from product import Product

# product = Product("https://www.etsy.com/uk/listing/1310127372/build-your-own-bullet-resin-board")
# product.connect()

store = Store("AustinAsh34")
store.connect()

store.get_admirers()
store.get_product_quantity()
#print(store.product_quantity)