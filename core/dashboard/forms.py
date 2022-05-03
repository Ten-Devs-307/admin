from pyexpat import model
from django import forms
from .models import JobCategory


class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        exclude = ['created_at', 'updated_at', 'published']


class UpdateJobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        exclude = ['created_at', 'updated_at', 'published', 'image']
