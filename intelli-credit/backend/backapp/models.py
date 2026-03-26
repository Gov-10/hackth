from django.db import models

# Create your models here.

class IntelliUser(models.Model):
    cognito_sub = models.CharField(max_length=500, unique=True)
    email = models.EmailField()
    created_at=models.DateTimeField(auto_now_add=True)
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
    input_file_key= models.CharField(max_length=200)
    cam_file_key=models.CharField(max_length=200, null=True, blank=True)
    job_id=models.CharField(max_length=100, unique=True, db_index=True)
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("processing", "Processing"),
        ("researching", "Researching"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default="queued")
    cam_content=models.TextField(null=True, blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.company.name}-{self.job_id}-{self.timestamp}"
