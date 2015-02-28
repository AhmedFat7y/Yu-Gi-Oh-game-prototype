from django.contrib import admin
from yugioh.mainapp.models import IconType, CardAttribute
# Register your models here.

admin.site.register(IconType)
admin.site.register(CardAttribute)
admin.site.register(CardType)