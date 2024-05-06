document.getElementById('sendMessage').addEventListener('click', function() {
    const message = document.getElementById('messageInput').value;
    if (message.trim() === '') return; // Ignore empty messages

    // Display the user's message immediately in the chat
    const chatHistory = document.querySelector('.chat-history ul');
    chatHistory.innerHTML += `<li class="clearfix">
        <div class="message-data text-right">
            <span class="message-data-time">${new Date().toLocaleTimeString()}, Today</span>
            <img src="https://bootdey.com/img/Content/avatar/avatar7.png" alt="avatar">
        </div>
        <div class="message other-message float-right">${message}</div>
    </li>`;

    // Clear input box after sending message
    document.getElementById('messageInput').value = '';

    // Send message to API and handle response
    fetch(`http://localhost:8000/detibot/${encodeURIComponent(message)}`)
        .then(response =>  {
            console.log('API Response:', response); // Log the full API response to help with debugging
            // Use the 'query' property from the response data
            const apiResponse = response || 'Response not found'; // Fallback text if 'query' is missing or undefined
            chatHistory.innerHTML += `<li class="clearfix">
                <div class="message-data">
                    <span class="message-data-time">${new Date().toLocaleTimeString()}, Today</span>
                </div>
                <div class="message my-message">${apiResponse}</div>
            </li>`;
        })
        .catch(error => console.error('Error:', error));
});