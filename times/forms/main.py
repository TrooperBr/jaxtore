from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from times.models import PlayerConvit

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

from times.models import Rank, Player

from datetime import datetime

class PlayerForm(forms.ModelForm):
	nick = forms.CharField()
	birth = forms.DateField(
		initial=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
		input_formats=['%d/%m/%Y %H:%M'],
		widget=forms.DateTimeInput(attrs={
			'class': 'form-control datetimepicker-input',
			'data-target': '#datetimepicker1'
			}
		)
	)
	#ranking = forms.ModelChoiceField(
	#	queryset=Rank.objects.all()
	#)
	class Meta:
		model = Player
		fields = ['nick','birth']
