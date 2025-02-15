// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAdjBSTRd3d8B2RQelrZxyFUydJjlLCJgQ",
  authDomain: "coeus-451007.firebaseapp.com",
  projectId: "coeus-451007",
  storageBucket: "coeus-451007.firebasestorage.app",
  messagingSenderId: "502820607642",
  appId: "1:502820607642:web:9df99e066daad78a34b123",
  measurementId: "G-4RP6M5S7BP"
};

// Initialize Firebase
const firebase = initializeApp(firebaseConfig);

export default firebase;