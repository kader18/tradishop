from django.urls import path 
from django.contrib.auth import views as auth_views
from . import views

app_name = "shop"

urlpatterns = [ 

    path('', views.acceuil, name='accueil'),
    path('boutique/', views.shop, name='shop'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('plats/', views.plats, name='plats'),
    


    path('panier/', views.panier, name='panier'),
    path('commande/', views.commande, name='commande'),
    path('update_article/', views.update_article, name='update_article'),
    path('traitement-commande/', views.traitementCommande, name="traitement_commande"),
    
    # Chatbot
    path('chatbot/', views.chatbot, name='chatbot'),
    
    # Aide
    path('aide/', views.aide, name='aide'),
    path('aide/commande/', views.aide_commande, name='aide_commande'),
    path('aide/livraison/', views.aide_livraison, name='aide_livraison'),
    path('aide/paiement/', views.aide_paiement, name='aide_paiement'),
    path('aide/compte/', views.aide_compte, name='aide_compte'),
    path('aide/retours/', views.aide_retours, name='aide_retours'),
    path('produit/<int:myid>/', views.details_produit, name='detail'),
    
    # Favoris
    path('favoris/', views.favoris_page, name='favoris'),
    path('toggle_favoris/', views.toggle_favoris, name='toggle_favoris'),


    path('register', views.register, name='register'),
    path('login', views.log_in, name='login'),
    path('logout', views.log_out, name='logout'),
    path('settings/', views.user_settings, name='settings'),
    
    path('password-reset/<str:uidb64>/<str:token>', views.activate_account_view, name='password_reset'),
    path("password_reset_view/", views.password_reset_request, name='password_reset_view'),
    path("password_reset_done/", views.password_reset_done, name='password_reset_done'),
    path("password_reset_confirm/<str:uidb64>/<str:token>/<str:email>/", views.password_reset_confirm, name='password_reset_confirm'),
    path("password_reset_complete/", views.password_reset_complete, name='password_reset_complete'),


    
]