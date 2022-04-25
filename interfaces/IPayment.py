from interface import Interface


class IPayment(Interface):

    def createPayment(self, paymentDetails):
        pass

    def cancelPayment(self, paymentStatus):
        pass
