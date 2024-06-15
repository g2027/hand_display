from django import forms
from .models import *
from django.forms import formset_factory
class MedidataForm(forms.ModelForm):
    
    SEX_CHOICES = [('None Specified', '0'), ('Male', '1'), ('Female', '2'), ('Other', '3')]
    RACE_CHOICES = [('None Specified', '0'), ('White', '1'),('Black', "2"), ("Asian", "3"), ("Native Hawaiian or Other Pacifc Islander", '4'), ("American Indian or Alaskan Native", "5"), ("More than one race", "6"), ("Other", "7"), ("Unkown", "8") ]
    AGE_CHOICES = [('None Specified', '0'), ("18-25", "1"), ("26-30", "2"), ("31-35", "3"), ("36-40", "4"), ("41-45", "5"), ("46-50", "6"), ("51-55", "7"), ("56-60", "8"), ("61-65", "9"), ("65-70", "10"), ("71-75", "11"), ("75+", "12")]
    BMI_CHOICES = [('None Specified', '0'), ('<18.5', "1"), ("18.5-25", "2"), ("25-30", "3"), (">30", "4")]
    sex = models.CharField(max_length=50, null=False, choices=SEX_CHOICES)
    race = models.CharField(max_length=50, null=False, choices=RACE_CHOICES)
    age = models.CharField(max_length=50, null=False, choices=AGE_CHOICES)
    bmi = models.CharField(max_length=50, null=False, choices=BMI_CHOICES)
    heatmap = models.ImageField(upload_to="avg_heatmaps_indexed/")
    
    class Meta:
        model = RawMedidata
        fields = [
            'race',
            'sex',
            'age',
            'bmi',
        ]
    
    
class CoordForm(forms.ModelForm):
    x_coord = models.IntegerField(verbose_name='x_coord', null=True, validators=[
            MaxValueValidator(99),
            MinValueValidator(0)
            ]
              )
    y_coord = models.IntegerField(verbose_name='y_coord', null=True, validators=[
        MaxValueValidator(39),
        MinValueValidator(0)
    ])
    
    class Meta:
        model = Coords
        fields= [
            'x_coord',
            'y_coord',
        ]
        



