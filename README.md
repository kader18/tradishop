# 🛍️ TradiShop - E-commerce Traditionnel Africain

[![Django](https://img.shields.io/badge/Django-5.0.4-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **TradiShop** est une plateforme e-commerce Django moderne spécialisée dans la vente de produits traditionnels africains authentiques. Découvrez une sélection unique de vêtements, chaussures, bijoux, médicaments traditionnels et bien plus encore.

## 🌟 Fonctionnalités Principales

### 🛒 E-commerce Complet
- **Catalogue de produits** avec catégories organisées
- **Système de panier** intelligent avec gestion des quantités
- **Pages de détail** produits avec galerie d'images
- **Système de commande** sécurisé avec validation
- **Gestion des livraisons** et adresses multiples
- **Système de favoris** pour sauvegarder les produits préférés

### 👤 Authentification & Sécurité
- **Inscription/Connexion** utilisateurs sécurisée
- **Réinitialisation de mot de passe** par email
- **Gestion des profils** clients personnalisés
- **Protection CSRF** et validation des formulaires
- **Authentification sociale** (Google, Facebook)

### 🎨 Interface Moderne
- **Design responsive** adapté mobile/tablette/desktop
- **Navigation intuitive** avec menu catégories
- **Images optimisées** et galeries produits
- **Templates Bootstrap 4** avec CSS personnalisé
- **Interface d'administration** Django complète

### 🤖 Fonctionnalités Avancées
- **Chatbot intégré** pour l'assistance client
- **Système d'aide** avec FAQ détaillée
- **Gestion des plats traditionnels** (section spéciale)
- **Système de recherche** et filtres produits

## 🚀 Installation Rapide

### Prérequis
- **Python 3.8+**
- **pip** (gestionnaire de paquets Python)
- **Git** (pour cloner le projet)

### Installation en 5 étapes

1. **Cloner le projet**
```bash
git clone https://github.com/kader18/tradishop.git
cd tradishop
```

2. **Créer l'environnement virtuel**
```bash
python -m venv env
```

3. **Activer l'environnement virtuel**
```bash
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configuration et lancement**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 🌐 Accès au Site
- **Site web** : http://127.0.0.1:8000/
- **Administration** : http://127.0.0.1:8000/admin/

## 📁 Structure du Projet

```
tradishop/
├── 📁 ecommerce/              # Configuration Django principale
│   ├── settings.py            # ⚠️ Paramètres (exclu du repo pour sécurité)
│   ├── urls.py               # URLs principales du projet
│   ├── wsgi.py               # Configuration WSGI
│   └── asgi.py               # Configuration ASGI
├── 📁 shop/                   # Application e-commerce principale
│   ├── models.py             # Modèles de données (Produit, Commande, etc.)
│   ├── views.py              # Vues et logique métier
│   ├── urls.py               # URLs de l'application shop
│   ├── admin.py              # Interface d'administration
│   ├── utils.py              # Utilitaires et fonctions helper
│   └── token.py              # Gestion des tokens
├── 📁 templates/             # Templates HTML
│   ├── base.html             # Template de base
│   ├── navbar.html           # Barre de navigation
│   ├── 📁 auth/              # Templates d'authentification
│   └── 📁 shop/              # Templates e-commerce
├── 📁 static/                # Fichiers statiques
│   ├── 📁 css/               # Styles CSS
│   ├── 📁 js/                # JavaScript
│   ├── 📁 images/            # Images du site
│   └── 📁 lib/               # Bibliothèques externes
├── 📁 images/                # Images des produits (médias)
├── 📁 env/                   # Environnement virtuel Python
├── manage.py                 # Script de gestion Django
├── requirements.txt          # Dépendances Python
└── README.md                 # Documentation du projet
```

## 🗄️ Modèles de Données

### 🛍️ Produit
- **Nom, prix, description** détaillée
- **Catégorie** et sous-catégories
- **Images multiples** avec galerie
- **Statut de publication** (actif/inactif)
- **Gestion des stocks** et disponibilité

### 📂 Category
- **Nom et description** de la catégorie
- **Image de catégorie** représentative
- **Hiérarchie** des catégories

### 👤 Client
- **Lien avec User Django** (authentification)
- **Informations de contact** complètes
- **Historique des commandes**
- **Adresses de livraison** multiples

### 📦 Commande
- **Gestion du panier** et articles
- **Statut de commande** (en cours, livrée, etc.)
- **Transaction ID** unique
- **Adresse de livraison** et facturation
- **Méthode de paiement**

### 🍽️ ProgrammePlats
- **Gestion des plats traditionnels**
- **Recettes et ingrédients**
- **Images des plats**

## ⚙️ Configuration

### 🔐 Sécurité
Le fichier `settings.py` contient des informations sensibles et est **exclu du repository** pour des raisons de sécurité. Pour configurer le projet :

1. **Créer un fichier `ecommerce/settings.py`** basé sur `ecommerce/settings.py.example`
2. **Configurer les variables d'environnement** :
```python
SECRET_KEY = 'votre-clé-secrète-django'
DEBUG = True  # False en production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
```

### 📧 Configuration Email
Pour activer l'envoi d'emails (réinitialisation de mot de passe) :
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

### 🗃️ Base de Données
Par défaut, le projet utilise **SQLite** pour le développement. Pour la production, configurez PostgreSQL ou MySQL :
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tradishop_db',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Déploiement en Production

### 1. Configuration Production
```python
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']
SECRET_KEY = 'votre-clé-secrète-production'
```

### 2. Collecte des fichiers statiques
```bash
python manage.py collectstatic
```

### 3. Configuration serveur web
- **Nginx** pour servir les fichiers statiques
- **Gunicorn** comme serveur WSGI
- **PostgreSQL** pour la base de données

### 4. Variables d'environnement
Créer un fichier `.env` :
```env
SECRET_KEY=votre-secret-key-production
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/tradishop_db
EMAIL_HOST_PASSWORD=votre-mot-de-passe-email
```

## 🛠️ Technologies Utilisées

- **Backend** : Django 5.0.4, Python 3.8+
- **Frontend** : HTML5, CSS3, JavaScript, Bootstrap 4
- **Base de données** : SQLite (dev), PostgreSQL (prod)
- **Authentification** : Django Auth + Social Auth
- **Interface** : Django Admin, Crispy Forms
- **Déploiement** : WSGI, Gunicorn, Nginx

## 📊 Fonctionnalités Techniques

### 🔒 Sécurité
- Protection CSRF intégrée
- Validation des formulaires Django
- Gestion sécurisée des sessions
- Authentification robuste
- Exclusion des fichiers sensibles

### ⚡ Performance
- Pagination des produits
- Images optimisées et compressées
- Requêtes de base de données optimisées
- Cache des sessions utilisateur
- Gestion efficace des fichiers statiques

### 📱 Responsive Design
- Bootstrap 4 pour la responsivité
- Design adaptatif mobile-first
- Navigation optimisée pour mobile
- Images responsives avec lazy loading

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. **Fork** le projet
2. **Créer une branche** pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. **Commit** vos changements (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. **Push** vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. **Ouvrir une Pull Request**

## 📞 Support & Contact

- **Email** : kadersoro18@gmail.com
- **GitHub** : [@kader18](https://github.com/kader18)
- **Projet** : [TradiShop Repository](https://github.com/kader18/tradishop)

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

<div align="center">

**🌟 TradiShop - Votre boutique en ligne pour les produits traditionnels africains authentiques 🌟**

*Fait avec ❤️ en Django*

</div>