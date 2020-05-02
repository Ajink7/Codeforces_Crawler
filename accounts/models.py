from django.db import models

# Create your models here.
from django.contrib import auth

class User(auth.models.User):
    def __str__(self):
        return "@.{}".format(self.username)
