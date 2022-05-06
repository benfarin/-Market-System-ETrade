from zope.interface import Interface


from Payment.PaymentDetails import PaymentDetails
from Payment.PaymentStatus import PaymentStatus


class IPayment(Interface):

    def createPayment(self, paymentDetails: PaymentDetails):
        pass

    def cancelPayment(self, paymentStatus: PaymentStatus):
        pass
