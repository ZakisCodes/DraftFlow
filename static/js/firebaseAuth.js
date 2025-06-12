// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.8.0/firebase-analytics.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  getAdditionalUserInfo,
  onAuthStateChanged,
} from "https://www.gstatic.com/firebasejs/11.8.0/firebase-auth.js";
import {
  getFirestore,
  setDoc,
  doc,
} from "https://www.gstatic.com/firebasejs/11.8.0/firebase-firestore.js";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries
let app, analytics, auth, db;
async function initFirebase() {
  const response = await fetch('/api/firebase-config');
  const firebaseConfig = await response.json();

  app = initializeApp(firebaseConfig);
  analytics = getAnalytics(app);
  auth = getAuth(app);
  db = getFirestore(app);

  // Your web app's Firebase configuration
  // For Firebase JS SDK v7.20.0 and later, measurementId is optional
  // Initialize Firebase

  // Auth state observer - handles automatic login persistence
  onAuthStateChanged(auth, (user) => {
    if (user) {
      // User is signed in
      console.log("User is logged in:", user.email);


      // If user is on login/signup page, redirect to home
      const currentPath = window.location.pathname;
      if (currentPath === "/login" || currentPath === "/signup" || currentPath === "/") {
        window.location.href = "/home";
      }

      // You can access all user details here:
      const userData = {
        uid: user.uid,
        email: user.email,
        displayName: user.displayName,
        photoURL: user.photoURL,
        emailVerified: user.emailVerified,
        creationTime: user.metadata.creationTime,
        lastSignInTime: user.metadata.lastSignInTime
      };

      // Use localStorage (persists across sessions) OR sessionStorage (cleared on tab/browser close)
      localStorage.setItem("userDetails", JSON.stringify(userData));
    } else {
      // User is signed out
      console.log("User is not logged in");
      localStorage.removeItem("LoggedInUserID");

      // If user is on protected pages, redirect to login
      const currentPath = window.location.pathname;
      if (currentPath === "/home" || currentPath.startsWith("/editor")) {
        window.location.href = "/login";
      }
    }
  });

}

initFirebase();
// Email registration
const Signupbtn = document.getElementById("signupbtn");

Signupbtn.addEventListener("click", (e) => {
  e.preventDefault();
  const name = document.getElementById("rname").value;
  const email = document.getElementById("remail").value;
  const password = document.getElementById("rpass").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      const user = userCredential.user;
      const userData = {
        email: email,
        name: name,
        createdAt: new Date().toISOString(),
        uid: user.uid
      };

      alert("Account Created Successfully");
      const docRef = doc(db, "users", user.uid);
      setDoc(docRef, userData)
        .then(() => {
          // No need for manual redirect - onAuthStateChanged will handle it
          console.log("User document created successfully");
        })
        .catch((error) => {
          console.error("Error writing document", error);
        });
    })
    .catch((error) => {
      const errorCode = error.code;
      if (errorCode == "auth/email-already-in-use") {
        alert("Email already in use");
      } else if (errorCode == "auth/weak-password") {
        alert("Password should be at least 6 characters");
      } else {
        alert("Unable to create user right now");
        console.error("Signup error:", error);
      }
    });
});

// Email sign in
const SignInbtn = document.getElementById("signinbtn");
SignInbtn.addEventListener("click", (e) => {
  e.preventDefault();
  const email = document.getElementById("email").value;
  const password = document.getElementById("pass").value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      alert("Login successful");
      // No need for manual redirect or localStorage - onAuthStateChanged handles it
      console.log("User signed in:", userCredential.user.email);
    })
    .catch((error) => {
      const errorCode = error.code;
      if (errorCode == "auth/invalid-credential" || errorCode == "auth/wrong-password") {
        alert("Incorrect Email or Password");
      } else if (errorCode == "auth/user-not-found") {
        alert("Account does not exist");
      } else if (errorCode == "auth/too-many-requests") {
        alert("Too many failed attempts. Please try again later.");
      } else {
        alert("Login failed. Please try again.");
        console.error("Login error:", error);
      }
    });
});

// Sign out function (add this to your home page)
function signOutUser() {
  signOut(auth).then(() => {
    alert("Signed out successfully");
    // onAuthStateChanged will handle the redirect
  }).catch((error) => {
    console.error("Sign out error:", error);
  });
}

// Google sign in (when you implement it)
const googleBtn = document.getElementById("googleLoginBtn");
googleBtn.addEventListener("click", () => {
  alert("Under development, Try using Email&Password Option");
});

// Function to get current user details (use this on your home page)
function getCurrentUserDetails() {
  const user = auth.currentUser;
  if (user) {
    return {
      uid: user.uid,
      email: user.email,
      displayName: user.displayName,
      photoURL: user.photoURL,
      emailVerified: user.emailVerified,
      creationTime: user.metadata.creationTime,
      lastSignInTime: user.metadata.lastSignInTime
    };
  }
  return null;
}

// Function to get user data from Firestore (use this to get additional data like name)
async function getUserDataFromFirestore(uid) {
  try {
    const docRef = doc(db, "users", uid);
    const docSnap = await getDoc(docRef);

    if (docSnap.exists()) {
      return docSnap.data();
    } else {
      console.log("No user document found");
      return null;
    }
  } catch (error) {
    console.error("Error getting user document:", error);
    return null;
  }
}