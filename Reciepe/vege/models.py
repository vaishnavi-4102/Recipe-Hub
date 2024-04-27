from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Recipe(models.Model):
    user = models.ForeignKey(User, on_delete =models.SET_NULL, null = True, blank = True)
    recipe_name = models.CharField(max_length=100)
    recipe_description = models.TextField()
    recipe_image = models.ImageField(upload_to="recipe")
    def __str__(self):
        return f"{self.recipe_name}"
    

class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField