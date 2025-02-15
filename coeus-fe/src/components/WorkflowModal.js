import React from 'react';
import { ReactFlowProvider, ReactFlow, Node, Edge } from 'reactflow';

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

// Handler when a node is clicked in the React Flow graph.
const onNodeClick = (event, node) => {
    // Open the branch modal for the clicked node.
    setSelectedCheckpoint(node);
    };

    // Define custom node types.
    const nodeTypes = {
    checkpoint: CheckpointNode
    };
    
const nodeTypes = {};

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


export default WorkflowModal;