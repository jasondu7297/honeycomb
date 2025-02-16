// utils/transformStateHistory.js

// Transform each state item into a node.
// Customize the mapping according to your state data structure.

export const transformStateHistoryToNodes = (stateHistory) => {
    console.log('State history:', stateHistory);
    return stateHistory.map((state, index) => ({
      id: state.checkpoint_id,
      data: { 
        label: `Checkpoint ${index + 1}`,
        message: state.most_recent_message,
        threadId: state.thread_id
      },
      position: { x: index * 150, y: index * 100 },
    }));
  };
  
export const transformStateHistoryToEdges = (stateHistory) => {
  console.log('State history for edges:', stateHistory);
  return stateHistory.map((state, index) => {
    if (index === 0) return null;
    return {
      id: `edge-${index}`,
      source: stateHistory[index - 1].checkpoint_id,
      target: state.checkpoint_id,
      type: 'smoothstep',
      markerEnd: { type: 'arrow' },
    };
  }).filter(edge => edge !== null);
};
  
