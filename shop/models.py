from django.db import models

# Create your models here.


class Images(models.Model):
    image = models.ImageField(upload_to='shop_images/')

class Category(models.Model):
    name = models.CharField(max_length=255)
    relative = models.ManyToManyField("self",related_name="brothers")
    score = models.FloatField()
    class Meta:
        ordering = ['score','-pk']




class Item(models.Model):
    name = models.CharField(max_length=255)
    category_primary = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="primary_items")
    category_all = models.ManyToManyField(Category, related_name="all_items")
    description = models.TextField()
    buy_link = models.CharField(max_length=255)
    score = models.FloatField()

    def short_desk(self, number=64):
        return self.description[:number]

    def save(self, *args, **kwargs):
        self.categpry_all.add(self.category_primary)
        return super(Item, self).__init__(*args, **kwargs)


from django.contrib.auth.models import User
from datetime import datetime


class ItemView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    from_view = models.OneToOneField("self",on_delete=models.SET_NULL,  null=True)

class CategoryView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)
    from_view = models.OneToOneField("self",on_delete=models.SET_NULL, null=True)


class CardItens(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    qnt  = models.PositiveIntegerField()
    update = models.DateTimeField(auto_now_add=True)
    def save(self, *args, **kwargs):
        self.update = datetime.now()
        return super(CardItens, self).__init__(*args, **kwargs)


class Card(models.Model):
    itens = models.ManyToManyField(CardItens)
    selling = models.BooleanField(default=True)
    create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    @property
    def last_update(self):
       return self.selling.all()[0]











