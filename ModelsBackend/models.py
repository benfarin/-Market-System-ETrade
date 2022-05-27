from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


# Create your models here.


class ProductModel(models.Model):
    product_id = models.IntegerField(primary_key=True)
    storeId = models.IntegerField()
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.CharField(max_length=100)
    weight = models.IntegerField()


class ProductKeyword(models.Model):
    product_id = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    keyword = models.CharField(max_length=100, null=True)

    class Meta:
        unique_together = ('product_id', 'keyword',)


class StoreTransactionModel(models.Model):
    storeId = models.IntegerField()
    storeName = models.CharField(max_length=100)
    transactionId = models.IntegerField(primary_key=True)
    paymentId = models.IntegerField()
    date = models.DateField()
    amount = models.IntegerField()


class ProductsInStoreTransactions(models.Model):
    transactionId = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE)
    productId = models.ForeignKey(ProductModel, on_delete=models.CASCADE)


class UserTransactionModel(models.Model):
    userID = models.UUIDField()
    transactionId = models.IntegerField(primary_key=True)
    paymentId = models.IntegerField()
    date = models.DateField()
    totalAmount = models.IntegerField()


class StoreTransactionsInUserTransactions(models.Model):
    userTransaction_id = models.ForeignKey(UserTransactionModel, on_delete=models.CASCADE)
    storeTransaction_id = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE)


class BagModel(models.Model):
    storeId = models.IntegerField(primary_key=True)


class ProductsInBagModel(models.Model):
    bag_ID = models.ForeignKey(BagModel, on_delete=models.SET_NULL, null=True)
    product_ID = models.ForeignKey(ProductModel, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()


class CartModel(models.Model):
    userid = models.UUIDField()
    bags = models.ForeignKey(BagModel, on_delete=models.CASCADE, null=True)


class UserModel(AbstractBaseUser):
    username = None
    userid = models.UUIDField(primary_key=True)
    cart = models.ForeignKey(CartModel, on_delete=models.CASCADE)
    transactions = models.ForeignKey(UserTransactionModel, on_delete=models.CASCADE, null=True)
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
    member_username = models.CharField(max_length=100)
    member_password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    bank = models.ForeignKey(BankModel, on_delete=models.CASCADE, null=True)
    is_admin = models.BooleanField(null=True)


class StoreModel(models.Model):
    storeID = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    founderId = models.ForeignKey(MemberModel, on_delete=models.CASCADE)
    bankAccount = models.ForeignKey(BankModel, on_delete=models.CASCADE)
    address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)
    # appointers: Dict[IMember: []] = {}  # Member : Members list   --This is a different model
    managers = models.ManyToManyField(MemberModel, related_name='managers')
    owners = models.ManyToManyField(MemberModel, related_name='owners')
    products: models.ManyToManyField(ProductModel)
    # productsQuantity = {}  # productId : quantity --This is a different model
    transactions = models.ForeignKey(StoreTransactionModel, on_delete=models.CASCADE, null=True)
    # discounts: {int: IDiscount} = {}
    # rules: {int: IRule} = {}


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

    class Meta:
        unique_together = ('userID', 'storeID',)


class StoreProductQuantityModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    productID = models.ForeignKey(ProductModel, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class StoreAppointersModel(models.Model):
    storeID = models.ForeignKey(StoreModel, on_delete=models.CASCADE)
    assingee = models.ManyToManyField(MemberModel, related_name='assingee')
    assigner = models.ManyToManyField(MemberModel, related_name='assigner')


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
    Rule_Type = [
        ('Store', 'Store'),
        ('Category', 'Category'),
        ('Product', 'Product'),
    ]
    Filter_Type = [
        (None, 'None'),
        ('Category', 'Category'),
        ('ProductID', 'ProductID'),
    ]
    rule_class = models.CharField(max_length=100, choices=Rule_Class, null=True)
    ruleID = models.IntegerField(primary_key=True)
    rule_kind = models.CharField(max_length=100, choices=Rule_Kind)
    rule_type = models.CharField(max_length=100, choices=Rule_Type)
    filter_type = models.CharField(max_length=100, choices=Filter_Type, null=True)
    at_least = models.IntegerField()
    at_most = models.IntegerField()
    ruleID1 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='firstRuleID', null=True)
    ruleID2 = models.ForeignKey('self', on_delete=models.CASCADE, related_name='secondRuleID', null=True)


class DiscountRulesModel(models.Model):
    discountID = models.ForeignKey(DiscountModel, on_delete=models.SET_NULL, null=True)
    ruleID = models.ForeignKey(RuleModel, on_delete=models.CASCADE)

