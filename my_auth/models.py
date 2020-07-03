from django.db import models


class Verificate(models.Model):
    email = models.EmailField(unique=True)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
