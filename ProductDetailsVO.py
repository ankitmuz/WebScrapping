class ProductDetailsVO:
    PRICE = ""
    TITLE = ""
    STOCK = ""
    MAFTR = ""

    def set_price(self, price):
        self.PRICE = price;

    def set_title(self, title):
        self.TITLE = title;

    def set_stock(self, stock):
        self.STOCK = stock;

    def set_maftr(self, maftr):
        self.MAFTR = maftr;

    def get_price(self):
        return self.PRICE

    def get_title(self):
        return self.TITLE

    def get_stock(self):
        return self.STOCK

    def get_maftr(self):
        return self.MAFTR
