from Business.UserPackage.Member import Member


class SystemManager(Member):
    def __init__(self, userName, password, phone, address, bank):
        super().__init__(userName, password, phone, address, bank)
