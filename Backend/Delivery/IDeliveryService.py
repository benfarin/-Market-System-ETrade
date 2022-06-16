from zope.interface import Interface


class IPaymentService(Interface):

    def connect(self):
        pass

    def makeSupply(self, name , address, city, country, zip):
        pass

    def cancelSupply(self,  transaction_id):
        pass
