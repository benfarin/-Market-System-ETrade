from Payment.PaymentStatus import PaymentStatus


class PaymentStatusDTO:
    def __init__(self, payment: PaymentStatus):
        self.paymentId = payment.getPaymentId()
        self.clientId = payment.getUserId()
        self.status = payment.getStatus()

    def getPaymentId(self):
        return self.paymentId

    def getClientID(self):
        return self.clientId

    def getStatus(self):
        return self.status

    def getStoreID(self):
        return self.storeId

    def setStatus(self, status):
        self.status = status

    def setClientID(self, clientID):
        self.clientId = clientID

    def setStoreID(self, storeID):
        self.storeId = storeID

    def setPaymentID(self, paymentID):
        self.paymentId = paymentID

    def __str__(self):
        toReturn = "payment" + str(self.paymentId) + ":"
        toReturn += "\n\tuserId: " + str(self.clientId)
        return toReturn + "\n\tstatus: " + str(self.status)


