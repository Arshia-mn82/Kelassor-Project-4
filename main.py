import pickle
import os

# Define the path for storing data
DATA_FILE = 'data.pkl'

# Product class to represent individual products
class Product:
    def __init__(self, name, price_range, category, stock):
        self.__name = name
        self.__price_range = price_range
        self.__category = category
        self.__stock = stock
        self.__ratings = []

    def add_rating(self, rating):
        if 1 <= rating <= 5:
            self.__ratings.append(rating)
        else:
            print("Invalid rating. Must be between 1 and 5.")

    def average_rating(self):
        return sum(self.__ratings) / len(self.__ratings) if self.__ratings else 0

    def get_name(self):
        return self.__name

    def get_price_range(self):
        return self.__price_range

    def get_category(self):
        return self.__category

    def get_stock(self):
        return self.__stock

    def set_stock(self, stock):
        self.__stock = stock

    def __str__(self):
        return f"{self.__name} | Price: {self.__price_range} | Category: {self.__category} | Stock: {self.__stock} | Avg Rating: {self.average_rating():.2f}"

# Cart class to manage the shopping cart
class Cart:
    def __init__(self):
        self.__items = {}

    def add_item(self, product, quantity):
        if product.get_name() in self.__items:
            self.__items[product.get_name()]['quantity'] += quantity
        else:
            self.__items[product.get_name()] = {'product': product, 'quantity': quantity}

    def remove_item(self, product_name):
        if product_name in self.__items:
            del self.__items[product_name]

    def view_cart(self):
        return {name: {'product': item['product'], 'quantity': item['quantity']} for name, item in self.__items.items()}

    def total_items(self):
        return sum(item['quantity'] for item in self.__items.values())

# Order class to handle user orders
class Order:
    def __init__(self, cart):
        self.__cart = cart
        self.__completed = False

    def complete_order(self):
        self.__completed = True

    def __str__(self):
        # Construct a detailed view of the items in the order
        items_details = "\n".join(
            f"{item['product'].get_name()} | Price: {item['product'].get_price_range()} | Quantity: {item['quantity']} | Avg Rating: {item['product'].average_rating():.2f}"
            for item in self.__cart.view_cart().values()
        )
        return f"Order Status: {'Completed' if self.__completed else 'Pending'} | Items: {self.__cart.total_items()}\nDetails:\n{items_details}"

# Main application logic
class Shop:
    def __init__(self):
        self.__products = []
        self.__cart = Cart()
        self.__orders = []

        # Load data from file or initialize with some default products
        self.__load_data()
        if not self.__products:  # If no products are loaded, add default products
            self.__initialize_default_products()

    def add_product(self, name, price_range, category, stock):
        self.__products.append(Product(name, price_range, category, stock))

    def view_products(self):
        return [str(product) for product in self.__products]

    def find_product(self, name=None, price_range=None, category=None):
        results = []
        for product in self.__products:
            if (name and name.lower() in product.get_name().lower()) or \
               (price_range and price_range in product.get_price_range()) or \
               (category and category.lower() == product.get_category().lower()):
                results.append(product)
        return results

    def add_to_cart(self, product_name, quantity):
        product = next((p for p in self.__products if p.get_name() == product_name), None)
        if product:
            if product.get_stock() >= quantity:
                self.__cart.add_item(product, quantity)
                product.set_stock(product.get_stock() - quantity)
                self.__save_data()
                print("Product added to cart.")
            else:
                print(f"Not enough stock for {product_name}.")
        else:
            print("Product not found.")

    def view_cart(self):
        cart_items = self.__cart.view_cart()
        return {name: {'product': str(item['product']), 'quantity': item['quantity']} for name, item in cart_items.items()}

    def remove_from_cart(self, product_name):
        self.__cart.remove_item(product_name)
        self.__save_data()

    def finalize_order(self):
        order = Order(self.__cart)
        order.complete_order()
        self.__orders.append(order)
        self.__cart = Cart()  # Empty the cart after finalizing
        self.__save_data()

    def view_orders(self):
        # Print detailed information of each order
        return [str(order) for order in self.__orders]

    def rate_product(self, product_name, rating):
        product = next((p for p in self.__products if p.get_name() == product_name), None)
        if product and 1 <= rating <= 5:
            product.add_rating(rating)
            self.__save_data()
            print("Rating submitted.")
        else:
            print("Product not found or invalid rating.")

    def __save_data(self):
        with open(DATA_FILE, 'wb') as file:
            pickle.dump({
                'products': self.__products,
                'cart': self.__cart,
                'orders': self.__orders
            }, file)

    def __load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'rb') as file:
                data = pickle.load(file)
                self.__products = data.get('products', [])
                self.__cart = data.get('cart', Cart())
                self.__orders = data.get('orders', [])

    def __initialize_default_products(self):
        # Add some default products
        self.add_product("Laptop", "1000-1500", "Electronics", 10)
        self.add_product("Headphones", "50-100", "Accessories", 20)
        self.add_product("Smartphone", "500-800", "Electronics", 15)
        self.__save_data()

    def menu(self):
        while True:
            print("\n--- Shop Menu ---")
            print("1. View Products")
            print("2. Search for Product")
            print("3. Add Product to Cart")
            print("4. View Cart")
            print("5. Remove Product from Cart")
            print("6. Finalize Order")
            print("7. View Orders")
            print("8. Rate a Product")
            print("9. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                print("\nProducts Available:")
                for product in self.view_products():
                    print(product)

            elif choice == '2':
                name = input("Enter product name (or leave blank): ")
                price_range = input("Enter price range (or leave blank): ")
                category = input("Enter category (or leave blank): ")
                results = self.find_product(name, price_range, category)
                if results:
                    print("\nSearch Results:")
                    for product in results:
                        print(product)
                else:
                    print("No products found.")

            elif choice == '3':
                product_name = input("Enter product name to add to cart: ")
                quantity = int(input("Enter quantity: "))
                self.add_to_cart(product_name, quantity)

            elif choice == '4':
                print("\nCart Contents:")
                for name, item in self.view_cart().items():
                    print(f"{name} | {item['product']} | Quantity: {item['quantity']}")

            elif choice == '5':
                product_name = input("Enter product name to remove from cart: ")
                self.remove_from_cart(product_name)

            elif choice == '6':
                self.finalize_order()
                print("Order finalized.")

            elif choice == '7':
                print("\nOrders:")
                for order in self.view_orders():
                    print(order)

            elif choice == '8':
                product_name = input("Enter product name to rate: ")
                rating = int(input("Enter rating (1 to 5): "))
                self.rate_product(product_name, rating)

            elif choice == '9':
                print("Exiting the application.")
                break

            else:
                print("Invalid choice. Please try again.")

# Main execution
if __name__ == "__main__":
    shop = Shop()
    shop.menu()
