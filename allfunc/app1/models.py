from django.db import models

    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='fichiers/')
    

class UploadedFile(models.Model):
    file = models.FileField(upload_to='stats/')     
    
class UploadedFile(models.Model):
    file = models.FileField(upload_to='upload/')
    
