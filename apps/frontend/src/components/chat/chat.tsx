import  { useState, useEffect } from "react";
import { Box, Card, Typography, Avatar, TextField, Button, CircularProgress } from "@mui/material";
import { styled } from "@mui/system";
import { FaRobot } from "react-icons/fa";
import { IoSend } from "react-icons/io5";

const ChatContainer = styled(Card)(() => ({
  width: "1000px",
  padding: "20px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  borderRadius: "16px",
  height: "500px",
  display: "flex",
  flexDirection: "column"
}));

const MessagesContainer = styled(Box)({
  flex: 1,
  overflowY: "auto",
  padding: "10px",
  "&::-webkit-scrollbar": {
    width: "8px"
  },
  "&::-webkit-scrollbar-track": {
    background: "#f1f1f1",
    borderRadius: "10px"
  },
  "&::-webkit-scrollbar-thumb": {
    background: "#888",
    borderRadius: "10px"
  }
});

const MessageBubble = styled(Box)(({ isUser } : {isUser : boolean}) => ({
  display: "flex",
  alignItems: "flex-start",
  marginBottom: "16px",
  flexDirection: isUser ? "row-reverse" : "row"
}));

const Message = styled(Box)(({ isUser } : {isUser : boolean}) => ({
  maxWidth: "70%",
  padding: "12px 16px",
  borderRadius: "12px",
  backgroundColor: isUser ? "#1976d2" : "#f5f5f5",
  color: isUser ? "white" : "black",
  marginLeft: isUser ? "0" : "8px",
  marginRight: isUser ? "8px" : "0",
  boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  wordBreak: "break-word"
}));

const InputContainer = styled(Box)({
  display: "flex",
  gap: "10px",
  padding: "16px 0 0",
  borderTop: "1px solid #eee"
});

const ChatUI = () => {
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! How can I help you today?", isUser: false },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      const userMessage = {
        id: messages.length + 1,
        text: newMessage,
        isUser: true
      };
      setMessages([...messages, userMessage]);
      setNewMessage("");
      setIsTyping(true);

      // Simulate bot response
      setTimeout(() => {
        const botMessage = {
          id: messages.length + 2,
          text: "Thank you for providing that information. I'm processing your request now.",
          isUser: false
        };
        setMessages(prev => [...prev, botMessage]);
        setIsTyping(false);
      }, 2000);
    }
  };

  useEffect(() => {
    const container = document.getElementById("messages-container");
    if (container) {
      container.scrollTop = container.scrollHeight;
    }
  }, [messages]);

  return (
    <ChatContainer>      
      <MessagesContainer id="messages-container">
        {messages.map((message) => (
          <MessageBubble key={message.id} isUser={message.isUser}>
            <Avatar
              sx={{
                bgcolor: message.isUser ? "#1976d2" : "#f50057",
                width: 32,
                height: 32
              }}
            >
              {message.isUser ? "U" : <FaRobot />}
            </Avatar>
            <Message isUser={message.isUser}>
              <Typography variant="body1">{message.text}</Typography>
            </Message>
          </MessageBubble>
        ))}
        {isTyping && (
          <MessageBubble isUser={false}>
            <Avatar
              sx={{
                bgcolor: "#f50057",
                width: 32,
                height: 32
              }}
            >
              <FaRobot />
            </Avatar>
            <Message isUser={false}>
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                <CircularProgress size={20} />
                <Typography>Typing...</Typography>
              </Box>
            </Message>
          </MessageBubble>
        )}
      </MessagesContainer>

      <InputContainer>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type your message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSendMessage()}
          size="small"
        />
        <Button
          variant="contained"
          color="primary"
          onClick={handleSendMessage}
          disabled={!newMessage.trim()}
          sx={{ minWidth: "100px" }}
          endIcon={<IoSend />}
        >
          Send
        </Button>
      </InputContainer>
    </ChatContainer>
  );
};

export default ChatUI;