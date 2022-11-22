from django.forms import ModelForm
from .models import Job


class JobForm(ModelForm):

    class Meta:
        model = Job
        fields = ['employer', 'source', 'position', 'actiontaken','response1','response2','myfollowup1', 'myfollowup2']