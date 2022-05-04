from Payment.PaymentSystem import PaymentSystem
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentDetails import PaymentDetails
from interfaces.IPayment import IPayment
from interface import implements


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

            return PaymentStatus(self.__getPaymentId(), paymentDetails.getUserId(), paymentDetails.getstoreID(),
                                 "payment succeeded")
        except Exception:
            return PaymentStatus(self.__getPaymentId(), paymentDetails.getUserId(), paymentDetails.getstoreID(),
                                 "payment failed")

    def cancelPayment(self, paymentStatus: PaymentStatus):
        try:
            self.__paymentSystem.CancelPayment(paymentStatus.paymentId)
            paymentStatus.setStatus("cancel payment succeeded")
        except Exception:
            paymentStatus.status("cancel payment failed")



    def __getPaymentId(self):
        paymentId = self.__paymentId
        self.__paymentId += 1
        return paymentId
