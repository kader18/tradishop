// Fonction pour initialiser les événements des boutons
function initializePanierButtons() {
    // Supprimer tous les anciens événements pour éviter les doublons
    var produitBtns = document.getElementsByClassName('update-panier');
    
    for (var i = 0; i < produitBtns.length; i++){
        // Supprimer les anciens événements
        produitBtns[i].removeEventListener('click', handlePanierClick);
        // Ajouter le nouvel événement
        produitBtns[i].addEventListener('click', handlePanierClick);
    }
}

// Fonction de gestion du clic
function handlePanierClick(event) {
    event.preventDefault();
    event.stopPropagation();
    
    var produitId = this.dataset.produit;
    var action = this.dataset.action;
    
    // Désactiver le bouton pendant la requête
    this.disabled = true;
    
    if (user === "AnonymousUser"){
        addCookieArticle(produitId, action);
    }else{
        updateUserCommande(produitId, action);
    }
}

// Initialiser les boutons au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    initializePanierButtons();
});

// Réinitialiser les boutons après un rechargement de page
window.addEventListener('load', function() {
    initializePanierButtons();
});


function addCookieArticle(produitId, action){
 
    if(action == "add"){
        if(panier[produitId] == undefined){
            panier[produitId] = {"qte":1};
            console.log("action undefined");
        }else{
            panier[produitId]["qte"] += 1;
            console.log("action add");
        }
    }

    if(action == "remove"){
        panier[produitId]["qte"] -= 1;
        if( panier[produitId]["qte"] <= 0){
            delete panier[produitId];
        }
    }


    if(action == "delete"){
        delete panier[produitId];
    }


    document.cookie = "panier=" + JSON.stringify(panier) + ";domain=;path=/";

    location.reload();
}

function updateUserCommande(produitId, action){
    var url = '/update_article/';
    var button = event.target.closest('.update-panier');

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({"produit_id": produitId, "action": action})
    })

    .then((response) => {
        return response.json();
    })

    .then((data) => {
        console.log('data', data);
        // Réactiver le bouton
        if (button) {
            button.disabled = false;
        }
        
        // Si l'article a été supprimé, retirer la ligne du tableau
        if (data === "Article supprimé") {
            var row = button.closest('tr');
            if (row) {
                row.style.transition = 'opacity 0.3s';
                row.style.opacity = '0';
                setTimeout(function() {
                    row.remove();
                    // Vérifier s'il reste des articles
                    var remainingRows = document.querySelectorAll('tbody tr');
                    if (remainingRows.length === 0) {
                        // Afficher un message si le panier est vide
                        var tbody = document.querySelector('tbody');
                        tbody.innerHTML = '<tr><td colspan="5" class="text-center">Votre panier est vide</td></tr>';
                    }
                }, 300);
            }
        } else {
            // Recharger la page pour mettre à jour les quantités
            location.reload();
        }
    })
    
    .catch((error) => {
        console.error('Erreur:', error);
        // Réactiver le bouton en cas d'erreur
        if (button) {
            button.disabled = false;
        }
        alert('Erreur lors de la mise à jour du panier');
    });
}