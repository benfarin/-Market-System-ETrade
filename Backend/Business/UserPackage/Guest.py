from Backend.Business.UserPackage.User import User
from ModelsBackend.models import UserModel
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

class Guest(User):
    def __init__(self, model=None):
        if model is None:
            super().__init__()
        else:
            self._model = model


