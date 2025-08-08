from event import Event
from pair import Pair


class Order(Event):
    def __init__(self, pair : Pair , price : float, quantity: float):
        super().__init__()
        self.pair = pair
        self.price = price
        self.quantity = quantity