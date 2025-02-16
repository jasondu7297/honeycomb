// GraphComponent.js
import React, { useState, useEffect } from 'react';
import ReactFlow, { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import { transformStateHistoryToNodes, transformStateHistoryToEdges } from '../utils/transformStateHistory';

const GraphComponent = ({ isLoading }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const fetchStateHistory = async () => {
    try {
      const response = await fetch("http://localhost:8000/state_history");
      const data = await response.json();
      // Transform the state history data into React Flow nodes and edges
      setNodes(transformStateHistoryToNodes(data));
      setEdges(transformStateHistoryToEdges(data));
    } catch (error) {
      console.error("Error fetching state history:", error);
    }
  };

  // Fetch the state history whenever isLoading becomes true
  useEffect(() => {
    if (isLoading) {
      fetchStateHistory();
    }
  }, [isLoading]);

  return (
    <ReactFlowProvider>
      <div style={{ width: '100%', height: '100%' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          onNodeClick={(event, node) => console.log("Clicked node:", node)}
        />
      </div>
    </ReactFlowProvider>
  );
};

export default GraphComponent;
