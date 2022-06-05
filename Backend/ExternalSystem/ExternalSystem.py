import requests


class ExternalSystem:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ExternalSystem.__instance is None:
            ExternalSystem()
        return ExternalSystem.__instance

    def __init__(self):
        self.externalURL = 'https://cs-bgu-wsep.herokuapp.com/'
        if ExternalSystem.__instance is None:
            ExternalSystem.__instance = self

    def CreateRequest(self, params):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now, please try later")
        request = requests.post(self.externalURL, data=params)
        paymentId = int.from_bytes(request.content, "little")
        if paymentId == -1:
            raise Exception("the transaction has failed")
        return paymentId

    def CancelRequest(self, params):
        if not self.isSystemExists():
            raise Exception("the external system is not available right now.")
        request = requests.post(self.externalURL, data=params)
        paymentId = int.from_bytes(request.content, "little")
        if paymentId == -1:
            raise Exception("the cancel request has failed")
        return paymentId

    def isSystemExists(self):
        try:
            request = requests.post(self.externalURL, data={'action_type': 'handshake'})
            if request.content == b'OK':
                return True
            return False
        except Exception as e:
            return False



