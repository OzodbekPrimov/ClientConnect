from django.db import models

# Create your models here.


class Lead(models.Model):
    STATE_CHOICES = (
        ("PENDING", 'Pending'),
        ("REACHED_OUT", 'Reached Out')
    )
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    resume = models.FileField(upload_to="resumes/")
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    