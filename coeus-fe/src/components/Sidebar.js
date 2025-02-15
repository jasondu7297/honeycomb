import React from 'react';

const styles = {
  sidebar: {
    width: '250px',
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
    width: '80px',
    height: '80px',
    borderRadius: '50%',
    background: '#444',
    marginBottom: '10px',
  },
  searchBox: {
    marginTop: 'auto',
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
};

const Sidebar = () => {
  return (
    <div style={styles.sidebar}>
      <div style={styles.profileBox}>
        <div style={styles.profileImage}></div>
        <h3>User Name</h3>
      </div>
      <div style={styles.searchBox}>
        <input style={styles.searchInput} type="text" placeholder="Search" />
      </div>
      <button style={styles.exploreButton}>Explore</button>
    </div>
  );
};

export default Sidebar;

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
