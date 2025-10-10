#!/bin/bash

echo "========================================"
echo "   TradiShop - E-commerce Traditionnel"
echo "========================================"
echo

echo "Activation de l'environnement virtuel..."
source env/bin/activate

echo
echo "Démarrage du serveur Django..."
echo
echo "Le site sera accessible sur : http://127.0.0.1:8000/"
echo "L'administration sur : http://127.0.0.1:8000/admin/"
echo
echo "Utilisateur admin : admin"
echo "Mot de passe admin : admin123"
echo
echo "Appuyez sur Ctrl+C pour arrêter le serveur"
echo

python manage.py runserver
