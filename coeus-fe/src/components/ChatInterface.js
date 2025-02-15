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

  const modalContentStyle = {
    backgroundColor: '#4e1655',
    padding: '20px',
    borderRadius: '8px',
    width: '80%',
    height: '80%',
    overflow: 'auto',
    boxShadow: '0 0 20px rgba(247, 87, 111, 0.2)'
  };

//   const Modal = ({ onClose, children }) => (
//     <div style={modalOverlayStyle}>
//       <div style={modalContentStyle}>
//       <button 
//   onClick={onClose} 
//   style={{ 
//     marginBottom: '10px', 
//     cursor: 'pointer', 
//     backgroundColor: 'grey', 
//     color: 'black', 
//     border: 'none', 
//     padding: '8px 16px', 
//     borderRadius: '8px' 
//   }}
// >
//   Close
// </button>
//         {children}
//       </div>
//     </div>
//   );



const CustomNode = ({ data }) => {
  return (
    <div style={{
      backgroundColor: 'grey',
      color: 'black',
      padding: '10px 20px',
      borderRadius: '12px',
      textAlign: 'center',
      boxShadow: '0px 2px 5px rgba(0,0,0,0.2)',
      minWidth: '100px'
    }}>
      {data.label}
    </div>
  );
};

// const nodeTypes = { custom: CustomNode };

// Ensure that each node in `nodes` has `type: 'custom'`
const updatedNodes = nodes.map(node => ({ ...node, type: 'custom' }));

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
          <h2>Agentic AI Workflow Visualization</h2>
          <ReactFlowProvider>
            <div style={{ width: '100%', height: '100%' }}>
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
