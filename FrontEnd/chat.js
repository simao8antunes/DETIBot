document.getElementById('sendMessage').addEventListener('click', function() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value;
    if (message.trim() === '') return; // Ignore empty messages

    const chatHistory = document.querySelector('.chat-history ul');

    function appendMessage(who, text, avatar, time = new Date().toLocaleTimeString()) {
        const li = document.createElement('li');
        li.className = 'clearfix';
        li.innerHTML = `<div class="message-data ${who === 'other' ? 'text-right' : ''}">
                            <span class="message-data-time">${time}, Today</span>
                            <img src="${avatar}" alt="avatar">
                        </div>
                        <div class="message ${who === 'other' ? 'other-message float-right' : 'my-message'}">${text}</div>`;
        chatHistory.appendChild(li);
    }

    // Display user's message immediately
    appendMessage('other', message, 'https://bootdey.com/img/Content/avatar/avatar7.png');

    // Clear input box after sending message
    messageInput.value = '';

    // Send message to API using axios
    axios.get(`http://localhost:8000/detibot/${encodeURIComponent(message)}`)
        .then(function (response) {
            // Handle success
            appendMessage('my', response.data.resposta, 'https://bootdey.com/img/Content/avatar/avatar6.png');
        })
        .catch(function (error) {
            // Handle error
            console.error('Error:', error);
            appendMessage('my', 'Error: Could not retrieve response.', 'https://bootdey.com/img/Content/avatar/avatar6.png');
        });
});
