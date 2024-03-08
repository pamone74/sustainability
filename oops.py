class Products:
    def __init__(self, price, ttype, origin):
        self.__final = price  
        self.__orgin = origin
        self.__type = ttype
    def getter(self):
        return self.__final
    # def setter(self):
    #     self.__final = self.__final * 10
    #     return self.__final
    def config(self):
        if(self.__type == "recycable"):
            return 1