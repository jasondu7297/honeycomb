import React, { useState } from 'react';
import { GoogleAuthProvider, getAuth, signInWithPopup } from 'firebase/auth';
// import firebase from '../firebase'; // Import your Firebase app instance

const styles = {
  toolsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '20px',
    flex: 1,
    position: 'relative',
  },
  toolCard: {
    background: 'rgba(93, 112, 147, 0.15)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '120px',
    borderRadius: '8px',
    fontSize: '1.2rem',
    cursor: 'pointer',
    transition: 'background 0.2s',
  },
  addTool: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#f7576f',
  },
  popup: {
    position: 'absolute',
    top: '-50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    background: 'linear-gradient(180deg, #4e1655 0%, #0d080e 100%)',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 0 20px rgba(247, 87, 111, 0.2)',
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '1rem',
    zIndex: 1000,
  },
  toolIcon: {
    width: '64px',
    height: '64px',
    marginBottom: '1rem',
  },
  googleButton: {
    padding: '10px 20px',
    background: '#f7576f',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '1rem',
    transition: 'background 0.2s',
  },
  closeButton: {
    padding: '8px 16px',
    background: 'rgba(255, 255, 255, 0.1)',
    color: '#fff',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '0.9rem',
    transition: 'background 0.2s',
  },
};

const provider = new GoogleAuthProvider();



function signInWithGoogle() {
  const auth = getAuth();
  signInWithPopup(auth, provider)
    .then((result) => {
      const user = result.user;
      console.log('User signed in:', user);
    })
    .catch((error) => {
      if (error.code === 'auth/configuration-not-found') {
        console.error('Firebase configuration not found. Check your Firebase setup.');
        // Implement user-friendly error message or redirect to a setup page
      } else {
        console.error('Error during sign in:', error);
      }
    });
}

const ToolsGrid = ({ tools }) => {
  const [selectedTool, setSelectedTool] = useState(null);

  const mergeStyles = (...objs) =>
    objs.reduce((acc, obj) => ({ ...acc, ...obj }), {});

  return (
    <div style={styles.toolsGrid}>
      {tools.map((tool) => (
        <div
          key={tool.id}
          style={{
            ...styles.toolCard,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
          onClick={() => setSelectedTool(tool)}
          onMouseEnter={(e) =>
            (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.15)')
          }
          onMouseLeave={(e) =>
            (e.currentTarget.style.background = 'rgba(93, 112, 147, 0.15)')
          }
        >
          <img
            src={tool.imageUrl}
            alt={tool.name}
            style={{ width: '50px', height: '50px', marginBottom: '8px', borderRadius: '10%' }}
          />
          <span>{tool.name}</span>
        </div>
      ))}
      <div
        style={mergeStyles(styles.toolCard, styles.addTool)}
        onMouseEnter={(e) =>
          (e.currentTarget.style.background = 'rgba(255, 255, 255, 0.15)')
        }
        onMouseLeave={(e) =>
          (e.currentTarget.style.background = 'rgba(93, 112, 147, 0.15)')
        }
      >
        +
      </div>
      {selectedTool && (
        <div style={styles.popup}>
          <img src={selectedTool.icon} alt={selectedTool.name} style={styles.toolIcon} />
          <h3>{selectedTool.name}</h3>
          <button onClick={signInWithGoogle} style={styles.googleButton}>
            Sign in with Google
          </button>
          <button onClick={() => setSelectedTool(null)} style={styles.closeButton}>
            Close
          </button>
        </div>
      )}
    </div>
  );
};

export default ToolsGrid;
