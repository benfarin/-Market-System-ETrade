from Backend.Payment.PaymentSystem import PaymentSystem
from Backend.Payment.PaymentStatus import PaymentStatus
from Backend.Payment.PaymentDetails import PaymentDetails
from Backend.interfaces.IPayment import IPayment


class Paymentlmpl:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Paymentlmpl.__instance is None:
            Paymentlmpl()
        return Paymentlmpl.__instance

    def __init__(self):
        self.__paymentSystem: PaymentSystem = PaymentSystem().getInstance()
        self.__messegeError = "error"
        self.__paymentId = 0
        if Paymentlmpl.__instance is None:
            Paymentlmpl.__instance = self

    def createPayment(self, paymentDetails: PaymentDetails):
        try:
            self.__paymentSystem.CreatePayment(paymentDetails.getUserId(),
                                               paymentDetails.getClientBankAccount().getAccountNumber(),
                                               paymentDetails.getClientBankAccount().getBranch(),
                                               paymentDetails.getRecieverBankAccount().getAccountNumber(),
                                               paymentDetails.getRecieverBankAccount().getBranch(),
                                               paymentDetails.getPaymentAmount())

            return PaymentStatus(self.getPaymentId(), paymentDetails.getUserId(), "payment succeeded")
        except Exception:
            return PaymentStatus(self.getPaymentId(), paymentDetails.getUserId(), "payment failed")

    def cancelPayment(self, paymentStatus: PaymentStatus):
        try:
            self.__paymentSystem.CancelPayment(paymentStatus.paymentId)
            paymentStatus.setStatus("cancel payment succeeded")
        except Exception:
            paymentStatus.status("cancel payment failed")

    def getPaymentId(self):
        paymentId = self.__paymentId
        self.__paymentId += 1
        return paymentId
