from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from .models import *
from django.http import JsonResponse
import json
import re
from datetime import datetime
from django.contrib.auth.decorators import login_required
from .utils import commandeAnonyme, data_cookie, data_favoris, panier_cookie, pargination, send_email_with_template

from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from django.core.validators import validate_email
from django.db.models.query_utils import Q
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.utils import timezone


# Validation mail
from django.conf import settings
from django.core.mail import send_mail, EmailMessage, BadHeaderError
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .token import TokenGeneretor
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from django.utils import translation
from django.conf import settings
from django.http import JsonResponse

generate_token = TokenGeneretor()


def acceuil(request, *args, **kwargs):
    """ vue principal """

    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    category = request.GET.get('categorie')
    commande = data['commande']


    
    categoriess = categories[:3]
    
    produit_list = []

    nombre_produits = 0

    if category == None:
        produits = Produit.objects.order_by('-price').filter(is_published=True)
    else:
        category = get_object_or_404(Category, name=category)
        produits = Produit.objects.filter(categorie=category)
        nombre_produits = len(produits)

    nombre_article = data['nombre_article']
    articles = data['articles']

    print(f"nombre article {nombre_article} ")

    items = pargination(request, produits)  

    context = {
        'commande': commande,
        'articles':articles,
        'nombre_produits':nombre_produits,
        'categories': categories,
        'categoriess': categoriess,
        'nombre_article': nombre_article,
        'items': items,
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris'],
        'panier': data['panier']
    }

    for category in categoriess:
        produits = Produit.objects.filter(categorie=category)
        produit_list.append(produits)

    context['produits'] = produit_list

    print(produit_list[:8])
    
    context['produits_home'] = produit_list[:8]

    nombre_produits_par_categorie = {}
    for category in categories:
        nombre_produits_par_categorie[category] = Produit.objects.filter(categorie=category).count()
    

    context['nombre_produits_par_categorie'] = nombre_produits_par_categorie

    return render(request, 'shop/acceuil.html', context)


def shop(request, *args, **kwargs):
    """ vue shop """

    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    commande = data['commande']
    
    # Récupérer les paramètres de filtrage
    category = request.GET.get('categorie')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    price_range = request.GET.get('price_range')
    search = request.GET.get('search')
    sort = request.GET.get('sort', 'price_desc')

    # Filtrer par catégorie
    if category == None:
        produits = Produit.objects.filter(is_published=True)
    else:
        category_obj = get_object_or_404(Category, name=category)
        produits = Produit.objects.filter(categorie=category_obj, is_published=True)

    # Filtrer par prix
    if min_price and max_price:
        try:
            min_price = float(min_price)
            max_price = float(max_price)
            produits = produits.filter(price__gte=min_price, price__lte=max_price)
        except (ValueError, TypeError):
            pass
    elif price_range:
        # Gestion des plages de prix prédéfinies
        if price_range == '0-5000':
            produits = produits.filter(price__gte=0, price__lte=5000)
        elif price_range == '5000-20000':
            produits = produits.filter(price__gte=5000, price__lte=20000)
        elif price_range == '20000-45000':
            produits = produits.filter(price__gte=20000, price__lte=45000)
        elif price_range == '45000-100000':
            produits = produits.filter(price__gte=45000, price__lte=100000)
        elif price_range == '100000+':
            produits = produits.filter(price__gte=100000)

    # Filtrer par recherche
    if search:
        produits = produits.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(categorie__name__icontains=search)
        )

    # Trier selon le paramètre de tri
    if sort == 'price_asc':
        produits = produits.order_by('price')
    elif sort == 'price_desc':
        produits = produits.order_by('-price')
    elif sort == 'name':
        produits = produits.order_by('name')
    elif sort == 'date':
        produits = produits.order_by('-date_ajout')
    else:
        produits = produits.order_by('-price')  # Par défaut

    nombre_article = data['nombre_article']
    articles = data['articles']

    items = pargination(request, produits)

    # Compter les produits par plage de prix pour l'affichage
    price_counts = {
        'all': Produit.objects.filter(is_published=True).count(),
        'range_0_5000': Produit.objects.filter(is_published=True, price__gte=0, price__lte=5000).count(),
        'range_5000_20000': Produit.objects.filter(is_published=True, price__gte=5000, price__lte=20000).count(),
        'range_20000_45000': Produit.objects.filter(is_published=True, price__gte=20000, price__lte=45000).count(),
        'range_45000_100000': Produit.objects.filter(is_published=True, price__gte=45000, price__lte=100000).count(),
        'range_100000_plus': Produit.objects.filter(is_published=True, price__gte=100000).count(),
    }

    context = {
        'commande': commande,
        'articles': articles,
        'produits': items,
        'categories': categories,
        'nombre_article': nombre_article,
        'price_counts': price_counts,
        'current_category': category,
        'current_price_range': price_range,
        'current_search': search,
        'current_sort': sort,
        'min_price': min_price,
        'max_price': max_price,
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris'],
        'panier': data['panier']
    }

    return render(request, 'shop/boutique.html', context)

