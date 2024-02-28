class StoreItem:
    """
    A general class to store item data concisely.
    """

    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        # self.manufacturer = manufacturer
        self.availability = availability
