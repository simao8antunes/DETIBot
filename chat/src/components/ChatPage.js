import React, { useState } from 'react';
import axios from 'axios';
import { DropdownButton, Dropdown, Spinner } from 'react-bootstrap';
import '../ChatPage.css';
import userAvatar from '../assets/user-avatar.jpg'; // Placeholder user avatar
import botAvatar from '../assets/bot-avatar.jpg'; // Bot avatar

const API_ADDR = "localhost:8000";

const ChatPage = () => {
    const [messages, setMessages] = useState([]); // State for storing chat messages
    const [newMessage, setNewMessage] = useState(''); // State for the current input
    const [language, setLanguage] = useState('en'); // State for the selected language
    const [loading, setLoading] = useState(false); // State for loading indicator

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

            // Set loading state to true
            setLoading(true);

            // Send the user's message to the API and handle the response
            try {
                const url = `http://${API_ADDR}/detibot/${language}/${encodeURIComponent(newMessage)}`;
                const response = await axios.get(url);

                // Handle the API response
                if (response.data) {
                    const apiResponse = {
                        text: response.data,
                        isUser: false, // Indicates the message is from the API
                    };
                    // Add the API response to the list of messages
                    setMessages((prevMessages) => [...prevMessages, apiResponse]);
                }
            } catch (error) {
                console.error('Error sending message to API:', error);
                // Optionally handle the error (e.g., display an error message to the user)
            } finally {
                // Set loading state to false
                setLoading(false);
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

    // Function to handle language change
    const handleLanguageChange = (selectedLanguage) => {
        setLanguage(selectedLanguage);
    };

    // Function to translate text based on the selected language
    const translateText = (text) => {
        // Define translations for English and Portuguese (Portugal)
        const translations = {
            en: {
                chatPageTitle: 'DetiBot',
                sendButton: 'Send',
                placeholder: 'Type your message...',
            },
            pt: {
                chatPageTitle: 'DetiBot',
                sendButton: 'Enviar',
                placeholder: 'Escreva a sua mensagem...',
            },
        };

        // Return the translated text based on the selected language
        return translations[language][text];
    };

    return (
        <div className="container mt-4">

            {/* Language dropdown button */}
            <DropdownButton
                id="languageDropdown"
                title={language === 'en' ? 'English' : 'Português'}
                variant="primary"
                style={{ position: 'absolute', top: '20px', right: '20px', backgroundColor: '#007bff', borderColor: '#007bff', borderRadius: '25px' }}
            >
                <Dropdown.Item onClick={() => handleLanguageChange('en')}>English</Dropdown.Item>
                <Dropdown.Item onClick={() => handleLanguageChange('pt')}>Português</Dropdown.Item>
            </DropdownButton>

            <h1 className="mb-4" style={{ fontFamily: 'Poppins, sans-serif', color: '#666', fontWeight: 'lighter' }}>{translateText('chatPageTitle')}</h1>

            <div className="card shadow" style={{ borderRadius: '25px', backgroundColor: '#A1C0CC', border: 'none' }}>

                <div className="card-body">
                    

                    {/* Display chat messages */}
                    <div className="chat-container" style={{backgroundColor: '#FFFFFF', maxHeight: '700px', overflowY: 'auto', height: '600px' }}>
                        {messages.map((message, index) => (
                            <div key={index} className={`message-wrapper ${message.isUser ? 'user-message' : 'api-message'}`}>
                                <img 
                                    src={message.isUser ? userAvatar : botAvatar} 
                                    alt={message.isUser ? 'User' : 'Bot'} 
                                    className="avatar" 
                                    style={{ width: '40px', height: '40px', borderRadius: '50%', marginRight: '10px' }}
                                />
                                <div className={`message-bubble ${message.isUser ? 'user-bubble' : 'api-bubble'}`}>
                                    {message.text}
                                </div>
                            </div>
                        ))}
                    </div>

                    {/* Loading spinner */}
                    {loading && (
                        <div className="text-center mt-3">
                            <Spinner animation="border" role="status" style={{ color: '#FFFFFF' }}>
                                <span className="sr-only"></span>
                            </Spinner>
                        </div>
                    )}

                    {/* Chat input field and send button */}
                    <div className="input-group mt-3">
                        <input
                            type="text"
                            value={newMessage}
                            onChange={(e) => setNewMessage(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder={translateText('placeholder')}
                            className="form-control"
                            style={{ borderRadius: '15px 15px 15px 15px' }}
                        />
                        <div className="input-group-append" style={{ marginLeft: '10px' }}>
                            <button
                                onClick={handleSendMessage}
                                className="btn btn-primary"
                                type="button"
                                style={{ backgroundColor: '#007bff', borderColor: '#007bff', borderRadius: '25px' }}
                            >
                                {translateText('sendButton')}
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatPage;
