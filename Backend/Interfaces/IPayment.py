from zope.interface import Interface


from Backend.Payment.PaymentDetails import PaymentDetails
from Backend.Payment.PaymentStatus import PaymentStatus


class IPayment(Interface):

    def createPayment(self, paymentDetails: PaymentDetails):
        pass

    def cancelPayment(self, paymentStatus: PaymentStatus):
        pass
