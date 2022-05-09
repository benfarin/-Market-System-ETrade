class PaymentStatus:
    def __init__(self, paymentId, clientId, status):
        self.paymentId = paymentId
        self.clientId = clientId
        self.status = status

    def getPaymentId(self):
        return self.paymentId

    def getUserId(self):
        return self.clientId

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
