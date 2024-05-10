import React, { useState } from 'react';
import axios from 'axios';
import '../ChatPage.css';

const ChatPage = () => {
    const [messages, setMessages] = useState([]); // State for storing chat messages
    const [newMessage, setNewMessage] = useState(''); // State for the current input

    // Function to handle sending a new message
    const handleSendMessage = async () => {
        if (newMessage.trim()) {
            // Create a message object for the user's message
            const userMessage = {
                text: newMessage,
                isUser: true, // Indicates the message is from the user
            };

            // Add the user's message to the list of messages
            setMessages((prevMessages) => [...prevMessages, userMessage]);

            // Clear the input field
            setNewMessage('');

            // Send the user's message to the API and handle the response
            try {
                const url = `http://localhost:8000/detibot/${encodeURIComponent(newMessage)}`;
                const response = await axios.get(url);

                // Handle the API response
                if (response.data && response.data.reply) {
                    const apiResponse = {
                        text: response.data.reply,
                        isUser: false, // Indicates the message is from the API
                    };
                    // Add the API response to the list of messages
                    setMessages((prevMessages) => [...prevMessages, apiResponse]);
                }
            } catch (error) {
                console.error('Error sending message to API:', error);
                // Optionally handle the error (e.g., display an error message to the user)
            }
        }
    };

    // Function to handle the Enter key press in the input field
    const handleKeyDown = (event) => {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent form submission
            handleSendMessage(); // Send the message
        }
    };

    return (
        <div className="container mt-4">
            <h1 className="mb-4">Chat Page</h1>

            {/* Display chat messages */}
            <div className="chat-container" style={{ maxHeight: '300px', overflowY: 'auto', borderRadius: '15px', border: '1px solid #ccc', padding: '10px' }}>
                {messages.map((message, index) => (
                    <div key={index} className={`message-wrapper ${message.isUser ? 'user-message' : 'api-message'}`}>
                        <div className={`message-bubble ${message.isUser ? 'user-bubble' : 'api-bubble'}`}>
                            {message.text}
                        </div>
                    </div>
                ))}
            </div>

            {/* Chat input field */}
            <div className="input-group mt-3">
                <input
                    type="text"
                    value={newMessage}
                    onChange={(e) => setNewMessage(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Type your message..."
                    className="form-control"
                />
                <button
                    onClick={handleSendMessage}
                    className="btn btn-primary ml-2"
                >
                    Send
                </button>
            </div>
        </div>
    );
};

export default ChatPage;
