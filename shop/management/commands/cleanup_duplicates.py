from django.core.management.base import BaseCommand
from shop.models import CommandeArticle
from django.db.models import Count

class Command(BaseCommand):
    help = 'Nettoie les doublons dans CommandeArticle'

    def handle(self, *args, **options):
        self.stdout.write("Recherche des doublons...")
        
        # Trouver les doublons
        duplicates = CommandeArticle.objects.values('commande', 'produit').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        self.stdout.write(f"Trouvé {len(duplicates)} combinaisons de doublons")
        
        for duplicate in duplicates:
            commande_id = duplicate['commande']
            produit_id = duplicate['produit']
            
            # Récupérer tous les articles de cette combinaison
            articles = CommandeArticle.objects.filter(
                commande_id=commande_id,
                produit_id=produit_id
            ).order_by('id')
            
            if articles.count() > 1:
                # Garder le premier et supprimer les autres
                first_article = articles.first()
                total_quantite = sum(article.quantite for article in articles)
                first_article.quantite = total_quantite
                first_article.save()
                
                # Supprimer les doublons
                articles.exclude(id=first_article.id).delete()
                self.stdout.write(f"Nettoyé {articles.count() - 1} doublons pour commande {commande_id}, produit {produit_id}")
        
        self.stdout.write(self.style.SUCCESS("Nettoyage terminé!"))

