import requests
import zope

from Backend.Payment.IPaymentService import IPaymentService

from django.conf import settings


@zope.interface.implementer(IPaymentService)
class RealDeliveryService:
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

    def makeSupply(self, name, address, city, country, zip):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now, please try later")
        try:
            params = {"action_type": "supply",
                      "name": name,
                      "address": address,
                      "city": city,
                      "country": country,
                      "zip": zip
                      }
            request = requests.post(self.external_system, data=params, timeout=15)
            supplyId = int.from_bytes(request.content, "little")
            if supplyId == -1:
                raise Exception("the transaction has failed")
            return supplyId
        except:
            raise Exception("the transaction has failed")

    def cancelSupply(self, transaction_id):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now, please try later")
        try:
            params = {"action_type": "cancel_supply",
                      "transaction_id": transaction_id,
                      }
            request = requests.post(self.external_system, data=params, timeout=15)
            supplyId = int.from_bytes(request.content, "little")
            if supplyId == -1:
                raise Exception("the transaction has failed")
            return supplyId
        except:
            raise Exception("the transaction has failed")
