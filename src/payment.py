from exceptions import NotEnoughFundsException
from turbine import ManagedMap

class Payment:
    accounts = ManagedMap()

    def pay(self, user_id: int, amount: float) -> bool:
        funds = self.accounts.get(user_id)

        if funds >= amount:
            self.accounts.put(user_id, funds - amount)
        else:
            raise NotEnoughFundsException()

        return True

    def refund(self, user_id: int, amount: int) -> bool:
        funds = self.accounts.get(user_id)
        self.accounts.put(user_id, funds + amount)
        return True
