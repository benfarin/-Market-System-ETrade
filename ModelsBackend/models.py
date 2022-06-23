from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.
class Initialized(models.Model):
    is_initialized = models.BooleanField(default=False)


class ProductModel(models.Model):
    product_id = models.IntegerField(primary_key=True)
    storeId = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(max_length=100)
    weight = models.FloatField()


class ProductKeyword(models.Model):
    product_id = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True)
    keyword = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('product_id', 'keyword',)


class StoreTransactionModel(models.Model):
    storeId = models.IntegerField()
    storeName = models.CharField(max_length=100)
    transactionId = models.IntegerField(primary_key=True)
    paymentId = models.IntegerField()
    deliveryId = models.IntegerField(null=True)
    date = models.DateField(auto_now=True)
    amount = models.IntegerField()


class ProductsInStoreTransactions(models.Model):
    transactionId = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE)
    productId = models.ForeignKey(ProductModel, on_delete=models.CASCADE)


class UserTransactionModel(models.Model):
    userID = models.UUIDField()
    transactionId = models.IntegerField(primary_key=True)
    date = models.DateField(auto_now=True)
    totalAmount = models.IntegerField()


class StoreTransactionsInUserTransactions(models.Model):
    userTransaction_id = models.ForeignKey(UserTransactionModel, on_delete=models.CASCADE)
    storeTransaction_id = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE)


class BagModel(models.Model):
    userId = models.UUIDField(null=True)
    storeId = models.IntegerField(null=True)

    class Meta:
        unique_together = ('userId', 'storeId')


class ProductsInBagModel(models.Model):
    bag_ID = models.ForeignKey(BagModel, on_delete=models.CASCADE, null=True)
    product_ID = models.ForeignKey(ProductModel, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()


class CartModel(models.Model):
    userid = models.UUIDField()


class BagsInCartModel(models.Model):
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE, null=True)
    storeID = models.IntegerField()
    bag = models.ForeignKey(BagModel, on_delete=models.CASCADE, null=True)


class UserModel(AbstractBaseUser):
    username = models.TextField(null=True)
    userid = models.UUIDField(primary_key=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    transactions = models.ForeignKey(UserTransactionModel, on_delete=models.CASCADE, null=True)
    isLoggedIn = models.BooleanField(default=False)
    USERNAME_FIELD = 'userid'


class BankModel(models.Model):
    accountNumber = models.IntegerField()
    branch = models.IntegerField()


class AddressModel(models.Model):
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    apartmentNum = models.IntegerField()
    zipCode = models.IntegerField()


class MemberModel(UserModel):
    member_password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(null=True)


class StoreModel(models.Model):
    storeID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    founderId = models.ForeignKey(MemberModel, on_delete=models.SET_NULL, null=True)
    bankAccount = models.ForeignKey(BankModel, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(AddressModel, on_delete=models.SET_NULL, null=True)
    # appointers: Dict[IMember: []] = {}  # Member : Members list   --This is a different model
    managers = models.ManyToManyField(MemberModel, related_name='managers')
    owners = models.ManyToManyField(MemberModel, related_name='owners')
    is_active = models.BooleanField(default=True)
    # products: models.ManyToManyField(ProductModel)  --different model
    # productsQuantity = {}  # productId : quantity --This is a different model
    # transactions = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE, null=True)
    # discounts: {int: IDiscount} = {}
    # rules: {int: IRule} = {}


class ProductsInStoreModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    productID = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True)


class TransactionsInStoreModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    transactionID = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE)


class StoreUserPermissionsModel(models.Model):
    userID = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    appointManager = models.BooleanField(default=False)
    appointOwner = models.BooleanField(default=False)
    closeStore = models.BooleanField(default=False)
    stockManagement = models.BooleanField(default=False)
    changePermission = models.BooleanField(default=False)
    rolesInformation = models.BooleanField(default=False)
    purchaseHistoryInformation = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    bid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('userID', 'storeID',)


class StoreAppointersModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    assingee = models.ForeignKey(MemberModel, on_delete=models.CASCADE, related_name='assingee', default=None)
    assigner = models.ForeignKey(MemberModel, on_delete=models.CASCADE, related_name='assigner', default=None)


