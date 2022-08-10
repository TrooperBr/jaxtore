from django.forms import ModelForm
from times.models import Time
from django import forms

class TimeRegisterForm(ModelForm):
	def save(self,user, *args, **kwargs):
		self.admin = user
		super().save()
	class Meta:
		model = Time
		fields = ['name', 'instagram', 'twitter', 'youtube', 'email']