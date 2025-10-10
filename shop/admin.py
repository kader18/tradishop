from django.contrib import admin
from .models import *


class ClientModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'email')


class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

class ProduitModelAdmin(admin.ModelAdmin):
    list_display = ('categorie', 'name', 'price', 'digital', 'image', 'date_ajout')    

class PlatsModelAdmin(admin.ModelAdmin):
    list_display = ( 'name', 'price', 'digital', 'description', 'image', 'date_ajout')    

class ProgrammePlatsModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')    


class CommandeModelAdmin(admin.ModelAdmin):
    list_display = ('client', 'complete', 'status', 'total_trans', 'transaction_id', 'date_commande')    

class CommandeArticleModelAdmin(admin.ModelAdmin):
    list_display = ('produit', 'commande', 'quantite', 'date_added')  

class AddressChippingModelAdmin(admin.ModelAdmin):
    list_display = ('client', 'commande', 'addresse', 'ville', 'zipcode', 'date_ajout')      

class FavorisModelAdmin(admin.ModelAdmin):
    list_display = ('client', 'produit', 'date_ajout')
    list_filter = ('date_ajout', 'client')
    search_fields = ('client__name', 'produit__name')


admin.site.register(Client, ClientModelAdmin)
admin.site.register(Produit, ProduitModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
admin.site.register(Plats, PlatsModelAdmin)
admin.site.register(ProgrammePlats, ProgrammePlatsModelAdmin)
admin.site.register(Commande, CommandeModelAdmin)
admin.site.register(CommandeArticle, CommandeArticleModelAdmin)
admin.site.register(AddressChipping, AddressChippingModelAdmin)
admin.site.register(Favoris, FavorisModelAdmin)

admin.site.site_title = "TradiShop Administration"
admin.site.site_header = "TradiShop - Administration"
admin.site.index_title = "Gestion du Site E-commerce"
