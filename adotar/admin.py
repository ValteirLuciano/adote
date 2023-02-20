from django.contrib import admin
from .models import PedidoAdocao

# Register your models here.
class PedidoAdocaoAdmin(admin.ModelAdmin):
    list_display = ('id', 'pet', 'usuario', 'data', 'status')


admin.site.register(PedidoAdocao, PedidoAdocaoAdmin)
