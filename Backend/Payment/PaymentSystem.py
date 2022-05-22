
from Backend.Exceptions.CustomExceptions import PaymentException


class PaymentSystem:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if PaymentSystem.__instance is None:
            PaymentSystem()
        return PaymentSystem.__instance

    def __init__(self):
        if PaymentSystem.__instance is None:
            PaymentSystem.__instance = self

    def CreatePayment(self, clientId, accountNumber1, branch1, accountNumber2, branch2, paymentAmount):
        # if np.random.random() < 0.05:
        #     raise PaymentException("payment failed")
        return True

    def CancelPayment(self, paymentId):
        if paymentId >= 0:
            return True
        else:
            raise PaymentException("illegal paymentId")
