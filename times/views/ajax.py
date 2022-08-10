from django.views import View
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from times.forms import TimeRegisterForm
class BaseAjax(View):
	def post(self, *args, **kwargs):
		return JsonResponse({'successful':True})

	def get(self, *args, **kwargs):
		return HttpResponse(404)


class TimeRegisterFormAjax(BaseAjax):
	def post(self, *args, **kwargs):
		if self.request.is_ajax():
			if self.request.user.is_authenticated :
				form = TimeRegisterForm()
				c = {
					'formhtml':render_to_string('teams/register-ajax.html', {'form': form}, self.request)
				}
				return JsonResponse(c)
			else:
				return JsonResponse({'successful':False,'erro':'Login Requisitado'})
		return HttpResponse(200)


from times.models import Time
class TimeRegisterAjax(BaseAjax):
	def post(self, *args, **kwargs):
		if self.request.is_ajax():
			if self.request.user.is_authenticated:
				form = TimeRegisterForm(self.request.POST)
				form.admin = self.request.user
				print(dir(form))
				Time(
					name=form.data['name'],
					instagram=form.data['instagram'],
					twitter=form.data['twitter'],
					youtube=form.data['youtube'],
					email=form.data['email'],
					#	phone=form.data['phone'],
					admin=self.request.user.player).save()
				return JsonResponse({'successful':200})
			else:
				return JsonResponse({'successful':False,'erro':'Login Requisitado'})
		return HttpResponse(200)

class SearchPlayerAjax(BaseAjax):
	def post(self, *args, **kwargs):
		pass