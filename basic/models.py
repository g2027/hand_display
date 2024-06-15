from typing import Any, Dict
from django.db import models
from PIL import Image
import csv
import pandas as pd
from django.core.validators import MaxValueValidator, MinValueValidator
from .thickness_mapping import *
from tempfile import TemporaryFile



class RawMedidata(models.Model):
    SEX_CHOICES = [('2', 'Male'), ('1', 'Female'), ('3', 'Other')]
    RACE_CHOICES = [('1', 'White'),('2', 'Black'), ('3', "Asian"), ('4', "Native Hawaiian or Other Pacific Islander"), ('5', "American Indian or Alaskan Native"), ('6', "More than one race"), ('7', "Other"), ('8', "Unknown") ]
    AGE_CHOICES = [('1', "18-25"), ('2', "26-30"), ('3', "31-35"), ('4', "36-40"), ('5', "41-45"), ('6', "46-50"), ('7', "51-55"), ('8', "56-60"), ('9', "61-65"), ('10', "65-70"), ('11', "71-75"), ('12', ">75")]
    BMI_CHOICES = [('1', '<18.5'), ('2', "18.5-25"), ('3', "25-30"), ('4', ">30")]
    index = models.CharField(max_length=50, null=True,)
    sex = models.CharField(max_length=50, null=True, choices=SEX_CHOICES)
    race = models.CharField(max_length=50, null=True, choices=RACE_CHOICES)
    age = models.CharField(max_length=50, null=True, choices=AGE_CHOICES)
    bmi = models.CharField(max_length=50, null=True, choices=BMI_CHOICES)
    heatmap = models.ImageField(upload_to="heatmaps_indexed/")
    
    
    def attrs(self):
        attrs = [f.name for f in self._meta.get_fields()]
        attrs.pop(0)
        return attrs
    
    def attrs_values(self):
        attrs = self.attrs()
        attrs_values = []
        for i in attrs:
            object_field_value = getattr(self, i)
            attrs_values.append(object_field_value)
        return attrs_values
    
    def create_rawmedidata(self):
        
        basic_path = "heatmaps_indexed/"
        data = pd.read_csv("basic/data_for_query.csv")
        # print(data)
        for i, row in data.iterrows():
            med = RawMedidata()
            med.index = f'{int(row["index"]):03d}'
            med.sex = int(row["sex"])
            med.race = int(row["race"])
            age = row["age"]
            if age:
                age= int(age)
                if 18<= age <=25:
                    med.age = 1
                elif 26<=age<=30:
                    med.age = 2
                elif 31<= age <= 35:
                    med.age = 3
                elif 36<=age<=40:
                    med.age = 4
                elif 41<=age<=45:
                    med.age = 5
                elif 46<=age<=50:
                    med.age = 6
                elif 51<=age<=55:
                    med.age = 7
                elif 56<=age<=60:
                    med.age = 8
                elif 61<=age<=65:
                    med.age = 9
                elif 66<=age<=70:
                    med.age = 10
                elif 71<=age<=75:
                    med.age = 11
                elif 75<age:
                    med.age = 12
            else:
                med.age = 0
            bmi = row["bmi"]
            if bmi:
                bmi = float(bmi)
                if bmi<18.5:
                    bmi_str = '1'
                elif 18.5<=bmi<25:
                    bmi_str = '2'
                elif 25<=bmi<30:
                    bmi_str = '3'
                elif 30<=bmi:
                    bmi_str = '4'
            else:
                bmi_str = '0'
            med.bmi = int(bmi_str)
            # print(med.age, med.sex, med.race, med.bmi)
            med.heatmap = basic_path + med.index +'.png'
            med.save()
        
        
        
       

                
        

class Coords(models.Model):
    x_coord = models.IntegerField(verbose_name='x_coord', validators=[
            MaxValueValidator(99),
            MinValueValidator(0)
            ]
                                  )
    y_coord = models.IntegerField(verbose_name='y_coord', validators=[
        MaxValueValidator(39),
        MinValueValidator(0)
    ])
    
class CompiledImages(models.Model):
    filtered_images = models.ImageField(upload_to='temp/')
    
    

    

# med = RawMedidata()
# med.create_rawmedidata()
         
# Create your models here.