class DiscountModel(models.Model):
    Simple_Discount_Choices = [
        ('Product', 'Product'),
        ('Category', 'Category'),
        ('Store', 'Store'),
        ('Composite', 'Composite'),
    ]
    Composite_Discount_Choices = [
        ('Max', 'Max'),
        ('Add', 'Add'),
        ('XOR', 'XOR'),
    ]
    discountID = models.IntegerField(primary_key=True)
    category = models.CharField(null=True, max_length=100)
    productID = models.IntegerField(null=True)
    percent = models.FloatField(null=True)
    type = models.CharField(max_length=100, choices=Simple_Discount_Choices)
    dID1 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='firstDiscountID', null=True)
    dID2 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='secondDiscountID', null=True)
    composite_type = models.CharField(max_length=100, choices=Composite_Discount_Choices, null=True)
    decide = models.IntegerField(choices=[(1, 1), (2, 2)], null=True)


class RuleModel(models.Model):
    Rule_Class = [
        ('DiscountComposite', 'DiscountComposite'),
        ('Price', 'Price'),
        ('PurchaseComposite', 'PurchaseComposite'),
        ('Quantity', 'Quantity'),
        ('Weight', 'Weight'),
    ]
    Rule_Kind = [
        ('Discount', 'Discount'),
        ('Purchase', 'Purchase'),
    ]
    Simple_Rule_Type = [
        ('Store', 'Store'),
        ('Category', 'Category'),
        ('Product', 'Product'),
    ]
    Composite_Rule_Type = [
        ('Or', 'Or'),
        ('And', 'And'),
    ]
    rule_class = models.CharField(max_length=100, choices=Rule_Class, null=True)
    ruleID = models.IntegerField(primary_key=True)
    rule_kind = models.CharField(max_length=100, choices=Rule_Kind)
    simple_rule_type = models.CharField(max_length=100, choices=Simple_Rule_Type, null=True)
    composite_rule_type = models.CharField(max_length=100, choices=Composite_Rule_Type, null=True)
    filter_type = models.CharField(max_length=100, null=True)
    at_least = models.IntegerField(null=True)
    at_most = models.IntegerField(null=True)
    ruleID1 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='firstRuleID', null=True)
    ruleID2 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='secondRuleID', null=True)


class DiscountRulesModel(models.Model):
    discountID = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True)
    ruleID = models.ForeignKey(RuleModel, on_delete=models.CASCADE)


class DiscountsInStoreModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    discountID = models.ForeignKey(DiscountModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('storeID', 'discountID',)


class RulesInStoreModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    ruleID = models.ForeignKey(RuleModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('storeID', 'ruleID',)


class NotificationModel(models.Model):
    userID = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField()
    read = models.BooleanField(default=False)


class LoginDateModel(models.Model):
    userID = models.UUIDField()
    username = models.TextField(null=True)
    date = models.DateTimeField(auto_now=True)


class BidOfferModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    productID = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    newPrice = models.FloatField()
    active = models.BooleanField(default=True)
    isAccepted = models.BooleanField(default=False)

class ReceiversOfBid(models.Model):
    bid = models.ForeignKey(BidOfferModel, on_delete=models.CASCADE)
    receiver = models.ForeignKey(MemberModel, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)

class SendersOfBid(models.Model):
    bid = models.ForeignKey(BidOfferModel, on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=True)


class OwnerAgreementModel(models.Model):
    assigner = models.ForeignKey(MemberModel, on_delete=models.CASCADE, related_name="Assigner")
    assignee = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    # permissionsOwners = models.ManyToManyField(MemberModel, related_name="permissionsOwners")
    active = models.BooleanField(default=True)
    isAccepted = models.BooleanField(default=False)


class ReceiversOfOwnerAgreement(models.Model):
    owner_agreement = models.ForeignKey(OwnerAgreementModel, on_delete=models.CASCADE)
    receiver = models.ForeignKey(MemberModel, on_delete=models.SET_NULL, null=True)
    accepted = models.BooleanField(default=False)






