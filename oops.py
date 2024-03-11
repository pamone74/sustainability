import datetime

class Product:
    def __init__(self, price, type, origin):
        self.__price = price
        self.__origin = origin
        self.__type = type

    def getter(self):
        return self.__price

    def config(self):
        if self.__type == "recyclable":
            return 1

class Manufacturer:
    def __init__(self, quantity, product_id, product_type, product_date, admin, merchant):
        self.id = product_id
        self.type = product_type
        self.date = product_date
        self.mer = merchant
        self.admin = admin
        self.quan = quantity

    def create(self):
        return [self.id, self.type, self.date, self.mer, self.quan]

class Merchant:
    def __init__(self, quantity, type, admin):
        self.quan = quantity
        self.type = type
        self.admin = admin

    def remain(self):
        return self.quan

    def track(self):
        admin = False
        item = Manufacturer(100, 550055, "bottles", datetime.timedelta(), admin,"merchant")
        item.create()
        merc = Merchant(20, "bottles", admin=True)
        if item.type == merc.type:
            item.quan -= merc.quan
            admin = "Merchant has taken 20 and manufacturer has 100"
        return [item.quan,merc.quan]

def main():
    #merchant_instance = Merchant(20, "bottles", admin=True)

   print(datetime.datetime.now)
    #print(Merchant.track())

if __name__ == "__main__":
    main()