def plats(request, *args, **kwargs):
    """ vue shop """
    categories = Category.objects.all()
    programme = ProgrammePlats.objects.all()
    data = data_cookie(request)
    commande = data['commande']
    
   
    category = request.GET.get('categorie')


    if category == None:
        produits = Produit.objects.order_by('-price').filter(is_published=True)
    else:
        category = get_object_or_404(Category, name=category)
        produits = Produit.objects.filter(categorie=category)

    nombre_article = data['nombre_article']
    articles = data['articles']

    
    plats = Plats.objects.order_by('-price').filter(is_published=True)
    
    items = pargination(request, plats)


    context = {
        'commande': commande,
        'plats':plats,
        'articles':articles,
        'produits':produits,
        'categories':categories,
        'programme': programme,
        'nombre_article': nombre_article
    }

    context['plats'] = items

    return render(request, 'shop/plats.html', context)


def contact(request, *args, **kwargs):
    context = {}

    if request.method == 'POST':
        email = request.POST.get('emailcontact')
        subject = request.POST.get('subject')
        description = request.POST.get('description')
        
        if email and subject and description:
            try:
                to_email = "kadersoro18@gmail.com"
                send_mail(subject, description, email, [to_email], fail_silently=False)
                messages.success(request, 'Votre message a été envoyé avec succès!')
            except Exception as e:
                messages.error(request, f'Erreur lors de l\'envoi du message: {str(e)}')
        else:
            messages.error(request, 'Veuillez remplir tous les champs.')
    
    return render(request, 'shop/contact.html', context)

def register(request, *args, **kwargs):
    """Vue d'inscription améliorée avec validation renforcée"""
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        firstname = request.POST.get('firstname', '').strip()
        lastname = request.POST.get('lastname', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')

        # Validation des champs requis
        if not all([username, firstname, lastname, email, password, repassword]):
            messages.error(request, "Tous les champs sont obligatoires.")
            return render(request, 'auth/register.html', context)

        # Validation du nom d'utilisateur
        if len(username) < 3 or len(username) > 30:
            messages.error(request, "Le nom d'utilisateur doit contenir entre 3 et 30 caractères.")
            return render(request, 'auth/register.html', context)
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            messages.error(request, "Le nom d'utilisateur ne peut contenir que des lettres, chiffres et underscores.")
            return render(request, 'auth/register.html', context)

        # Validation des noms
        if len(firstname) < 2 or len(firstname) > 30:
            messages.error(request, "Le prénom doit contenir entre 2 et 30 caractères.")
            return render(request, 'auth/register.html', context)
        
        if len(lastname) < 2 or len(lastname) > 30:
            messages.error(request, "Le nom doit contenir entre 2 et 30 caractères.")
            return render(request, 'auth/register.html', context)

        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', firstname):
            messages.error(request, "Le prénom ne peut contenir que des lettres.")
            return render(request, 'auth/register.html', context)
        
        if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', lastname):
            messages.error(request, "Le nom ne peut contenir que des lettres.")
            return render(request, 'auth/register.html', context)

        # Validation de l'email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, "Veuillez entrer une adresse email valide.")
            return render(request, 'auth/register.html', context)

        # Validation du mot de passe
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return render(request, 'auth/register.html', context)
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', password):
            messages.error(request, "Le mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre et un caractère spécial.")
            return render(request, 'auth/register.html', context)

        if password != repassword:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'auth/register.html', context)

        # Vérification de l'unicité
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'auth/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse email est déjà utilisée.")
            return render(request, 'auth/register.html', context)

        try:
            # Création de l'utilisateur
            my_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=firstname,
                last_name=lastname,
                is_active=True  # Activer directement pour simplifier
            )

            # Créer le profil client associé
            from .models import Client
            Client.objects.create(user=my_user)

            messages.success(request, f'Compte créé avec succès! Bienvenue {firstname}!')
            
            # Auto-login après inscription
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('shop:accueil')
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la création du compte: {str(e)}")
            return render(request, 'auth/register.html', context)
    
    return render(request, 'auth/register.html', context)


