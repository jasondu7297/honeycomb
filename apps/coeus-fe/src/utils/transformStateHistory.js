// utils/transformStateHistory.js

// Transform each state item into a node.
// Customize the mapping according to your state data structure.
export const transformStateHistoryToNodes = (stateHistory) => {
    return stateHistory.map((state, index) => ({
      id: state.id || `${index}`, // ensure each node has a unique id
      data: { label: state.name || `State ${index}` },
      position: { x: state.x || index * 150, y: state.y || index * 100 },
    }));
  };
  
  // Create edges between consecutive states (if applicable).
  export const transformStateHistoryToEdges = (stateHistory) => {
    return stateHistory.map((state, index) => {
      if (index === 0) return null;
      return {
        id: `edge-${index}`,
        source: stateHistory[index - 1].id || `${index - 1}`,
        target: state.id || `${index}`,
        type: 'smoothstep',
        markerEnd: { type: 'arrow' },
      };
    }).filter(edge => edge !== null);
  };