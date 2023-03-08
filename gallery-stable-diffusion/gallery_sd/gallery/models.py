from django.db import models

# Create your models here.
class pics(models.Model):
    no = models.IntegerField(primary_key=True)
    cp = models.CharField(max_length=500)
    pic_name = models.CharField(max_length=500)
    prompt = models.CharField(max_length=500)
    n_prompt = models.CharField(max_length=500)
    cfg_scale = models.CharField(max_length=500)
    steps = models.CharField(max_length=500)
    sampler = models.CharField(max_length=500)
    seed = models.CharField(max_length=500)
    lora = models.CharField(max_length=500)
    