def activate_account_view(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Votre compte a été activié avec succès .")

    else:
        messages.error(request, "Le lien d'activation est invalide")

    return redirect('shop:login')

def log_in(request, *args, **kwargs):
    """Vue de connexion améliorée avec support email et gestion d'erreurs"""
    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me', False)

        if not username_or_email or not password:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'auth/login.html')

        # Essayer de se connecter avec le nom d'utilisateur
        user = authenticate(username=username_or_email, password=password)
        
        # Si échec, essayer avec l'email
        if user is None and '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Gestion de "Se souvenir de moi"
                if not remember_me:
                    # Session expire à la fermeture du navigateur
                    request.session.set_expiry(0)
                else:
                    # Session expire dans 30 jours
                    request.session.set_expiry(30 * 24 * 60 * 60)
                
                messages.success(request, f'Bienvenue {user.first_name}!')
                
                # Redirection vers la page précédente ou l'accueil
                next_page = request.GET.get('next', 'shop:accueil')
                return redirect(next_page)
            else:
                messages.error(request, 'Votre compte est désactivé. Veuillez contacter l\'administrateur.')
        else:
            messages.error(request, 'Nom d\'utilisateur/email ou mot de passe incorrect.')
            return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')

def log_out(request, *args, **kwargs):
    logout(request)
    return redirect('shop:accueil')

def password_reset_done(request, *args, **kwargs):
    return render(request, 'password_reset_done.html')

