import React from 'react';

const styles = {
  pictureArea: {
    position: 'relative',
    height: '350px',
    background: `url('/neon_futuristic_background.jpg')`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    marginBottom: '60px',
    borderRadius: '8px',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 0 20px rgba(247, 87, 111, 0.2)',
    overflow: 'hidden',
  },
  tabsContainer: {
    position: 'absolute',
    bottom: '10px',
    left: '50%',
    transform: 'translateX(-50%)',
    display: 'flex',
    gap: '10px',
  },
  tabButton: {
    background: 'rgba(255, 255, 255, 0.1)',
    border: 'none',
    color: '#fff',
    padding: '10px 20px',
    cursor: 'pointer',
    borderRadius: '4px',
    transition: 'background 0.2s',
  },
  tabButtonActive: {
    background: '#b94a53',
    color: '#000',
  },
};

const PictureArea = ({ activeTab, setActiveTab }) => {
  const mergeStyles = (...objs) =>
    objs.reduce((acc, obj) => ({ ...acc, ...obj }), {});

  return (
    <div style={styles.pictureArea}>
      <div style={styles.tabsContainer}>
        <button
          style={
            activeTab === 'tools'
              ? mergeStyles(styles.tabButton, styles.tabButtonActive)
              : styles.tabButton
          }
          onClick={() => setActiveTab('tools')}
        >
          My Tools
        </button>
        <button
          style={
            activeTab === 'data'
              ? mergeStyles(styles.tabButton, styles.tabButtonActive)
              : styles.tabButton
          }
          onClick={() => setActiveTab('data')}
        >
          My Data
        </button>
      </div>
    </div>
  );
};

export default PictureArea;
