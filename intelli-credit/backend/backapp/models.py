from django.db import models

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=500, default='Unknown Company')
    sector=models.CharField(max_length=250, default='General')
    gstin=models.CharField(max_length=200, null=True, blank=True)
    pan=models.CharField(max_length=500, null=True, blank=True)
    address=models.TextField()
    def __str__(self):
        return f"{self.name}-{self.sector}"


class History(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    file_key=models.CharField(max_length=250)
    timestamp=models.DateTimeField(auto_now=True)
    cam_content=models.TextField()
    def __str__(self):
        return f"{self.company}-{self.timestamp}"



