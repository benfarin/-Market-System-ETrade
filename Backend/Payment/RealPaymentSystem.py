import requests
import zope

from Backend.Exceptions.CustomExceptions import PaymentException
from Backend.ExternalSystem.ExternalSystem import ExternalSystem
from Backend.Payment.IPaymentService import IPaymentService

from django.conf import settings


@zope.interface.implementer(IPaymentService)
class RealPaymentService:
    def __init__(self, url=None):
        if url is None:
            self.external_system = settings.EXTERNAL_SYSTEM_URL
        else:
            self.external_system = url

    def connect(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.isSystemExists()

    def isSystemExists(self):
        try:
            request = requests.post(self.external_system, data={'action_type': 'handshake'}, timeout=15)
            if request.content == b'OK':
                return True
            return False
        except Exception as e:
            return False

    def makePayment(self, card_number, month, year, holder, ccv, id):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now, please try later")
        try:
            params = {"action_type": "pay",
                      "card_number": card_number,
                      "month": month,
                      "year": year,
                      "holder": holder,
                      "ccv": ccv,
                      "id": id
                      }
            request = requests.post(self.external_system, data=params, timeout=15)
            paymentId = int.from_bytes(request.content, "little")
            if paymentId == -1:
                raise Exception("the transaction has failed")
            return paymentId
        except requests.exceptions.Timeout:
            raise PaymentException("The payment took too long")
        except:
            raise PaymentException("the transaction has failed")

    def cancelPayment(self, transaction_id):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now, please try later")
        try:
            params = {"action_type": "cancel_pay",
                      "transaction_id": transaction_id,
                      }
            request = requests.post(self.external_system, data=params, timeout=15)
            paymentId = int.from_bytes(request.content, "little")
            if paymentId == -1:
                raise Exception("the transaction has failed")
            return paymentId
        except:
            raise Exception("the transaction has failed")
