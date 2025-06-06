from django.db import models

# Create your models here.



class unet_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10)
    model_name = models.CharField(max_length=10)
    model_executed = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "unet_model"

        
        
class resNet_model(models.Model):
    S_No = models.AutoField(primary_key=True)
    model_accuracy = models.CharField(max_length=10)
    model_name = models.CharField(max_length=10)
    model_executed = models.CharField(max_length=10, null=True)

    class Meta:
        db_table = "resNet_model"


