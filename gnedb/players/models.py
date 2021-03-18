#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
    
class Player(models.Model):
    
    full_name = models.CharField("Nom ",max_length=150, null=True)
    country = models.CharField("Pays ",max_length=150, null=True)
    height = models.IntegerField("Taille ", null=True)
    team = models.CharField("Équipe ",max_length=150, null=True)  
    ic   = models.CharField("Ind. Carac. ",max_length=10, null=True)
    imc = models.CharField("IMC ",max_length=10, null=True)
    last_update = models.DateTimeField("Last Update ",auto_now_add=True)
    age = models.IntegerField("Age ", null=True)
    defense = models.IntegerField("Defense ", null=True)
    freethrow = models.IntegerField("Lancer F. ", null=True)
    twopts = models.IntegerField("2pts ", null=True)
    threepts = models.IntegerField("3pts ", null=True)
    dribbling = models.IntegerField("Dribble ", null=True)
    passing = models.IntegerField("Passe ", null=True)
    speed = models.IntegerField("Vitesse ", null=True)
    footwork = models.IntegerField("Jeu de Jambe ", null=True)
    rebond = models.IntegerField("Rebond ", null=True)
    experience = models.IntegerField("Experience ", null=True)

