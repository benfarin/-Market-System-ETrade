import zope

from Backend.Payment import RealPaymentSystem
from Backend.Payment.IPaymentService import IPaymentService


@zope.interface.implementer(IPaymentService)
class ProxyPaymentService:
    def __init__(self, real_subject):
        self._real_subject = real_subject

    def check_access(self):
        return self._real_subject is None


    def connect(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.connect()

    def makePayment(self, card_number, month, year, holder, ccv, id):
        if self.check_access():
            return True
        else:
            return self._real_subject.makePayment(card_number, month, year, holder, ccv, id)

    def cancelPayment(self, transaction_id):
        if self.check_access():
            return True
        else:
            return self._real_subject.cancelPayment(transaction_id)

    def changeExternalPayment(self, paymentSystem):
        self._real_subject = paymentSystem
