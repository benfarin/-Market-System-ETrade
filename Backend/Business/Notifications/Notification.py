import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()


class Notification:

    def __init__(self, model):
        self.__model = model

    def getNotificationText(self):
        return self.__model.text

    def getNotificationUser(self):
        return self.__model.userID
