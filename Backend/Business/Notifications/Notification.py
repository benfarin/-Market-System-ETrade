import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()


class Notification:

    def __init__(self, model):
        self.__model = model
        self.__reciever = self.__model.userID
        self.__text = self.__model.text

    def getNotificationText(self):
        return self.__text

    def getNotificationUser(self):
        return self.__reciever
