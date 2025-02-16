import React, { useState, useEffect, useRef, useCallback } from 'react';
import Sidebar from './Sidebar';
import CoeusHeader from './CoeusHeader';
import ReactFlow, { ReactFlowProvider, applyNodeChanges, applyEdgeChanges } from 'reactflow';
import 'reactflow/dist/style.css';
import GraphComponent from './GraphComponent';

const ChatInterface = () => {
  // Chat state
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello, how can I assist you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const chatWindowRef = useRef(null);

  // Visualization and branching modals
  const [showVisualization, setShowVisualization] = useState(false);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState(null);

  // Dummy nodes and edges for the React Flow visualization.
  const [nodes, setNodes] = useState([
    { id: '1', data: { label: 'Start Checkpoint' }, position: { x: 0, y: 50 } },
    { id: '2', data: { label: 'Checkpoint 1', message: 'Hello, how can I assist you today?', output: 'I can help you with your research?' }, position: { x: 250, y: 50 } },
    { id: '3', data: { label: 'Checkpoint 2', message: 'Oh hello there', output: 'Kenobi?' }, position: { x: 500, y: 50 } }
  ]);
  const [edges, setEdges] = useState([
    { id: 'e1-2', source: '1', target: '2' },
    { id: 'e2-3', source: '2', target: '3' }
  ]);

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    [],
  );
  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    [],
  );

  // Automatically scroll to the bottom of the chat window when new messages arrive.
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages, isLoading]);

  // Dummy response generator (replace with real logic or API call).
  const generateBotResponse = (userText) => {
    return `You said: "${userText}". This is a simulated response.`;
  };

  // Modal component used for both the visualization and branch editing.
  const Modal = ({ onClose, children }) => (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000
      }}
    >
      <div
        style={{
          backgroundColor: '#4e1655',
          backgroundImage: `
            linear-gradient(to right, rgba(255,255,255,0.1) 1px, transparent 1px),
            linear-gradient(to bottom, rgba(255,255,255,0.1) 1px, transparent 1px)
          `,
          backgroundSize: '20px 20px',
          padding: '20px',
          borderRadius: '8px',
          width: '80%',
          height: '80%',
          overflow: 'auto',
          position: 'relative'
        }}
      >
        <button
          onClick={onClose}
          style={{
            position: 'absolute',
            top: '10px',
            right: '10px',
            cursor: 'pointer'
          }}
        >
          Close
        </button>
        {children}
      </div>
    </div>
  );

  const BranchButton = ({ editedMessage, onClose }) => {
    const [loading, setLoading] = useState(false);

    const handleBranch = async (e) => {
      e.preventDefault();
      if (!input.trim()) return;
      console.log('Branching off with new message:', editedMessage);

      // Add the user's message to the chat
      setMessages(prev => [...prev, { sender: 'user', text: input }]);
      setIsLoading(true);
  
      try {
        const response = await fetch("http://localhost:8000/update", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: editedMessage }),
        });
  
        // Clear the input field
        setInput("");
  
        // Add an initial bot message (which we'll update as we receive the stream)
        setMessages(prev => [...prev, { sender: 'bot', text: "", isStreaming: true }]);
  
        // Process the streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder("utf-8");
        let result = "";
  
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          result += decoder.decode(value, { stream: true });
        }
        const finalMessage = extractFinalMessage(result); // Your function to get the final message
        setMessages(prevMessages => {
          const updatedMessages = [...prevMessages];
          // Replace the last message (the streaming bot message) with the final message
          updatedMessages[updatedMessages.length - 1] = {
            ...updatedMessages[updatedMessages.length - 1],
            text: finalMessage,
            isStreaming: false, // Optionally disable any streaming indicator
          };
          return updatedMessages;
        });
      } catch (error) {
        console.error("Error streaming response:", error);
        setMessages(prev => [...prev, { sender: 'bot', text: "Error occurred" }]);
      }
      setIsLoading(false);
    };

    return (
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <button
          onClick={handleBranch}
          disabled={loading}
          style={{
            marginTop: '10px',
            padding: '10px 20px',
            backgroundColor: '#f5646d',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            opacity: loading ? 0.6 : 1
          }}
        >
          {loading ? 'Branching...' : 'Branch from this checkpoint'}
        </button>

        {loading && (
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            backgroundColor: 'rgba(255, 255, 255, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            borderRadius: '4px'
          }}>
            <span>Loading...</span>
          </div>
        )}
      </div>
    );
  };

  // Modal for branching off a checkpoint.
  const BranchModal = ({ checkpoint, onClose }) => {
    // Local state to allow editing the checkpoint's message.
    // console.log('Checkpoint:', checkpoint);
    const [editedMessage, setEditedMessage] = useState(checkpoint.data.message);
    // console.log('Edited message:', editedMessage);
    return (
      <div
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundColor: 'rgba(0, 0, 0, 0.5)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 1100
        }}
      >
        <div
          style={{
            backgroundColor: '#fff',
            padding: '20px',
            borderRadius: '8px',
            width: '50%',
            maxWidth: '500px',
            overflow: 'auto',
            position: 'relative'
          }}
        >
          <button
            onClick={onClose}
            style={{
              position: 'absolute',
              top: '10px',
              right: '10px',
              cursor: 'pointer'
            }}
          >
            Close
          </button>
          <h2>Branch from {checkpoint.data.label}</h2>
          <div>
            <p>
              <strong>Original Message:</strong>
            </p>
            <pre style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
              {checkpoint.data.message}
            </pre>
          </div>
          <div style={{ marginTop: '10px' }}>
            <label>Edit Message to Branch Off:</label>
            <textarea
              value={editedMessage}
              onChange={(e) => setEditedMessage(e.target.value)}
              rows={4}
              style={{ width: '100%', marginTop: '5px' }}
            />
            <BranchButton editedMessage={editedMessage} onClose={onClose} />
          </div>
        </div>
      </div>
    );
  };

  // Handler when a node is clicked in the React Flow graph.
  const onNodeClick = (event, node) => {
    // Open the branch modal for the clicked node.
    console.log("Clicked node:", node);
    setSelectedCheckpoint(node);
  };

  // ----- STYLES -----

  // Outer container: flex row to hold sidebar and main content
  const outerContainerStyle = {
    display: 'flex',
    flexDirection: 'row',
    height: '100vh',
    width: '100%',
    margin: 0,
    padding: 0,
    background: 'linear-gradient(180deg, #4e1655 0%, #0d080e 90%, #0d080e 100%)',
    color: '#b94a53'
  };

  // const workflowBackgroundStyle = {
  //   background: 'linear-gradient(180deg, #4e1655 50%, #0d080e 100%)',
  //   width: '100%',
  //   height: '100%',
  // }
  // Force the sidebar to be 250px wide
  const sidebarWrapperStyle = {
    width: '250px'
  };

  const whiteText = {
    color: '#fff',
  };

  // Main container takes up the remaining space
  const mainContainerStyle = {
    flex: 1,
    display: 'flex',
    flexDirection: 'column',
    padding: '1rem'
  };

  // Chat area container
  const chatContainerStyle = {
    display: 'flex',
    flexDirection: 'column',
    flex: 1 // grow to fill remaining vertical space
  };

  const chatWindowStyle = {
    flex: 1,
    overflowY: 'auto',
    padding: '1rem',
    backgroundColor: '#4e1655',
    borderRadius: '8px',
    marginBottom: '1rem',
    width: '80%',
    height: '80%',
    transform: 'translateX(10%)',
    boxShadow: '0 0 20px rgba(247, 87, 111, 0.2)'
  };

  // Form styles
  const formStyle = {
    display: 'flex',
    width: '100%'
  };

  const inputStyle = {
    flex: 1,
    padding: '0.75rem 1rem',
    borderRadius: '20px',
    border: `1px solid #b94a53`,
    outline: 'none',
    backgroundColor: '#0d080e',
    color: '#b94a53'
  };

  const buttonStyle = {
    marginLeft: '0.5rem',
    padding: '0.75rem 1.5rem',
    borderRadius: '20px',
    border: 'none',
    backgroundColor: '#b94a53',
    color: '#0d080e',
    cursor: 'pointer',
    fontWeight: 'bold'
  };
  
  // Message alignment and bubble styles
  const messageStyle = (sender) => ({
    display: 'flex',
    justifyContent: sender === 'user' ? 'flex-end' : 'flex-start',
    marginBottom: '1rem'
  });

  const bubbleStyle = (sender) => ({
    maxWidth: '60%',
    padding: '0.75rem 1rem',
    borderRadius: '20px',
    lineHeight: '1.4',
    color: '#ffffff',
    backgroundColor: sender === 'user' ? '#b94a53' : '#0d080e'
  });

  // ----- Modal & React Flow Styles -----
  const modalOverlayStyle = {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    background: 'linear-gradient(180deg, #4e1655 0%, #0d080e 90%, #0d080e 100%)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000
  };

  const CustomNode = ({ data }) => {
    return (
      <div style={{
        backgroundColor: 'grey',
        color: 'black',
        padding: '10px 20px',
        borderRadius: '12px',
        textAlign: 'center',
        boxShadow: '0 0 20px rgba(247, 87, 111, 0.2)',
        minWidth: '100px'
      }}>
        {data.label}
      </div>
    );
  };

  const nodeTypes = { custom: CustomNode };

  //pass route
  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add the user's message to the chat
    setMessages(prev => [...prev, { sender: 'user', text: input }]);
    setIsLoading(true);

    try {
      const response = await fetch("http://localhost:8000/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      // Clear the input field
      setInput("");

      // Add an initial bot message (which we'll update as we receive the stream)
      setMessages(prev => [...prev, { sender: 'bot', text: "", isStreaming: true }]);

      // Process the streaming response
      const reader = response.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let result = "";

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        result += decoder.decode(value, { stream: true });
      }
      const finalMessage = extractFinalMessage(result); // Your function to get the final message
      setMessages(prevMessages => {
        const updatedMessages = [...prevMessages];
        // Replace the last message (the streaming bot message) with the final message
        updatedMessages[updatedMessages.length - 1] = {
          ...updatedMessages[updatedMessages.length - 1],
          text: finalMessage,
          isStreaming: false, // Optionally disable any streaming indicator
        };
        return updatedMessages;
      });
    } catch (error) {
      console.error("Error streaming response:", error);
      setMessages(prev => [...prev, { sender: 'bot', text: "Error occurred" }]);
    }
    setIsLoading(false);
  };

  function extractFinalMessage(rawOutput) {
    // Use a regular expression to match the last AIMessage content
    const regex = /AIMessage\(content='([^']*)'/g;
    let match, lastMessage = '';
    while ((match = regex.exec(rawOutput)) !== null) {
      lastMessage = match[1];
    }
    return lastMessage;
  }  

  return (
    <div style={outerContainerStyle}>
      {/* Sidebar Wrapper */}
      <div style={sidebarWrapperStyle}>
        <Sidebar />
      </div>
  
      {/* Main Content */}
      <div style={mainContainerStyle}>
        <CoeusHeader />
        <div style={chatContainerStyle}>
          <div ref={chatWindowRef} style={chatWindowStyle}>
            {messages.map((msg, idx) => (
              <div key={idx} style={messageStyle(msg.sender)}>
                <div style={bubbleStyle(msg.sender)}>{msg.text}</div>
              </div>
            ))}
            {isLoading && (
              <div style={messageStyle('bot')}>
                <div style={bubbleStyle('bot')}>Typing...</div>
              </div>
            )}
  
            {/* Show Visualization button only after final bot output is parsed */}
            {!isLoading &&
              messages.length > 0 &&
              messages[messages.length - 1].sender === 'bot' &&
              !messages[messages.length - 1].isStreaming &&
              messages[messages.length - 1].text && (
                <button
                  onClick={() => setShowVisualization(true)}
                  style={buttonStyle}
                >
                  Show Visualization
                </button>
              )}
          </div>
  
          <form onSubmit={handleSend} style={formStyle}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              style={inputStyle}
            />
            <button type="submit" style={buttonStyle}>
              Send
            </button>
          </form>
        </div>
      </div>
  
      {/* Visualization Modal */}
      {showVisualization && (
        <Modal onClose={() => setShowVisualization(false)}>
          <h2 style={{ color: 'white' }}>Agentic AI Workflow Visualization</h2>
          <GraphComponent onNodeClick={onNodeClick} />
        </Modal>
      )}
  
      {/* Branching Modal */}
      {selectedCheckpoint && (
        <BranchModal
          checkpoint={selectedCheckpoint}
          onClose={() => setSelectedCheckpoint(null)}
        />
      )}
    </div>
  );
};

export default ChatInterface;