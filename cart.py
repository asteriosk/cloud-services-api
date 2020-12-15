import turbine
from helpers import NotAvailableStockException
from payment import Payment
from stock import Stock
from turbine import ManagedMap
# from turbine import ManagedList

@turbine.endpoint("/cart")
class Cart:
    # Managed state holding the shopping cart contents
    cart: ManagedMap = ManagedMap()

    stock_svc: Stock = turbine.service.discover(Stock.__class__)
    payment_svc: Payment = turbine.service.discover(Payment.__class__)

    # permits one item at a time.
    @turbine.endpoint("/cart/add_item")
    def add_item(self, user_id: int, item_id: int) -> bool:
        user_items = self.cart.get(user_id)

        if not user_items:
            user_items = []
            self.cart.put(user_id, user_items)

        user_items.append(item_id)

        return True

    @turbine.endpoint("/cart/remove_item")
    def remove_item(self, user_id: int, item_id: int) -> bool:
        user_items = self.cart.get(user_id)

        if not user_items:
            return False

        user_items.remove(item_id)

        return True

    # The transactional decoration ensures that all function calls are atomic and successful (i.e., no exceptions return from calls
    # by turbine convention)
    @turbine.transactional
    @turbine.endpoint("/cart/checkout")
    def checkout(self, user_id: int) -> bool:
        total_price = 0

        # checks if all items are available
        for item in self.cart.get(user_id):
            if not self.stock_svc.available_stock(item):
                raise NotAvailableStockException("No items left for item_id: " + str(item))

            self.stock_svc.subtract_stock(item, 1)
            total_price += self.stock_svc.price(item)

        # subtracts the items
        self.payment_svc.pay(user_id, total_price)

        return True


if __name__ == '__main__':
    pass

