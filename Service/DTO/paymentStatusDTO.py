class paymentStatusDTO:
    def __init__(self, paymentId, clientId, storeId, status):
        self.paymentId = paymentId
        self.clientId = clientId
        self.storeId = storeId
        self.status = status

    def getPaymentId(self):
        return self.paymentId

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

    def setStatus(self, status):
        self.status = status
