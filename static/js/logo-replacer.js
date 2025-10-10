// Script pour forcer le changement du logo TradiShop
document.addEventListener('DOMContentLoaded', function() {
    // Fonction pour remplacer le texte Eflyer par TradiShop
    function replaceEflyerWithTradiShop() {
        // Remplacer tous les textes contenant "Eflyer" ou "EFlyer"
        const walker = document.createTreeWalker(
            document.body,
            NodeFilter.SHOW_TEXT,
            null,
            false
        );
        
        let node;
        while (node = walker.nextNode()) {
            if (node.textContent.includes('Eflyer') || node.textContent.includes('EFlyer')) {
                node.textContent = node.textContent.replace(/Eflyer|EFlyer/gi, 'TradiShop');
            }
        }
        
        // Remplacer les images de logo
        const images = document.querySelectorAll('img');
        images.forEach(img => {
            if (img.src.includes('logo.png') || img.src.includes('footer-logo.png')) {
                // Créer un nouveau logo avec du texte
                const logoDiv = document.createElement('div');
                logoDiv.style.cssText = `
                    display: inline-block;
                    font-family: Arial, sans-serif;
                    font-weight: bold;
                    font-size: 24px;
                    background: linear-gradient(90deg, rgb(123, 102, 44) 50%, #007bff 50%);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                `;
                logoDiv.textContent = 'TRADISHOP';
                img.parentNode.replaceChild(logoDiv, img);
            }
        });
    }
    
    // Exécuter immédiatement
    replaceEflyerWithTradiShop();
    
    // Réexécuter après un délai pour s'assurer que tout est chargé
    setTimeout(replaceEflyerWithTradiShop, 1000);
    
    // Observer les changements du DOM
    const observer = new MutationObserver(function(mutations) {
        mutations.forEach(function(mutation) {
            if (mutation.type === 'childList') {
                replaceEflyerWithTradiShop();
            }
        });
    });
    
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
});
