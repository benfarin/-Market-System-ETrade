def singleton_dec(class_):
    instances = {}
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance

@singleton_dec
class PaymentSystem(implements(IMarket)):

    def CancelPayment(self,paymentId) :
            return generatePaymentId()

    def generatePaymentId(self):
            return Guid.NewGuid()

    def CreatePayment(self,clientId,accountNumber1 ,branch1 , accountNumber2 ,branch2, paymentAmount):
            return Guid.NewGuid()
