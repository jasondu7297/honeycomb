import React from 'react';
import ToolsGrid from './components/ToolsGrid';
import Sidebar from './components/Sidebar';
import PictureArea from './components/PictureArea';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ChatInterface from './components/ChatInterface';

function App() {
  // Sample data to display in the Tools grid
  const myTools = [
    { id: 1, name: 'Perplexity', imageUrl: '/icons/perplexity-ai-icon.png' },
    { id: 2, name: 'Gmail', imageUrl: '/icons/gmail_icon.png' },
    { id: 3, name: 'Google Drive', imageUrl: '/icons/google_drive_icon.png' },
    { id: 4, name: 'Google Search', imageUrl: '/icons/google-icon-rounded.png' },
  ];
  
  const myModels = [
    { id: 1, name: 'OpenAI', imageUrl: '/icons/open_ai_icon.png' },
    { id: 2, name: 'Gemini', imageUrl: '/icons/gemini_icon.png' },
    { id: 3, name: 'Mistral AI', imageUrl: '/icons/mistral_ai.png' },
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
                  <ToolsGrid tools={myModels} />
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
