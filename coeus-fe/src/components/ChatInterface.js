import React, { useState, useEffect, useRef } from 'react';

const ChatInterface = () => {
  // Initialize conversation with a welcome message from the bot.
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello, how can I assist you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatWindowRef = useRef(null);

  // Automatically scroll to the bottom of the chat window when new messages arrive.
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Handles sending a message.
  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return; // Prevent sending empty messages.

    // Add the user's message.
    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate a delay for the bot's response (replace this with your API call).
    setTimeout(() => {
      const botMessage = {
        sender: 'bot',
        text: generateBotResponse(userMessage.text)
      };
      setMessages((prev) => [...prev, botMessage]);
      setIsLoading(false);
    }, 1000);
  };

  // Dummy response generator (replace with real logic or API call).
  const generateBotResponse = (userText) => {
    return `You said: "${userText}". This is a simulated response.`;
  };

  // Inline styles for a simple chat UI.
  const containerStyle = {
    display: 'flex',
    flexDirection: 'column',
    height: '100vh',
    maxWidth: '600px',
    margin: '0 auto',
    border: '1px solid #ddd'
  };

  const chatWindowStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '1rem',
    backgroundColor: '#f5f5f5'
  };

  const formStyle = {
    display: 'flex',
    borderTop: '1px solid #ddd',
    padding: '0.5rem'
  };

  const inputStyle = {
    flex: 1,
    padding: '0.5rem',
    borderRadius: '20px',
    border: '1px solid #ddd'
  };

  const buttonStyle = {
    marginLeft: '0.5rem',
    padding: '0.5rem 1rem',
    borderRadius: '20px',
    border: 'none',
    backgroundColor: '#0084ff',
    color: 'white',
    cursor: 'pointer'
  };

  const messageStyle = (sender) => ({
    marginBottom: '1rem',
    textAlign: sender === 'user' ? 'right' : 'left'
  });

  const bubbleStyle = (sender) => ({
    display: 'inline-block',
    padding: '0.5rem 1rem',
    borderRadius: '20px',
    backgroundColor: sender === 'user' ? '#0084ff' : '#e5e5ea',
    color: sender === 'user' ? 'white' : 'black'
  });

  return (
    <div style={containerStyle}>
      <div ref={chatWindowRef} style={chatWindowStyle}>
        {messages.map((msg, idx) => (
          <div key={idx} style={messageStyle(msg.sender)}>
            <div style={bubbleStyle(msg.sender)}>
              {msg.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div style={messageStyle('bot')}>
            <div style={bubbleStyle('bot')}>Typing...</div>
          </div>
        )}
      </div>
      <form onSubmit={handleSend} style={formStyle}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          style={inputStyle}
        />
        <button type="submit" style={buttonStyle}>
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
