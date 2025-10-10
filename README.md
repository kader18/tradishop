# TradiShop - Site E-commerce Traditionnel

## Description
TradiShop est un site e-commerce Django spécialisé dans la vente de produits traditionnels africains. Le site propose des vêtements, chaussures, bijoux, médicaments traditionnels et bien plus encore.

## Fonctionnalités Principales

### 🛍️ E-commerce
- **Catalogue de produits** avec catégories (Chaussures, Vêtements, Bijoux, etc.)
- **Système de panier** avec gestion des quantités
- **Pages de détail** des produits avec images multiples
- **Système de commande** avec validation
- **Gestion des livraisons** et adresses

### 👤 Authentification
- **Inscription** des utilisateurs
- **Connexion/Déconnexion**
- **Réinitialisation de mot de passe**
- **Gestion des profils clients**

### 🎨 Interface
- **Design responsive** adapté mobile/desktop
- **Navigation intuitive** avec menu catégories
- **Images optimisées** pour les produits
- **Templates modernes** avec Bootstrap

## Installation et Configuration

### Prérequis
- Python 3.8+
- pip
- Git

### Installation

1. **Cloner le projet**
```bash
git clone <url-du-repo>
cd tradishop-main
```

2. **Créer un environnement virtuel**
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

5. **Configurer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

7. **Lancer le serveur**
```bash
python manage.py runserver
```

### Accès
- **Site web** : http://127.0.0.1:8000/
- **Administration** : http://127.0.0.1:8000/admin/
  - Utilisateur : admin
  - Mot de passe : admin123

## Structure du Projet

```
tradishop-main/
├── ecommerce/           # Configuration Django
│   ├── settings.py      # Paramètres du projet
│   ├── urls.py         # URLs principales
│   └── wsgi.py         # Configuration WSGI
├── shop/               # Application principale
│   ├── models.py       # Modèles de données
│   ├── views.py        # Vues et logique métier
│   ├── urls.py         # URLs de l'app
│   └── admin.py        # Interface d'administration
├── templates/          # Templates HTML
│   ├── base.html       # Template de base
│   ├── auth/           # Templates d'authentification
│   └── shop/           # Templates de l'e-commerce
├── static/             # Fichiers statiques
│   ├── css/            # Styles CSS
│   ├── js/             # JavaScript
│   └── images/         # Images du site
├── images/             # Images des produits (médias)
├── manage.py           # Script de gestion Django
└── requirements.txt    # Dépendances Python
```

## Modèles de Données

### Produit
- Nom, prix, description
- Catégorie, images multiples
- Statut de publication
- Gestion des livraisons

### Category
- Nom, description
- Image de catégorie

### Client
- Lien avec User Django
- Informations de contact

### Commande
- Gestion du panier
- Statut de commande
- Transaction ID
- Adresse de livraison

## Configuration Email

Pour activer l'envoi d'emails, modifiez `ecommerce/settings.py` :

```python
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'votre-email@gmail.com'
EMAIL_HOST_PASSWORD = 'votre-mot-de-passe-app'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
```

## Fonctionnalités Techniques

### Sécurité
- Protection CSRF
- Validation des formulaires
- Gestion des erreurs
- Authentification sécurisée

### Performance
- Pagination des produits
- Images optimisées
- Requêtes optimisées
- Cache des sessions

### Responsive Design
- Bootstrap 4
- Design adaptatif
- Navigation mobile
- Images responsives

## Déploiement

### Production
1. Modifier `DEBUG = False` dans settings.py
2. Configurer `ALLOWED_HOSTS`
3. Configurer la base de données de production
4. Collecter les fichiers statiques : `python manage.py collectstatic`
5. Configurer le serveur web (Apache/Nginx)

### Variables d'environnement
Créer un fichier `.env` :
```
SECRET_KEY=votre-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@localhost/dbname
EMAIL_HOST_PASSWORD=votre-mot-de-passe-email
```

## Support et Maintenance

### Logs
- Les logs Django sont dans la console
- Erreurs 404/500 affichées en mode DEBUG

### Sauvegarde
- Base de données : `python manage.py dumpdata > backup.json`
- Images : sauvegarder le dossier `images/`

### Mise à jour
1. Sauvegarder la base de données
2. Mettre à jour le code
3. Appliquer les migrations : `python manage.py migrate`
4. Redémarrer le serveur

## Contact

Pour toute question ou support :
- Email : kadersoro18@gmail.com
- GitHub : [Votre profil GitHub]

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

---

**TradiShop** - Votre boutique en ligne pour les produits traditionnels africains authentiques.