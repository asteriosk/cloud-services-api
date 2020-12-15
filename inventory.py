from helpers import NotEnoughStockException
from turbine import ManagedMap

class Inventory:
    item_count = ManagedMap()
    item_price = ManagedMap()

    def subtract(self, item_id: int, cnt: int) -> bool:
        available_stock = self.item_count.get(item_id)

        if available_stock < cnt:
            raise NotEnoughStockException()

        self.item_count.put(item_id, available_stock - cnt)

        return True

    def available(self, item_id: int) -> int:
        if self.item_count.get(item_id) > 0:
            return 1

        return 0

    def price(self, item_id: int) -> float:
        return self.item_price.get(item_id)
