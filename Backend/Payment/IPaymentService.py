from zope.interface import Interface


class IPaymentService(Interface):

    def connect(self):
        pass

    def makePayment(self, card_number, month, year, holder, ccv, id):
        pass

    def cancelPayment(self, transaction_id):
        pass
