class PaymentStatus:
    def __init__(self, paymentId, clientId, storeId, status):
        self.paymentId = paymentId
        self.clientId = clientId
        self.storeId = storeId
        self.status = status

    def getPaymentId(self):
        return self.paymentId

    def setStatus(self, status):
        self.status = status
