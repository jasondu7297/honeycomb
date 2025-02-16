// GraphComponent.js
import React, { useState, useEffect } from 'react';
import ReactFlow, { ReactFlowProvider } from 'reactflow';
import 'reactflow/dist/style.css';
import { transformStateHistoryToNodes, transformStateHistoryToEdges } from '../utils/transformStateHistory';

const GraphComponent = ({ onNodeClick }) => {
  const [nodes, setNodes] = useState([]);
  const [edges, setEdges] = useState([]);

  const fetchStateHistory = async () => {
    try {
      const response = await fetch("http://localhost:8000/history/get");
      const data = await response.json();
      console.log("Fetched state history:", data);
      setNodes(transformStateHistoryToNodes(data));
      setEdges(transformStateHistoryToEdges(data));
    } catch (error) {
      console.error("Error fetching state history:", error);
    }
  };

  // what does this do, timer?
  useEffect(() => {
    fetchStateHistory();
    console.log("Fetching state history...");
  }, []);

  return (
    <ReactFlowProvider>
      <div style={{ width: '100%', height: '100%' }}>
        <ReactFlow
          nodes={nodes}
          edges={edges}
          fitView
          onNodeClick={(event, node) => {
            if (onNodeClick) {
              onNodeClick(event, node);
            }
          }}
        />
      </div>
    </ReactFlowProvider>
  );
};

export default GraphComponent;
