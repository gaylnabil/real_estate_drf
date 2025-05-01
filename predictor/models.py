from django.db import models

# Create your models here.
class CSVFile(models.Model):
    file = models.FileField(upload_to='csv_uploads/', max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"CSV File uploaded at {self.uploaded_at}"