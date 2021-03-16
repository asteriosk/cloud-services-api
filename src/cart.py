import service
from exceptions import NotAvailableStockException
from payment import Payment
from inventory import Inventory
from service import ManagedMap
# from turbine import ManagedList

@service.endpoint("/cart")
class Cart:
    # Managed state holding the shopping cart contents
    cart: ManagedMap = ManagedMap()

    stock_svc: Inventory = service.service.discover(Inventory.__class__)
    payment_svc: Payment = service.service.discover(Payment.__class__)

    # permits one item at a time.
    @service.endpoint(endpoint = "/cart/add_item", method={"user_id": "POST", "item_id": "GET"})
    def add_item(self, user_id: int, item_id: int) -> bool:
        user_items = self.cart.get(user_id)

        if not user_items:
            user_items = []
            self.cart.put(user_id, user_items)

        user_items.append(item_id)

        return True

    @service.endpoint(endpoint = "/cart/remove_item", method={"user_id": "POST", "item_id": "GET"})
    def remove_item(self, user_id: int, item_id: int) -> bool:
        user_items = self.cart.get(user_id)

        if not user_items:
            return False

        user_items.remove(item_id)

        return True

    # The transactional decoration ensures that all function calls are atomic and successful (i.e., no exceptions
    # return from calls by turbine convention)
    @service.transactional
    @service.endpoint(endpoint = "/cart/checkout", method={"user_id": "POST"})
    def checkout(self, user_id: int) -> bool:
        orchestrator = service.Orchestrator()

        orchestrator.start_saga()

        total_price = 0

        # checks if all items are available
        for item in self.cart.get(user_id):

            item_available = orchestrator.call(self.stock_svc.available, {"item_id": item})

            if not item_available:
                raise NotAvailableStockException("No items left for item_id: " + str(item))

            status = orchestrator.call(self.stock_svc.subtract, {"item_id": item, "quantity": 1})

            price = orchestrator.call(self.stock_svc.price, {"item_id": item})

            total_price += price

        # subtracts the items
        status = orchestrator.call(self.payment_svc.pay, {"user_id": user_id,"total_price": total_price})

        orchestrator.end_saga()

        return True

if __name__ == '__main__':
    pass

