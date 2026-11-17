document.addEventListener('DOMContentLoaded', function () {
    const chatBody = document.getElementById('chatBody');
    const chatInput = document.getElementById('chatInput');
    const sendBtn = document.getElementById('sendChat');
    const clearBtn = document.getElementById('clear-chat');
    const suggestions = document.querySelectorAll('.suggestion');

    function appendMessage(content, sender) {
        const message = document.createElement('div');
        message.className = 'message ' + sender;
        message.textContent = content;
        chatBody.appendChild(message);
        chatBody.scrollTop = chatBody.scrollHeight;
    }

    async function sendMessage(message) {
        if (!message || !message.trim()) {
            return;
        }
        appendMessage(message, 'user');
        chatInput.value = '';
        appendMessage('Thinking...', 'assistant');

        const response = await fetch('/api/chatbot', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();
        const messages = chatBody.querySelectorAll('.message');
        const lastMessage = messages[messages.length - 1];
        if (lastMessage) {
            lastMessage.textContent = data.reply || 'Sorry, I could not process that request.';
        }
    }

    function handleSend() {
        const message = chatInput.value.trim();
        sendMessage(message);
    }

    sendBtn.addEventListener('click', handleSend);
    chatInput.addEventListener('keydown', function (event) {
        if (event.key === 'Enter') {
            handleSend();
        }
    });

    clearBtn.addEventListener('click', function () {
        chatBody.innerHTML = '';
        appendMessage("Hello! I'm InsureBot AI, your insurance assistant. I can explain insurance plans, calculate demonstration premiums, recommend policies, and help you manage your insurance account. How can I help you today?", 'assistant');
    });

    suggestions.forEach(function (btn) {
        btn.addEventListener('click', function () {
            sendMessage(btn.textContent.trim());
        });
    });
});