def password_reset_request(request, *args, **kwargs):
    """Vue de demande de réinitialisation de mot de passe améliorée"""
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        
        if not email:
            messages.error(request, 'Veuillez entrer votre adresse email.')
            return render(request, 'password_reset.html')
        
        # Validation de l'email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messages.error(request, 'Veuillez entrer une adresse email valide.')
            return render(request, 'password_reset.html')
        
        try:
            user = User.objects.get(email=email)
            
            # Générer le token de réinitialisation
            domain = get_current_site(request).domain
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = generate_token.make_token(user)
            
            # Préparer l'email
            subject = "Réinitialisation de votre mot de passe - Tradishop"
            template_name = 'auth/password_reset_email.html'
            
            context = {
                "user": user,
                "user_name": f"{user.first_name} {user.last_name}",
                "domain": domain,
                "uid": uid,
                "token": token,
                "protocol": 'https' if request.is_secure() else 'http'
            }
            
            # Envoyer l'email
            try:
                send_email_with_template(subject, template_name, context, user.email, settings.EMAIL_HOST_USER)
                messages.success(request, f'Un email de réinitialisation a été envoyé à {email}. Vérifiez votre boîte de réception.')
            except Exception as e:
                # En cas d'erreur d'envoi, afficher le lien en mode développement
                reset_url = f"{request.scheme}://{domain}/password_reset_confirm/{uid}/{token}/{email}/"
                messages.success(request, f'Email envoyé ! (Mode dev: {reset_url})')
                print(f"Erreur envoi email: {str(e)}")
            
            return redirect('shop:password_reset_done')
            
        except User.DoesNotExist:
            # Ne pas révéler si l'email existe ou non pour des raisons de sécurité
            messages.success(request, 'Si cette adresse email est associée à un compte, vous recevrez un email de réinitialisation.')
            return redirect('shop:password_reset_done')
        except Exception as e:
            messages.error(request, f'Une erreur est survenue: {str(e)}')
            return render(request, 'password_reset.html')
    
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token, email, *args, **kwargs):
    """Vue de confirmation de réinitialisation de mot de passe améliorée"""
    
    # Vérifier la validité du token avant d'afficher le formulaire
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(email=email, pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is None or not generate_token.check_token(user, token):
        messages.error(request, "Le lien de réinitialisation est invalide ou a expiré.")
        return redirect('shop:password_reset_view')
    
    if request.method == "POST":
        password = request.POST.get('password', '')
        repassword = request.POST.get('repassword', '')

        # Validation des champs
        if not password or not repassword:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'password_reset_confirm.html')

        if password != repassword:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'password_reset_confirm.html')

        # Validation de la force du mot de passe
        if len(password) < 8:
            messages.error(request, "Le mot de passe doit contenir au moins 8 caractères.")
            return render(request, 'password_reset_confirm.html')
        
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]', password):
            messages.error(request, "Le mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre et un caractère spécial.")
            return render(request, 'password_reset_confirm.html')

        try:
            # Modifier le mot de passe de l'utilisateur
            user.set_password(password)
            user.save()
            
            # Invalider toutes les sessions existantes pour forcer une nouvelle connexion
            from django.contrib.sessions.models import Session
            Session.objects.filter(expire_date__gte=timezone.now()).delete()
            
            messages.success(request, "Votre mot de passe a été réinitialisé avec succès. Vous pouvez maintenant vous connecter.")
            return redirect('shop:password_reset_complete')
            
        except Exception as e:
            messages.error(request, f"Une erreur est survenue lors de la réinitialisation: {str(e)}")
            return render(request, 'password_reset_confirm.html')
    
    return render(request, 'password_reset_confirm.html')

def password_reset_complete(request, *args, **kwargs):
    return render(request, "password_reset_complete.html")

@login_required
def user_settings(request, *args, **kwargs):
    """Page de paramètres utilisateur"""
    user = request.user
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_profile':
            # Mise à jour du profil
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            
            # Validation
            if not all([first_name, last_name]):
                messages.error(request, 'Tous les champs sont obligatoires.')
                return render(request, 'auth/settings.html', {'user': user})
            
            if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', first_name):
                messages.error(request, 'Le prénom ne peut contenir que des lettres.')
                return render(request, 'auth/settings.html', {'user': user})
            
            if not re.match(r'^[a-zA-ZÀ-ÿ\s]+$', last_name):
                messages.error(request, 'Le nom ne peut contenir que des lettres.')
                return render(request, 'auth/settings.html', {'user': user})
            
            # Mettre à jour les informations (sans l'email)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            messages.success(request, 'Vos informations ont été mises à jour avec succès.')
            return redirect('shop:settings')
        
        elif action == 'change_password':
            # Changement de mot de passe
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            # Validation
            if not all([current_password, new_password, confirm_password]):
                messages.error(request, 'Tous les champs sont obligatoires.')
                return render(request, 'auth/settings.html', {'user': user})
            
            # Vérifier le mot de passe actuel
            if not user.check_password(current_password):
                messages.error(request, 'Le mot de passe actuel est incorrect.')
                return render(request, 'auth/settings.html', {'user': user})
            
            # Validation du nouveau mot de passe
            if len(new_password) < 8:
                messages.error(request, 'Le nouveau mot de passe doit contenir au moins 8 caractères.')
                return render(request, 'auth/settings.html', {'user': user})
            
            if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', new_password):
                messages.error(request, 'Le nouveau mot de passe doit contenir au moins une majuscule, une minuscule, un chiffre et un caractère spécial.')
                return render(request, 'auth/settings.html', {'user': user})
            
            if new_password != confirm_password:
                messages.error(request, 'Les nouveaux mots de passe ne correspondent pas.')
                return render(request, 'auth/settings.html', {'user': user})
            
            # Changer le mot de passe
            user.set_password(new_password)
            user.save()
            
            # Reconnecter l'utilisateur avec le nouveau mot de passe
            from django.contrib.auth import update_session_auth_hash
            update_session_auth_hash(request, user)
            
            messages.success(request, 'Votre mot de passe a été changé avec succès.')
            return redirect('shop:settings')
    
    return render(request, 'auth/settings.html', {'user': user})

