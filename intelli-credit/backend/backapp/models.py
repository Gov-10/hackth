from django.db import models

# Create your models here.

class IntelliUser(models.Model):
    cognito_sub = models.CharField(max_length=500, unique=True)
    email = models.EmailField()
    created_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.email}"

class Company(models.Model):
    name=models.CharField(max_length=500, unique=True)
    handled_by=models.ForeignKey(IntelliUser, on_delete=models.CASCADE)
    gstin = models.CharField(max_length=100, unique=True)
    sector=models.CharField(max_length=100)
    pan=models.CharField(max_length=1000)
    address=models.TextField()
    def __str__(self):
        return f"{self.name}-> {self.handled_by.email}"

class History(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    handled_by=models.ForeignKey(IntelliUser, on_delete=models.CASCADE)
    file_key=models.TextField()
    job_id=models.CharField(max_length=100, unique=True)
    status=models.CharField(max_length=50)
    cam_content=models.TextField()
    timestamp=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.company.name}-{self.job_id}-{self.timestamp}"
