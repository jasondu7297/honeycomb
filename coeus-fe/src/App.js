import React from 'react';
import ToolsGrid from './components/ToolsGrid';
import Sidebar from './components/Sidebar';
import PictureArea from './components/PictureArea';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';

function App() {
  // Sample data to display in the Tools grid
  const myTools = [
    { id: 1, name: 'Tool 1' },
    { id: 2, name: 'Tool 2' },
    { id: 3, name: 'Tool 3' },
  ];

  // Dark, futuristic theme styles
  const styles = {
    appContainer: {
      display: 'flex',
      height: '100vh',
      margin: 0,
      background: 'linear-gradient(180deg, #4e1655 0%, #0d080e 100%)',
      fontFamily: 'Arial, sans-serif',
      color: '#FFFFFF',
    },
    mainContent: {
      flex: 1,
      display: 'flex',
      flexDirection: 'column',
      padding: '20px',
      boxSizing: 'border-box',
    },
  };

  // Tab state for switching between My Tools and My Data
  const [activeTab, setActiveTab] = React.useState('tools');

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={
            <div style={styles.appContainer}>
              {/* Sidebar */}
              <Sidebar />

              {/* Main Content */}
              <div style={styles.mainContent}>
                {/* Picture Area */}
                <PictureArea activeTab={activeTab} setActiveTab={setActiveTab} />

                {/* Tools or Data Grid */}
                {activeTab === 'tools' ? (
                  <ToolsGrid tools={myTools} />
                ) : (
                  <ToolsGrid tools={myTools} />
                )}
              </div>
            </div>
          }
        />
        <Route path="/chat" element={<ChatInterface />} />
      </Routes>
    </Router>
  );
}

export default App;
