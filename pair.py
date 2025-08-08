class Pair:
    def __init__(self, base_currency, quote_currency):
        self.base_currency = base_currency
        self.quote_currency = quote_currency

    def __str__(self):
        return f"{self.base_currency}/{self.quote_currency}"