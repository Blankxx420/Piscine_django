from django.db import models

class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.CharField(max_length=255, blank=True)
    diameter = models.IntegerField(blank=True, null=True)
    orbital_period = models.IntegerField(blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    rotation_period = models.IntegerField(blank=True, null=True)
    surface_water = models.FloatField(blank=True, null=True)     
    terrain = models.CharField(max_length=255, blank=True)
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class People(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    birth_year = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=32, blank=True)
    eye_color = models.CharField(max_length=32, blank=True)
    hair_color = models.CharField(max_length=32, blank=True)
    height = models.IntegerField(blank=True, null=True)
    mass = models.FloatField(blank=True, null=True)
    
    homeworld = models.ForeignKey(
        Planets,
        to_field="name",
        on_delete=models.CASCADE,
        related_name="residents"
    )
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name