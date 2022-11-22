from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )
    date = models.DateTimeField(auto_now_add= True)
    employer = models.CharField(max_length=100)
    source = models.CharField(max_length=100)
    position = models.CharField(max_length=100, null=True, blank=True)
    actiontaken = models.BooleanField(default=False)
    response1 = models.CharField(max_length=100, null=True, blank=True)
    response2 = models.CharField(max_length=100, null=True, blank=True)
    myfollowup1 = models.CharField(max_length=100, null=True, blank=True)
    myfollowup2 = models.CharField(max_length=100, null=True, blank=True)

    
    def __str__(self):
        return str(self.employer)
    
    class Meta:
        ordering = ['date']