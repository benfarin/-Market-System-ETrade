from Backend.ExternalSystem.ExternalSystem import ExternalSystem
from Backend.Payment.PaymentStatus import PaymentStatus
from Backend.Payment.PaymentDetails import PaymentDetails


class Paymentlmpl:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Paymentlmpl.__instance is None:
            Paymentlmpl()
        return Paymentlmpl.__instance

    def __init__(self):
        self.__paymentSystem: ExternalSystem = ExternalSystem().getInstance()
        if Paymentlmpl.__instance is None:
            Paymentlmpl.__instance = self

    def createPayment(self, paymentDetails: PaymentDetails):
        try:
            params = {"action_type": "pay",
                      "card_number": paymentDetails.getCardNumber(),
                      "month": paymentDetails.getMonth(),
                      "year": paymentDetails.getYear(),
                      "holder": paymentDetails.getHolderCardName(),
                      "ccv": paymentDetails.getCVV(),
                      "id": paymentDetails.getHolderID()
                      }

            paymentId = self.__paymentSystem.CreateRequest(params)

            return PaymentStatus(paymentId, paymentDetails.getUserId(), "payment succeeded")

        except Exception as e:
            return PaymentStatus(-1, paymentDetails.getUserId(), e)

    def cancelPayment(self, paymentStatus: PaymentStatus):
        try:
            params = {"action_type": "cancel_pay",
                      "transaction_id": paymentStatus.getPaymentId(),
                      }
            self.__paymentSystem.CancelRequest(params)
            paymentStatus.setStatus("cancel payment succeeded")

        except Exception as e:
            paymentStatus.status("cancel payment failed")

