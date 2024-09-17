from django.db import models

class DiseaseDetection(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='disease_images/', blank=False)
    prediction = models.CharField(max_length=255)
    prob = models.CharField(max_length=255)
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Anonymous - {self.prediction}"
