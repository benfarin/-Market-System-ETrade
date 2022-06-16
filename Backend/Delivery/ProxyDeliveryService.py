import zope

from Backend.Payment.IPaymentService import IPaymentService


@zope.interface.implementer(IPaymentService)
class ProxyDeliveryService:
    def __init__(self, real_subject):
        self._real_subject = real_subject

    def check_access(self):
        return self._real_subject is None


    def connect(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.connect()

    def makeSupply(self, name , address, city, country, zip):
        if self.check_access():
            return True
        else:
            return self._real_subject.makeSupply(name , address, city, country, zip)

    def cancelSupply(self,  transaction_id):
        if self.check_access():
            return True
        else:
            return self._real_subject.cancelSupply(transaction_id)

    def changeExternalDelivery(self, deliverySystem):
        self._real_subject = deliverySystem