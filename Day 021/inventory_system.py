from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional
import json
import operator
from functools import reduce


@dataclass
class Product:
    id: int
    name: str
    category: str
    price: float
    quantity: int
    reorder_level: int
    last_updated: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "quantity": self.quantity,
            "reorder_level": self.reorder_level,
            "last_updated": self.last_updated,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        return cls(**data)


class InventoryManagementSystem:
    def __init__(self):
        self.products: List[Product] = []
        self.categories: set = set()
        self.transaction_history: List[dict] = []

    def add_product(self, product: Product) -> None:
        """Add a new product to inventory using list append."""
        if not any(p.id == product.id for p in self.products):
            self.products.append(product)
            self.categories.add(product.category)
            self._add_transaction("ADD", product.id, product.quantity)
        else:
            raise ValueError(f"Product with ID {product.id} already exists")

    def remove_product(self, product_id: int) -> None:
        """Remove a product using list comprehension."""
        initial_length = len(self.products)
        self.products = [p for p in self.products if p.id != product_id]
        if len(self.products) == initial_length:
            raise ValueError(f"Product with ID {product_id} not found")
        self._add_transaction("REMOVE", product_id, 0)

    def update_quantity(self, product_id: int, quantity_change: int) -> None:
        """Update product quantity using next() and list comprehension."""
        product = next((p for p in self.products if p.id == product_id), None)
        if product:
            new_quantity = product.quantity + quantity_change
            if new_quantity >= 0:
                product.quantity = new_quantity
                product.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self._add_transaction("UPDATE", product_id, quantity_change)
            else:
                raise ValueError("Insufficient stock")
        else:
            raise ValueError(f"Product with ID {product_id} not found")

    def get_low_stock_products(self) -> List[Product]:
        """Get products below reorder level using filter()."""
        return list(filter(lambda p: p.quantity <= p.reorder_level, self.products))

    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category using list comprehension."""
        return [p for p in self.products if p.category.lower() == category.lower()]

    def search_products(self, search_term: str) -> List[Product]:
        """Search products using filter() and lambda."""
        return list(
            filter(
                lambda p: search_term.lower() in p.name.lower()
                or search_term.lower() in p.category.lower(),
                self.products,
            )
        )

    def sort_products(self, key: str = "name", reverse: bool = False) -> List[Product]:
        """Sort products using sorted() and operator.attrgetter()."""
        return sorted(self.products, key=operator.attrgetter(key), reverse=reverse)

    def get_total_inventory_value(self) -> float:
        """Calculate total inventory value using reduce()."""
        return reduce(lambda acc, p: acc + (p.price * p.quantity), self.products, 0)

    def get_category_summary(self) -> Dict[str, dict]:
        """Get summary by category using dictionary comprehension and list comprehension."""
        return {
            category: {
                "count": len(
                    category_products := [
                        p for p in self.products if p.category == category
                    ]
                ),
                "total_value": sum(p.price * p.quantity for p in category_products),
                "average_price": sum(p.price for p in category_products)
                / len(category_products),
            }
            for category in self.categories
        }

    def _add_transaction(self, action: str, product_id: int, quantity: int) -> None:
        """Add a transaction to history using list append."""
        self.transaction_history.append(
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "action": action,
                "product_id": product_id,
                "quantity": quantity,
            }
        )

    def save_to_file(self, filename: str) -> None:
        """Save inventory to file using list comprehension."""
        data = {
            "products": [p.to_dict() for p in self.products],
            "transactions": self.transaction_history,
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_from_file(self, filename: str) -> None:
        """Load inventory from file using list comprehension."""
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.products = [Product.from_dict(p) for p in data["products"]]
                self.categories = {p.category for p in self.products}
                self.transaction_history = data["transactions"]
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filename} not found")


def main():
    ims = InventoryManagementSystem()

    # Sample products for testing
    sample_products = [
        Product(
            1,
            "Laptop",
            "Electronics",
            999.99,
            10,
            5,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
        Product(
            2,
            "Smartphone",
            "Electronics",
            599.99,
            15,
            8,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
        Product(
            3,
            "Desk Chair",
            "Furniture",
            199.99,
            8,
            4,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
        Product(
            4,
            "Coffee Maker",
            "Appliances",
            79.99,
            12,
            6,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    ]

    # Add sample products
    for product in sample_products:
        ims.add_product(product)

    while True:
        print("\nInventory Management System")
        print("1. Add Product")
        print("2. Remove Product")
        print("3. Update Quantity")
        print("4. View All Products")
        print("5. Search Products")
        print("6. View Low Stock Products")
        print("7. View Category Summary")
        print("8. View Total Inventory Value")
        print("9. Save Inventory")
        print("10. Load Inventory")
        print("11. Exit")

        choice = input("\nEnter your choice (1-11): ")

        try:
            if choice == "1":
                id = int(input("Enter product ID: "))
                name = input("Enter product name: ")
                category = input("Enter product category: ")
                price = float(input("Enter product price: "))
                quantity = int(input("Enter product quantity: "))
                reorder_level = int(input("Enter reorder level: "))

                product = Product(
                    id=id,
                    name=name,
                    category=category,
                    price=price,
                    quantity=quantity,
                    reorder_level=reorder_level,
                    last_updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                )
                ims.add_product(product)
                print("Product added successfully!")

            elif choice == "2":
                id = int(input("Enter product ID to remove: "))
                ims.remove_product(id)
                print("Product removed successfully!")

            elif choice == "3":
                id = int(input("Enter product ID: "))
                quantity_change = int(
                    input("Enter quantity change (positive or negative): ")
                )
                ims.update_quantity(id, quantity_change)
                print("Quantity updated successfully!")

            elif choice == "4":
                sort_by = input("Sort by (name/price/quantity): ")
                reverse = input("Reverse order? (y/n): ").lower() == "y"

                products = ims.sort_products(sort_by, reverse)
                print("\nProduct List:")
                for product in products:
                    print(
                        f"ID: {product.id}, Name: {product.name}, "
                        f"Category: {product.category}, Price: ${product.price:.2f}, "
                        f"Quantity: {product.quantity}"
                    )

            elif choice == "5":
                search_term = input("Enter search term: ")
                results = ims.search_products(search_term)
                print("\nSearch Results:")
                for product in results:
                    print(
                        f"ID: {product.id}, Name: {product.name}, "
                        f"Category: {product.category}, Quantity: {product.quantity}"
                    )

            elif choice == "6":
                low_stock = ims.get_low_stock_products()
                print("\nLow Stock Products:")
                for product in low_stock:
                    print(
                        f"ID: {product.id}, Name: {product.name}, "
                        f"Quantity: {product.quantity}, Reorder Level: {product.reorder_level}"
                    )

            elif choice == "7":
                summary = ims.get_category_summary()
                print("\nCategory Summary:")
                for category, data in summary.items():
                    print(f"\nCategory: {category}")
                    print(f"Total Products: {data['count']}")
                    print(f"Total Value: ${data['total_value']:.2f}")
                    print(f"Average Price: ${data['average_price']:.2f}")

            elif choice == "8":
                total_value = ims.get_total_inventory_value()
                print(f"\nTotal Inventory Value: ${total_value:.2f}")

            elif choice == "9":
                filename = input("Enter filename to save: ")
                ims.save_to_file(filename)
                print("Inventory saved successfully!")

            elif choice == "10":
                filename = input("Enter filename to load: ")
                ims.load_from_file(filename)
                print("Inventory loaded successfully!")

            elif choice == "11":
                print("Thank you for using the Inventory Management System!")
                break

            else:
                print("Invalid choice. Please try again.")

        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
