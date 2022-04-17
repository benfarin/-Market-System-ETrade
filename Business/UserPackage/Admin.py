from Business.UserPackage.Member import Member
class Admin(Member):
    def __init__(self,userName, password, phone, address, bank):
        super().__init__(self,userName, password, phone, address, bank)


