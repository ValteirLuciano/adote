from django.contrib import admin

from .models import Raca, Tag, Pet

# Register your     models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'nome', 'estado', 'cidade', 'raca', 'status')

class RacaAdmin(admin.ModelAdmin):
    list_display = ('id', 'raca')

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag')


admin.site.register(Raca, RacaAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Pet, PetAdmin)
