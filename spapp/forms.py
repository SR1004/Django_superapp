from django import forms
from .models import Collection

class coll(forms.ModelForm):
    class Meta:
        model=Collection
        fields=['Study_Name','Study_Description','Study_Phase','Sponser_Name']