def panier(request, *args, **kwargs):
    """ panier """
    categories = Category.objects.all()

    data = data_cookie(request)
    favoris_data = data_favoris(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles':articles,
        'categories':categories,
        'commande':commande,
        'nombre_article':nombre_article,
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }

    return render(request, 'shop/panier.html', context)


def commande(request, *args, **kwargs):
    """ Commande """

    categories = Category.objects.all()

    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    context = {
        'articles':articles,
        'categories':categories,
        'commande':commande,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/commande.html', context)


# Chatbot
def chatbot(request, *args, **kwargs):
    """ Vue pour le chatbot """
    if request.method == 'POST':
        message = request.POST.get('message', '').strip()
        
        # Réponses prédéfinies du chatbot
        responses = {
            'bonjour': 'Bonjour ! Comment puis-je vous aider aujourd\'hui ?',
            'salut': 'Salut ! Je suis là pour vous aider avec vos questions sur TradiShop.',
            'aide': 'Je peux vous aider avec les commandes, la livraison, les paiements, votre compte et les retours. Que souhaitez-vous savoir ?',
            'commande': 'Pour passer une commande, ajoutez les produits à votre panier puis procédez au checkout. Vous pouvez aussi consulter notre page d\'aide.',
            'livraison': 'Nos délais de livraison varient selon votre localisation. En général, comptez 1-7 jours ouvrés.',
            'paiement': 'Nous acceptons Mobile Money, cartes bancaires, virement et paiement à la livraison.',
            'compte': 'Pour créer un compte, cliquez sur "Connexion" puis "Inscription".',
            'retour': 'Vous avez 14 jours pour retourner un produit non utilisé.',
            'contact': 'Vous pouvez nous contacter au +225 07 799 802 35 ou par email à support@tradishop.com',
            'prix': 'Nos prix sont affichés en FCFA. Vous pouvez filtrer par prix dans la boutique.',
            'produit': 'Nous vendons des produits traditionnels africains : vêtements, bijoux, chaussures, et plus encore.',
            'merci': 'De rien ! N\'hésitez pas si vous avez d\'autres questions.',
            'au revoir': 'Au revoir ! Bonne journée et à bientôt sur TradiShop !',
            'tradishop': 'TradiShop est votre boutique en ligne spécialisée dans les produits traditionnels africains.',
            'boutique': 'Notre boutique propose une large gamme de produits : vêtements, bijoux, chaussures, accessoires et plus encore.',
            'panier': 'Pour ajouter un produit au panier, cliquez sur le bouton "Ajouter au panier" sur la page du produit.',
        }
        
        # Réponse simple basée sur les mots-clés
        response_text = "Désolé, je n'ai pas compris votre question. Pouvez-vous reformuler ?"
        
        for keyword, response in responses.items():
            if keyword in message.lower():
                response_text = response
                break
        
        return JsonResponse({'response': response_text})
    
    return JsonResponse({'response': 'Bonjour ! Comment puis-je vous aider ?'})


def change_language(request):
    """Vue pour changer la langue"""
    if request.method == 'POST':
        language = request.POST.get('language', 'fr')
        if language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            request.session[translation.LANGUAGE_SESSION_KEY] = language
            return JsonResponse({'success': True, 'language': language})
    return JsonResponse({'success': False})


def change_currency(request):
    """Vue pour changer la devise"""
    if request.method == 'POST':
        currency = request.POST.get('currency', 'FCFA')
        if currency in settings.CURRENCIES:
            request.session['currency'] = currency
            return JsonResponse({'success': True, 'currency': currency})
    return JsonResponse({'success': False})


def get_currency_info(request):
    """Récupérer les informations de devise"""
    currency = request.session.get('currency', 'FCFA')
    currency_info = settings.CURRENCIES.get(currency, settings.CURRENCIES['FCFA'])
    return JsonResponse(currency_info)


# Page d'aide
def aide(request, *args, **kwargs):
    """ Page d'aide """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide.html', context)


# Pages d'aide spécialisées
def aide_commande(request, *args, **kwargs):
    """ Aide pour les commandes """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide_commande.html', context)


def aide_livraison(request, *args, **kwargs):
    """ Aide pour la livraison """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide_livraison.html', context)


def aide_paiement(request, *args, **kwargs):
    """ Aide pour les paiements """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide_paiement.html', context)


def aide_compte(request, *args, **kwargs):
    """ Aide pour le compte utilisateur """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide_compte.html', context)


def aide_retours(request, *args, **kwargs):
    """ Aide pour les retours et remboursements """
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/aide_retours.html', context)




def update_article(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return JsonResponse("Veuillez vous connecter", safe=False)
    
    # Récupérer les données selon la méthode de requête
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            produit_id = data['produit_id']
            action = data['action']
        else:
            produit_id = request.POST.get('produit_id')
            action = request.POST.get('action')
    else:
        return JsonResponse("Méthode non autorisée", safe=False)

    try:
        client = request.user.client
    except:
        client, created = Client.objects.get_or_create(user=request.user)

    try:
        produit = Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return JsonResponse("Produit non trouvé", safe=False)

    commande, created = Commande.objects.get_or_create(client=client, complete=False)

    # Récupérer ou créer l'article de commande
    try:
        commande_article = CommandeArticle.objects.get(commande=commande, produit=produit)
    except CommandeArticle.DoesNotExist:
        commande_article = CommandeArticle.objects.create(commande=commande, produit=produit, quantite=0)
    except CommandeArticle.MultipleObjectsReturned:
        # En cas de doublons, garder le premier et supprimer les autres
        articles = CommandeArticle.objects.filter(commande=commande, produit=produit)
        commande_article = articles.first()
        articles.exclude(id=commande_article.id).delete()

    if action == 'add':
        commande_article.quantite += 1

    if action == 'remove':
        commande_article.quantite -= 1

    commande_article.save()

    if action == 'delete':
        commande_article.delete()
        return JsonResponse("Article supprimé", safe=False)

    if commande_article.quantite <= 0:
        commande_article.delete()
        return JsonResponse("Article supprimé", safe=False)

    return JsonResponse("Article ajouté", safe=False)


def traitementCommande(request, *args, **kwargs):
    """ traitement,  validation de la com;ande  et verification de l'integrite des donnees(detection de fraude)"""

    STATUS_TRANSACTION = ['ACCEPTED', 'COMPLETED', 'SUCESS']
    
    transaction_id = datetime.now().timestamp()

    data = json.loads(request.body)

    print(data)

    if request.user.is_authenticated:

        client = request.user.client

        commande, created = Commande.objects.get_or_create(client=client, complete=False)


    else:
        client, commande = commandeAnonyme(request, data)

    total = float(data['form']['total'])

    commande.transaction_id = data['payment_info']['transaction_id']

    commande.total_trans = total

    if commande.get_panier_total == total:

        commande.complete = True
        commande.status = data['payment_info']['status']

    else:
        commande.status = "REFUSED"
        commande.save()
        
        return JsonResponse("Attention!!! Traitement Refuse Fraude detecte!", safe=False)

    commande.save()    
    
    if not commande.status in STATUS_TRANSACTION:
        return JsonResponse("Désolé, le paiement a échoué, veuillez réessayer")    

  

    if commande.produit_physique:

        AddressChipping.objects.create(
            client=client,
            commande=commande,
            addresse = data['shipping']['address'],
            ville=data['shipping']['city'],
            zipcode=data['shipping']['zipcode']
        )



    return JsonResponse("Votre paiement a été effectué avec succès, vous recevrez votre commande dans un instant !", safe=False)


def about(request, *args, **kwargs):
    """ vue principale """

    produits = Produit.objects.all()
    categories = Category.objects.all()
    data = data_cookie(request)
    nombre_article = data['nombre_article']
    commande = data['commande']
    articles = data['articles']

    context = {
        "articles": articles,
        "commande": commande,
        'produits': produits,
        'categories': categories,
        'nombre_article': nombre_article
    }

    return render(request, 'shop/about.html', context)


def details_produit(request, myid, *args, **kwargs):
    """Vue de chaque produits"""
    try:
        product_object = get_object_or_404(Produit, id=myid, is_published=True)
    except Produit.DoesNotExist:
        messages.error(request, "Produit non trouvé")
        return redirect('shop:accueil')

    categories = Category.objects.all()
    data = data_cookie(request)
    articles = data['articles']
    commande = data['commande']
    nombre_article = data['nombre_article']

    # Produits similaires de la même catégorie
    produits_similaires = Produit.objects.filter(
        categorie=product_object.categorie, 
        is_published=True
    ).exclude(id=myid)[:4]

    context = {
        'commande': commande,
        'articles': articles,
        'categories': categories,
        'nombre_article': nombre_article,
        'product_object': product_object,
        'produits_similaires': produits_similaires
    }

    return render(request, 'shop/detail.html', context)


def toggle_favoris(request, *args, **kwargs):
    """Ajouter/Retirer un produit des favoris"""
    if not request.user.is_authenticated:
        return JsonResponse("Veuillez vous connecter pour ajouter aux favoris", safe=False)
    
    # Récupérer les données selon la méthode de requête
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            produit_id = data['produit_id']
        else:
            produit_id = request.POST.get('produit_id')
    else:
        return JsonResponse("Méthode non autorisée", safe=False)
    
    try:
        client = request.user.client
    except:
        client, created = Client.objects.get_or_create(user=request.user)
    
    try:
        produit = Produit.objects.get(id=produit_id)
    except Produit.DoesNotExist:
        return JsonResponse("Produit non trouvé", safe=False)
    
    # Vérifier si le produit est déjà dans les favoris
    favori, created = Favoris.objects.get_or_create(client=client, produit=produit)
    
    if created:
        return JsonResponse("Produit ajouté aux favoris", safe=False)
    else:
        favori.delete()
        return JsonResponse("Produit retiré des favoris", safe=False)


def favoris_page(request, *args, **kwargs):
    """Page des favoris"""
    if not request.user.is_authenticated:
        messages.error(request, "Veuillez vous connecter pour voir vos favoris")
        return redirect('shop:login')
    
    categories = Category.objects.all()
    data = data_cookie(request)
    favoris_data = data_favoris(request)
    
    context = {
        'commande': data['commande'],
        'articles': data['articles'],
        'categories': categories,
        'nombre_article': data['nombre_article'],
        'favoris': favoris_data['favoris'],
        'nombre_favoris': favoris_data['nombre_favoris']
    }
    
    return render(request, 'shop/favoris.html', context)


def is_favori(request, produit_id):
    """Vérifier si un produit est dans les favoris"""
    if not request.user.is_authenticated:
        return False
    
    try:
        client = request.user.client
        return Favoris.objects.filter(client=client, produit_id=produit_id).exists()
    except:
        return False
   