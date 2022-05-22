from Backend.Business.UserPackage.User import User


class Guest(User):
    def __init__(self):
        super().__init__()
