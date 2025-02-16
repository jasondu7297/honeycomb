import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const styles = {
  sidebar: {
    width: '250px',
    height: '100vh',
    background: 'linear-gradient(180deg, #4e1655 50%, #0d080e 100%)',
    display: 'flex',
    flexDirection: 'column',
    padding: '20px',
    boxSizing: 'border-box',
  },
  profileBox: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    marginBottom: '20px',
  },
  profileImage: {
    width: '90px',
    height: '90px',
    borderRadius: '30%',
    background: '#444',
    marginBottom: '10px',
  },
  searchBox: {
    marginTop: 'auto',
    alignItems: 'center',
  },
  searchInput: {
    width: '100%',
    padding: '8px',
    background: 'rgba(255, 255, 255, 0.1)',
    border: 'none',
    outline: 'none',
    color: '#fff',
    borderRadius: '4px',
  },
  exploreButton: {
    marginTop: '20px',
    padding: '10px',
    background: '#f7576f',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    animation: 'pulse 2s infinite',
    marginBottom: '30px',
  },
  whiteText: {
    color: '#fff',
  },
};

const Sidebar = () => {
  const navigate = useNavigate();
  const location = useLocation();

  // Determine if the current location is the chat page.
  const isChatPage = location.pathname === '/chat';

  // Set the button's text and target route based on the current location.
  const buttonText = isChatPage ? 'Back to Home' : 'Run a Workflow';
  const targetPath = isChatPage ? '/' : '/chat';

  const handleToggleChat = () => {
    navigate(targetPath);
  };

  return (
    <div style={styles.sidebar}>
      <div style={styles.profileBox}>
          <img
            src="/alex_cropped_headshot.png"
            alt="User"
            style={styles.profileImage}
          />
        <h3 style={styles.whiteText}>Alexander Cholmsky</h3>
      </div>
      {/* <div style={styles.searchBox}>
        <input style={styles.searchInput} type="text" placeholder="Search" />
      </div> */}
      <button style={styles.exploreButton} onClick={handleToggleChat}>
        {buttonText}
      </button>
      <button style={styles.exploreButton} onClick={() => window.open("https://poloclub.github.io/wizmap/?dataURL=http%3A%2F%2F127.0.0.1%3A5500%2Fdata.ndjson&gridURL=http%3A%2F%2F127.0.0.1%3A5500%2Fgrid.json", "_blank")}>
        Explore Embeddings
      </button>
    </div>
  );
};

export default Sidebar;

// Add keyframes for pulse animation
const keyframes = `
  @keyframes pulse {
    0% {
      transform: scale(1);
    }
    50% {
      transform: scale(1.05);
    }
    100% {
      transform: scale(1);
    }
  }
`;

const style = document.createElement('style');
style.textContent = keyframes;
document.head.appendChild(style);
