import io
import contextlib
from typing import List, Tuple

# Named constants to replace magic numbers and global mutable state
DEFAULT_TAX_RATE = 0.07
FOOD_TAX_RATE = 0.0
LARGE_ORDER_QTY_THRESHOLD = 10
LARGE_ORDER_BONUS_DISCOUNT = 0.03

HIGH_SUBTOTAL_THRESHOLD = 100.0


# ----------------------------------------------------------------------
# Domain Classes & OOP Architecture
# ----------------------------------------------------------------------

class Tier:
    """Base class defining the customer tier discount and points behavior (Polymorphism)."""
    name = "none"

    def get_tier_discount(self, subtotal: float) -> float:
        return 0.0

    def get_points(self, total: float) -> int:
        return int(total // 10)


class NoneTier(Tier):
    name = "none"


class SilverTier(Tier):
    name = "silver"

    def get_tier_discount(self, subtotal: float) -> float:
        return subtotal * 0.05 if subtotal > HIGH_SUBTOTAL_THRESHOLD else subtotal * 0.02

    def get_points(self, total: float) -> int:
        return int(total // 10) * 2


class GoldTier(Tier):
    name = "gold"

    def get_tier_discount(self, subtotal: float) -> float:
        return subtotal * 0.10 if subtotal > HIGH_SUBTOTAL_THRESHOLD else subtotal * 0.05

    def get_points(self, total: float) -> int:
        return int(total // 10) * 3


class PlatinumTier(Tier):
    name = "platinum"

    def get_tier_discount(self, subtotal: float) -> float:
        return subtotal * 0.15 if subtotal > HIGH_SUBTOTAL_THRESHOLD else subtotal * 0.10

    def get_points(self, total: float) -> int:
        return int(total // 10) * 5


class TierFactory:
    """Encapsulates creation of Tier objects from string identifiers."""
    _TIERS = {
        "none": NoneTier(),
        "silver": SilverTier(),
        "gold": GoldTier(),
        "platinum": PlatinumTier(),
    }

    @classmethod
    def get_tier(cls, tier_name: str) -> Tier:
        if tier_name not in cls._TIERS:
            raise ValueError(f"Invalid tier: {tier_name}")
        return cls._TIERS[tier_name]


class Product:
    """Represents an item available for purchase with price and category validation (Encapsulation)."""
    def __init__(self, name: str, price: float, category: str):
        if price < 0:
            raise ValueError("Price cannot be negative.")
        if not name:
            raise ValueError("Product name cannot be empty.")
        self.name = name
        self.price = price
        self.category = category

    def get_tax_rate(self) -> float:
        return FOOD_TAX_RATE if self.category == "food" else DEFAULT_TAX_RATE


class OrderItem:
    """Represents a line item inside an order pairing a Product and a quantity."""
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be positive.")
        self.product = product
        self.quantity = quantity

    def line_subtotal(self) -> float:
        return self.product.price * self.quantity

    def line_tax(self) -> float:
        return self.line_subtotal() * self.product.get_tax_rate()


class Order:
    """Encapsulates order calculation logic, returning values without direct printing."""
    def __init__(self, customer_name: str, tier: Tier, items: List[OrderItem]):
        if not customer_name:
            raise ValueError("Customer name cannot be empty.")
        self.customer_name = customer_name
        self.tier = tier
        self.items = items

    def calculate_subtotal(self) -> float:
        return sum(item.line_subtotal() for item in self.items)

    def calculate_tax(self) -> float:
        return sum(item.line_tax() for item in self.items)

    def calculate_total_quantity(self) -> int:
        return sum(item.quantity for item in self.items)

    def calculate_discount(self) -> float:
        subtotal = self.calculate_subtotal()
        tier_discount = self.tier.get_tier_discount(subtotal)
        
        bonus_discount = 0.0
        if self.calculate_total_quantity() >= LARGE_ORDER_QTY_THRESHOLD:
            bonus_discount = subtotal * LARGE_ORDER_BONUS_DISCOUNT
            
        return tier_discount + bonus_discount

    def calculate_total(self) -> float:
        return self.calculate_subtotal() - self.calculate_discount() + self.calculate_tax()

    def calculate_points(self) -> int:
        return self.tier.get_points(self.calculate_total())


class ReceiptPrinter:
    """Handles formatted receipt text rendering, keeping calculation and I/O strictly separate."""
    @staticmethod
    def print_receipt(order: Order) -> None:
        print("Receipt for " + order.customer_name + " (" + order.tier.name + ")")
        print("-" * 40)
        for item in order.items:
            line_cost = item.line_subtotal()
            print(item.product.name + " x" + str(item.quantity) + " = " + str(line_cost))
        
        subtotal = order.calculate_subtotal()
        discount = order.calculate_discount()
        tax = order.calculate_tax()
        total = order.calculate_total()
        points = order.calculate_points()

        print("-" * 40)
        print("Subtotal: " + str(round(subtotal, 2)))
        print("Discount: " + str(round(discount, 2)))
        print("Tax: " + str(round(tax, 2)))
        print("Total: " + str(round(total, 2)))
        print("Points earned: " + str(points))
        print("")


# ----------------------------------------------------------------------
# Legacy Setup & Data Conversion
# ----------------------------------------------------------------------

RAW_PRODUCTS = [
    ("Laptop", 1200.0, "electronics"),
    ("Headphones", 200.0, "electronics"),
    ("Coffee Beans", 15.0, "food"),
    ("Notebook", 5.0, "stationery"),
    ("Water Bottle", 10.0, "food"),
    ("Monitor", 300.0, "electronics"),
    ("Pen", 2.0, "stationery"),
]

PRODUCTS_OBJ = [Product(name, price, cat) for name, price, cat in RAW_PRODUCTS]

RAW_ORDERS = [
    ("Alice", "gold", [(0, 1), (1, 2), (2, 3)]),
    ("Bob", "none", [(3, 10), (6, 5)]),
    ("Charlie", "platinum", [(5, 2), (4, 6), (2, 2)]),
    ("Dana", "silver", [(1, 1), (3, 3), (6, 10)]),
]

ORDERS_OBJ = [
    Order(
        customer_name=name,
        tier=TierFactory.get_tier(tier_str),
        items=[OrderItem(PRODUCTS_OBJ[prod_idx], qty) for prod_idx, qty in item_tuples]
    )
    for name, tier_str, item_tuples in RAW_ORDERS
]


# ----------------------------------------------------------------------
# Legacy Execution & Refactored Entry Point
# ----------------------------------------------------------------------

def calc_legacy(o):
    """Original procedural legacy function preserved strictly for test golden comparison."""
    TAXRATE = 0.07
    foodtax = 0.0
    n = o[0]; t = o[1]; items = o[2]
    sub = 0.0; tax = 0.0
    print("Receipt for " + n + " (" + t + ")")
    print("-" * 40)
    for it in items:
        pi = it[0]; q = it[1]
        p = RAW_PRODUCTS[pi][1]; nm = RAW_PRODUCTS[pi][0]; cat = RAW_PRODUCTS[pi][2]
        line = p * q
        sub = sub + line
        if cat == "food":
            tax = tax + line * foodtax
        else:
            tax = tax + line * TAXRATE
        print(nm + " x" + str(q) + " = " + str(line))
    d = 0.0
    if t == "none":
        d = 0.0
    elif t == "silver":
        if sub > 100: d = sub * 0.05
        else: d = sub * 0.02
    elif t == "gold":
        if sub > 100: d = sub * 0.10
        else: d = sub * 0.05
    elif t == "platinum":
        if sub > 100: d = sub * 0.15
        else: d = sub * 0.10
    totalqty = 0
    for it in items:
        totalqty = totalqty + it[1]
    if totalqty >= 10:
        d = d + sub * 0.03
    total = sub - d + tax
    pts = 0
    if t == "none": pts = int(total // 10)
    elif t == "silver": pts = int(total // 10) * 2
    elif t == "gold": pts = int(total // 10) * 3
    elif t == "platinum": pts = int(total // 10) * 5
    print("-" * 40)
    print("Subtotal: " + str(round(sub, 2)))
    print("Discount: " + str(round(d, 2)))
    print("Tax: " + str(round(tax, 2)))
    print("Total: " + str(round(total, 2)))
    print("Points earned: " + str(pts))
    print("")
    return total


def legacy_main():
    grand = 0.0
    for o in RAW_ORDERS:
        grand = grand + calc_legacy(o)
    print("GRAND TOTAL (all orders): " + str(round(grand, 2)))


def capture(fn):
    """Run fn() and return everything it printed, as a string."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn()
    return buf.getvalue()


GOLDEN_OUTPUT = capture(legacy_main)


def refactored_main():
    """Print every receipt and the grand total — same output as legacy_main()."""
    grand_total = 0.0
    for order in ORDERS_OBJ:
        ReceiptPrinter.print_receipt(order)
        grand_total += order.calculate_total()
    print("GRAND TOTAL (all orders): " + str(round(grand_total, 2)))


def _check():
    try:
        your_output = capture(refactored_main)
    except NotImplementedError:
        print("Solution not implemented yet.\n")
        print("Below is the TARGET output your refactor must reproduce exactly:\n")
        print(GOLDEN_OUTPUT)
        return

    if your_output == GOLDEN_OUTPUT:
        print("PASS - behaviour is unchanged. Your refactor is safe.\n")
    else:
        print("FAIL - the output changed, so this is not yet a valid refactor.\n")
        g = GOLDEN_OUTPUT.splitlines()
        y = your_output.splitlines()
        for i in range(max(len(g), len(y))):
            gl = g[i] if i < len(g) else "<no line>"
            yl = y[i] if i < len(y) else "<no line>"
            if gl != yl:
                print("First difference at line " + str(i + 1) + ":")
                print("  expected: " + repr(gl))
                print("  yours:    " + repr(yl))
                break


if __name__ == "__main__":
    _check()