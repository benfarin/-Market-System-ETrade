class MarketService:
        __instance = None

        @staticmethod
        def getInstance():
            """ Static access method. """
            if MarketService.__instance is None:
                __instance = MarketService()
            return MarketService.__instance

        def __init__(self):
            """ Virtually private constructor. """
            if MarketService.__instance is not None:
                raise Exception("This class is a singleton!")
            else:
                MarketService.__instance = self
s = MarketService()

