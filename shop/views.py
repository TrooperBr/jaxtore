from django.shortcuts import render
from django.views import View
from .models import (
    Category,
)

class CategoryView(View):
    def get(self, slug, *args, **kwargs):
        context = {
                "itens":Category.objects.filter(slug=slug)
            }
        return render(self.request, 'shop/categoryview.html', context=context)

class ItemVew(View):
    def get(self, *args, **kwargs):
        context = {
                "relatead_itens":[],
                "item":None
            }
        return render(self.request, 'shop/categoryview.html', context=context)

# Create your views here.
class ShopHome(View):
    def get(self, *args, **kwargs):
        context = {
                "best_products":[],
                "user_categorys":[],
                "user_products_list":[]
            }
        return render(self.request, 'shop/categoryview.html', context=context)