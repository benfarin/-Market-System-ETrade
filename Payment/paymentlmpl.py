from Payment.PaymentSystem import PaymentSystem
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentDetails import PaymentDetails


class paymentlmpl:
    def __init__(self):
        self.__paymentSystem : PaymentSystem = PaymentSystem()
        self.__messegeError = "error"

    def cancelPayment(self,paymentStatus : PaymentStatus ):
        paymentID = self.__paymentSystem.CancelPayment(paymentStatus.paymentId)
        return PaymentStatus(paymentID, paymentStatus.clientId, paymentStatus.storeId, not paymentStatus.status == self.__messegeError)
    def createPayment(self,paymentDetails : PaymentDetails):
        paymentID = self.__paymentSystem.CreatePayment(paymentDetails.getClientId(),paymentDetails.getClientBankAccount().getAccountNumber(),paymentDetails.getClientBankAccount().getBranch(),paymentDetails.getRecieverBankAccount().getAccountNumber(),paymentDetails.getRecieverBankAccount().getBranch(),paymentDetails.getPaymentAmount())
        return PaymentStatus(paymentID,paymentStatus.clientId,paymentStatus.storeId,not paymentStatus.status == self.__messegeError )

