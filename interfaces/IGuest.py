from interface import implements, Interface
from interfaces.IUser import IUser

class Guest(Interface, IUser):
    pass
