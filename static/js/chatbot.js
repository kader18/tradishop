// Chatbot JavaScript
class TradiShopChatbot {
    constructor() {
        this.isOpen = false;
        this.isTyping = false;
        this.messages = [];
        this.init();
    }

    init() {
        this.createChatbotHTML();
        this.bindEvents();
        this.addWelcomeMessage();
    }

    createChatbotHTML() {
        const chatbotHTML = `
            <div class="chatbot-container" id="chatbotContainer">
                <div class="chatbot-window" id="chatbotWindow">
                    <div class="chatbot-header">
                        <h3>🤖 Assistant TradiShop</h3>
                        <button class="chatbot-close" id="chatbotClose">&times;</button>
                    </div>
                    <div class="chatbot-messages" id="chatbotMessages">
                        <!-- Messages will be added here -->
                    </div>
                    <div class="chatbot-suggestions" id="chatbotSuggestions">
                        <div class="suggestion-chips">
                            <span class="suggestion-chip" data-message="Bonjour">👋 Bonjour</span>
                            <span class="suggestion-chip" data-message="Aide">❓ Aide</span>
                            <span class="suggestion-chip" data-message="Commande">🛒 Commande</span>
                            <span class="suggestion-chip" data-message="Contact">📞 Contact</span>
                        </div>
                    </div>
                    <div class="chatbot-input-container">
                        <input type="text" class="chatbot-input" id="chatbotInput" placeholder="Tapez votre message...">
                        <button class="chatbot-send" id="chatbotSend">
                            <i class="fas fa-paper-plane"></i>
                        </button>
                    </div>
                </div>
                <button class="chatbot-toggle" id="chatbotToggle">
                    <i class="fas fa-comments"></i>
                </button>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    bindEvents() {
        const toggle = document.getElementById('chatbotToggle');
        const close = document.getElementById('chatbotClose');
        const send = document.getElementById('chatbotSend');
        const input = document.getElementById('chatbotInput');
        const suggestions = document.querySelectorAll('.suggestion-chip');

        toggle.addEventListener('click', () => this.toggleChatbot());
        close.addEventListener('click', () => this.closeChatbot());
        send.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });

        suggestions.forEach(chip => {
            chip.addEventListener('click', () => {
                const message = chip.getAttribute('data-message');
                this.sendMessage(message);
            });
        });
    }

    toggleChatbot() {
        const window = document.getElementById('chatbotWindow');
        const toggle = document.getElementById('chatbotToggle');
        
        this.isOpen = !this.isOpen;
        
        if (this.isOpen) {
            window.classList.add('active');
            toggle.classList.add('active');
            document.getElementById('chatbotInput').focus();
        } else {
            window.classList.remove('active');
            toggle.classList.remove('active');
        }
    }

    closeChatbot() {
        this.isOpen = false;
        document.getElementById('chatbotWindow').classList.remove('active');
        document.getElementById('chatbotToggle').classList.remove('active');
    }

    addWelcomeMessage() {
        const welcomeMessage = "Bonjour ! Je suis l'assistant TradiShop. Comment puis-je vous aider aujourd'hui ?";
        this.addMessage('bot', welcomeMessage);
    }

    addMessage(sender, message) {
        const messagesContainer = document.getElementById('chatbotMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}`;
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.textContent = message;
        
        messageDiv.appendChild(bubble);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.messages.push({ sender, message, timestamp: new Date() });
    }

    showTyping() {
        if (this.isTyping) return;
        
        this.isTyping = true;
        const messagesContainer = document.getElementById('chatbotMessages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message bot';
        typingDiv.id = 'typingIndicator';
        
        const typingBubble = document.createElement('div');
        typingBubble.className = 'message-bubble bot';
        typingBubble.innerHTML = `
            <div class="chatbot-typing">
                Assistant TradiShop écrit
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        `;
        
        typingDiv.appendChild(typingBubble);
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    hideTyping() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
        this.isTyping = false;
    }

    async sendMessage(message = null) {
        const input = document.getElementById('chatbotInput');
        const messageText = message || input.value.trim();
        
        if (!messageText) return;
        
        // Add user message
        this.addMessage('user', messageText);
        
        // Clear input
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            // Get CSRF token
            const csrfToken = this.getCSRFToken();
            
            // Send message to server
            const response = await fetch('/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: `message=${encodeURIComponent(messageText)}`
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTyping();
            
            // Add bot response
            if (data.response) {
                this.addMessage('bot', data.response);
            } else {
                this.addMessage('bot', 'Désolé, je n\'ai pas pu traiter votre demande. Veuillez réessayer.');
            }
            
        } catch (error) {
            console.error('Erreur chatbot:', error);
            this.hideTyping();
            this.addMessage('bot', 'Désolé, une erreur s\'est produite. Veuillez réessayer.');
        }
    }

    getCSRFToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }

    // Méthode pour ajouter des suggestions dynamiques
    updateSuggestions(suggestions) {
        const container = document.getElementById('chatbotSuggestions');
        const chipsContainer = container.querySelector('.suggestion-chips');
        
        chipsContainer.innerHTML = '';
        suggestions.forEach(suggestion => {
            const chip = document.createElement('span');
            chip.className = 'suggestion-chip';
            chip.textContent = suggestion;
            chip.setAttribute('data-message', suggestion);
            chip.addEventListener('click', () => {
                this.sendMessage(suggestion);
            });
            chipsContainer.appendChild(chip);
        });
    }
}

// Initialiser le chatbot quand le DOM est chargé
document.addEventListener('DOMContentLoaded', function() {
    // Attendre un peu pour que la page soit complètement chargée
    setTimeout(() => {
        new TradiShopChatbot();
    }, 1000);
});

// Fonction globale pour ouvrir le chatbot depuis d'autres parties du site
window.openChatbot = function() {
    const chatbot = document.querySelector('.chatbot-container');
    if (chatbot) {
        const toggle = chatbot.querySelector('#chatbotToggle');
        toggle.click();
    }
};
