import React, { useState, useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import CoeusHeader from './CoeusHeader';
import ReactFlow, { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';

// Custom node component to display checkpoint details.
const CheckpointNode = ({ data }) => {
  return (
    <div
      style={{
        padding: '10px',
        border: '1px solid #f5646d',
        borderRadius: '8px',
        backgroundColor: '#fff',
        cursor: 'pointer'
      }}
    >
      <strong>{data.label}</strong>
      <div style={{ marginTop: '5px', fontSize: '0.85rem', color: '#333' }}>
        <p><strong>Message:</strong> {data.message}</p>
        <p><strong>Output:</strong> {data.output}</p>
      </div>
    </div>
  );
};

const ChatInterface = () => {
  // Chat state
  const [messages, setMessages] = useState([
    { sender: 'bot', text: 'Hello, how can I assist you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatWindowRef = useRef(null);

// Visualization and branching modals
  const [showVisualization, setShowVisualization] = useState(false);
  const [selectedCheckpoint, setSelectedCheckpoint] = useState(null);

  // Dummy nodes and edges for the React Flow visualization.
  const [nodes, setNodes] = useState([
    { id: '1', data: { label: 'Start Checkpoint' }, position: { x: 0, y: 50 } },
    { id: '2', data: { label: 'Checkpoint 1' }, position: { x: 250, y: 50 } },
    { id: '3', data: { label: 'Checkpoint 2' }, position: { x: 500, y: 50 } }
  ]);
  const [edges, setEdges] = useState([
    { id: 'e1-2', source: '1', target: '2' },
    { id: 'e2-3', source: '2', target: '3' }
  ]);

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

    // Optionally open the visualization popup when the send button is clicked.
    setShowVisualization(true);

    // Add the user's message.
    const userMessage = { sender: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    // Simulate a delay for the bot's response (replace with your API call).
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

  // Modal component used for both the visualization and branch editing.
  const Modal = ({ onClose, children }) => (
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
        zIndex: 1000
      }}
    >
      <div
        style={{
          backgroundColor: '#fff',
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

  // Modal for branching off a checkpoint.
  const BranchModal = ({ checkpoint, onClose }) => {
    // Local state to allow editing the checkpoint's message.
    const [editedMessage, setEditedMessage] = useState(checkpoint.data.message);
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
            <p>
              <strong>Output:</strong>
            </p>
            <pre style={{ backgroundColor: '#f0f0f0', padding: '10px' }}>
              {checkpoint.data.output}
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
          </div>
          <button
            onClick={() => {
              // Simulate updating the state and branching off.
              console.log('Branching off with new message:', editedMessage);
              // Here you would call your branch-off API (e.g. app.update_state)
              onClose();
            }}
            style={{
              marginTop: '10px',
              padding: '10px 20px',
              backgroundColor: '#f5646d',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Branch from this checkpoint
          </button>
        </div>
      </div>
    );
  };


  // Handler when a node is clicked in the React Flow graph.
  const onNodeClick = (event, node) => {
    // Open the branch modal for the clicked node.
    setSelectedCheckpoint(node);
  };

  // Define custom node types.
  const nodeTypes = {
    checkpoint: CheckpointNode
  };
  

const CustomNode = ({ data }) => {
  return (
    <div className="custom-node">
      {data.label}
    </div>
  );
};

const updatedNodes = nodes.map(node => ({ ...node, type: 'custom' }));

  return (
    <div className="outer-container">
      <div className="sidebar-wrapper">
        <Sidebar />
      </div>

      <div className="main-container">
        <CoeusHeader />
        <div className="chat-container">
          <div ref={chatWindowRef} className="chat-window">
            {messages.map((msg, idx) => (
              <div key={idx} className={`message-container ${msg.sender}`}>
                <div className={`message-bubble ${msg.sender}`}>
                  {msg.text}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="loading-indicator">
                <div className="typing-bubble">Typing...</div>
              </div>
            )}
          </div>

          <form onSubmit={handleSend} className="chat-form">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask anything..."
              className="chat-input"
            />
            <button type="submit" className="chat-button">
              Send
            </button>
          </form>
        </div>
      </div>

      {showVisualization && (
        <Modal onClose={() => setShowVisualization(false)}>
          <h2>Agentic AI Workflow Visualization</h2>
          <ReactFlowProvider>
            <div className="workflow-container">
              <ReactFlow
                nodes={nodes}
                edges={edges}
                nodeTypes={nodeTypes}
                onNodeClick={onNodeClick}
              />
            </div>
          </ReactFlowProvider>
        </Modal>
      )}

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
