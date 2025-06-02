// Import Firebase functions
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.8.0/firebase-app.js";
import {
  getAuth,
  onAuthStateChanged,
  signOut,
} from "https://www.gstatic.com/firebasejs/11.8.0/firebase-auth.js";
import {
  getFirestore,
  getDoc,
  doc,
} from "https://www.gstatic.com/firebasejs/11.8.0/firebase-firestore.js";

// Firebase Configuration
const firebaseConfig = {
  apiKey: "AIzaSyBp5hN8nhz-pYkyo6MZvysR4ViB1ehWfJ0",
  authDomain: "draftflow-b7b11.firebaseapp.com",
  projectId: "draftflow-b7b11",
  storageBucket: "draftflow-b7b11.firebasestorage.app",
  messagingSenderId: "269160881503",
  appId: "1:269160881503:web:b8dd4446dbd68bbc626aea",
  measurementId: "G-HTEHKFJ880",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth();
const db = getFirestore();

// DOM elements
const textEditor = document.getElementById("textEditor");
const generateBtn = document.getElementById("generateBtn");
const clearBtn = document.getElementById("clearBtn");
const outputSection = document.getElementById("outputSection");
const outputContent = document.getElementById("outputContent");
const copyBtn = document.getElementById("copyBtn");
const charCounter = document.getElementById("charCounter");
const buttonText = document.getElementById("buttonText");
const profileBtn = document.getElementById("profileBtn");
const loginBtn = document.getElementById('logInBtn');
const profileAvatarSpan = profileBtn ? profileBtn.querySelector('.profile-avatar span') : null; // Get the span inside profile-avatar
const profileInitial = document.getElementById('initial');
// State
let isGenerating = false;
let isProfileDropdownOpen = false;

// Assuming 'auth' (from getAuth()) and 'db' (from getFirestore()) are available in this scope.
// Also assuming you have these DOM elements:

onAuthStateChanged(auth, (user) => {
    if (user) {
        // --- User is Logged In ---
        console.log("User is logged in:", user.email, user.uid);

        // 1. Hide Login Button, Show Profile Button
        if (loginBtn) loginBtn.style.display = 'none';
        if (profileBtn) profileBtn.style.display = 'flex'; // Use 'flex' as it's a flex container

        // 2. Fetch User Data from Firestore
        const userUID = user.uid; // Use user.uid directly from the auth object
        const docRef = doc(db, "users", userUID);

        getDoc(docRef)
            .then((docSnap) => {
                if (docSnap.exists()) {
                    const userData = docSnap.data();
                    console.log("User data from Firestore:", userData);

                    // Update profile display name and email if elements exist
                    const pronameElement = document.getElementById("proname"); // Assuming these are inside profileBtn or elsewhere
                    const proemailElement = document.getElementById("proemail"); // You might need to add these IDs to your HTML

                    if (pronameElement) pronameElement.innerText = userData.name || user.displayName || user.email;
                    if (proemailElement) proemailElement.innerText = userData.email || user.email;

                    // Update profile avatar initials (e.g., "ZA" in your HTML)
                    if (profileAvatarSpan && userData.name) {
                        const nameParts = userData.name.split(' ').filter(part => part.length > 0);
                        if (nameParts.length===1){
                           const initials = userData.name.substring(0, 2).toUpperCase();
                           profileInitial.innerText = initials; // Take first two initials
                           console.log("Loop1: ",initials);
                           
                          }else{
                            const initials = userData.name.split(' ').map(n => n[0]).join('').toUpperCase();
                            profileInitial.innerText = initials.substring(0, 2); // Take first two initials
                            console.log("Loop2: ",initials);

                        }
  //                      profileAvatarSpan.innerText = initials.substring(0, 2); // Take first two initials
                    } else if (profileAvatarSpan && user.email) {
                        profileAvatarSpan.innerText = user.email.substring(0, 2).toUpperCase(); // Fallback to email initials
                    }

                } else {
                    console.log("No matching user document found in Firestore for UID:", userUID);
                    // Fallback to Firebase Auth object data if Firestore document not found
                    if (profileAvatarSpan && user.email) {
                        profileAvatarSpan.innerText = user.email.substring(0, 2).toUpperCase();
                    }
                }
            })
            .catch((error) => {
                console.error("Error fetching user data from Firestore:", error);
                // Even if Firestore fails, the user is still logged in via Firebase Auth
                // You might still display user.email or user.displayName here
                if (profileAvatarSpan && user.email) {
                    profileAvatarSpan.innerText = user.email.substring(0, 2).toUpperCase();
                }
            });

        // Optional: Attach event listeners here if not already attached globally
        if (logoutButton) { // Assuming 'logoutButton' is the ID for a logout button
            logoutButton.onclick = () => {
                if (confirm("Are you sure you want to logout?")) {
                    // Call your shared signOutUser function from firebaseAuthObserver.js
                    signOutUser();
                }
            };
        }
        if (profileBtn) {
            profileBtn.onclick = () => {
                // Handle click on profile button (e.g., redirect to profile page)
                console.log("Profile button clicked!");
                // window.location.href = "/profile"; // Example
            };
        }


    } else {
        // --- User is Logged Out ---
        console.log("User is not logged in.");

        // 1. Show Login Button, Hide Profile Button
        if (loginBtn) loginBtn.style.display = 'flex';
        if (profileBtn) profileBtn.style.display = 'none';

        // 2. Clear any displayed user data
        const pronameElement = document.getElementById("proname");
        const proemailElement = document.getElementById("proemail");
        if (pronameElement) pronameElement.innerText = "";
        if (proemailElement) proemailElement.innerText = "";
        if (profileAvatarSpan) profileAvatarSpan.innerText = "ZA"; // Reset to default initials

        // Optional: Attach login button listener
        if (loginBtn) {
            loginBtn.onclick = () => {
                window.location.href = "/"; // Redirect to your auth/login page
            };
        }
    }
});
// Firebase Logout Function
function FirebaseLogout() {
  signOut(auth)
    .then(() => {
      console.log("User signed out successfully");
      window.location.href = "/";
    })
    .catch((error) => {
      console.log("Error in signing out:", error);
    });
}

// Initialize Application
document.addEventListener("DOMContentLoaded", function () {
  // Focus on text editor
  if (textEditor) textEditor.focus();

  // Add entrance animations
  setTimeout(() => {
    const heroSection = document.querySelector(".hero-section");
    if (heroSection) heroSection.style.opacity = "1";
  }, 100);

  // Initialize logout button
  //initializeLogoutButton();
});

// Character counter
if (textEditor && charCounter) {
  textEditor.addEventListener("input", function () {
    const count = this.value.length;
    charCounter.textContent = `${count} characters`;

    // Update counter color based on length
    if (count > 5000) {
      charCounter.style.color = "#ef4444";
    } else if (count > 3000) {
      charCounter.style.color = "#f59e0b";
    } else {
      charCounter.style.color = "var(--text-muted)";
    }
  });
}

// Generate button functionality
if (generateBtn) {
  generateBtn.addEventListener("click", async function () {
    if (isGenerating) return;

    const text = textEditor ? textEditor.value.trim() : "";
    if (!text) {
      showStatus("Please enter some text to transform!", "error");
      if (textEditor) textEditor.focus();
      return;
    }

    setLoadingState(true);

    try {
      // Simulate API call with realistic delay
      await new Promise((resolve) =>
        setTimeout(resolve, 2000 + Math.random() * 2000)
      );

      const transformedText = transformText(text);
      displayOutput(transformedText);
      showStatus("Text transformed successfully! ✨", "success");
    } catch (error) {
      showStatus("Something went wrong. Please try again.", "error");
      console.error("Transform error:", error);
    } finally {
      setLoadingState(false);
    }
  });
}

// Clear button functionality
if (clearBtn) {
  clearBtn.addEventListener("click", function () {
    const hasContent = (textEditor && textEditor.value) || 
                      (outputContent && outputContent.textContent);
    
    if (hasContent) {
      if (textEditor) textEditor.value = "";
      if (outputContent) outputContent.textContent = "";
      if (outputSection) outputSection.classList.remove("visible");
      if (charCounter) {
        charCounter.textContent = "0 characters";
        charCounter.style.color = "var(--text-muted)";
      }
      if (textEditor) textEditor.focus();
      showStatus("Content cleared", "success");
    }
  });
}

// Copy button functionality
if (copyBtn) {
  copyBtn.addEventListener("click", async function () {
    try {
      const textToCopy = outputContent ? outputContent.textContent : "";
      await navigator.clipboard.writeText(textToCopy);
      showStatus("Copied to clipboard! 📋", "success");

      // Visual feedback
      const originalText = copyBtn.textContent;
      copyBtn.textContent = "Copied!";
      copyBtn.style.background = "var(--accent-success)";
      copyBtn.style.color = "var(--text-primary)";

      setTimeout(() => {
        copyBtn.textContent = originalText;
        copyBtn.style.background = "";
        copyBtn.style.color = "";
      }, 2000);
    } catch (error) {
      showStatus("Failed to copy. Please select and copy manually.", "error");
    }
  });
}

// Profile button functionality
if (profileBtn) {
  profileBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    toggleProfileDropdown();
  });
}

// Keyboard shortcuts
document.addEventListener("keydown", function (e) {
  // Ctrl/Cmd + Enter to generate
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    e.preventDefault();
    if (!isGenerating && generateBtn) generateBtn.click();
  }

  // Ctrl/Cmd + Shift + C to clear
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === "C") {
    e.preventDefault();
    if (clearBtn) clearBtn.click();
  }

  // Close dropdown on Escape key
  if (e.key === "Escape" && isProfileDropdownOpen) {
    closeProfileDropdown();
  }
});

// Utility Functions
function setLoadingState(loading) {
  isGenerating = loading;
  if (generateBtn) generateBtn.classList.toggle("loading", loading);

  if (loading && buttonText) {
    buttonText.innerHTML = `
      <span>Transforming</span>
      <div class="typing-indicator">
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
        <div class="typing-dot"></div>
      </div>
    `;
    generateBtn.style.pointerEvents = "none";
  } else if (buttonText) {
    buttonText.textContent = "Transform Text";
    if (generateBtn) generateBtn.style.pointerEvents = "";
  }
}

function transformText(text) {
  // Enhanced text transformation with multiple formatting improvements
  let transformed = text;

  // Fix common formatting issues
  transformed = transformed
    // Fix multiple spaces
    .replace(/\s+/g, " ")
    // Fix line breaks
    .replace(/\n\s*\n\s*\n/g, "\n\n")
    // Add proper sentence spacing
    .replace(/([.!?])\s*([A-Z])/g, "$1 $2")
    // Fix quotes
    .replace(/"/g, '"')
    .replace(/"/g, '"')
    .replace(/'/g, '"')
    .replace(/'/g, ":")
    // Capitalize first letter of sentences
    .replace(/(^|[.!?]\s+)([a-z])/g, (match, p1, p2) => p1 + p2.toUpperCase());

  // Add structure and formatting
  const lines = transformed.split("\n").filter((line) => line.trim());
  const formattedLines = [];

  lines.forEach((line, index) => {
    line = line.trim();

    // Skip empty lines
    if (!line) return;

    // Detect and format headings (lines that are short and don't end with punctuation)
    if (line.length < 60 && !line.match(/[.!?]$/) && index < lines.length - 1) {
      formattedLines.push(`**${line}**\n`);
    }
    // Format list items
    else if (line.match(/^[-*•]\s/)) {
      formattedLines.push(`• ${line.replace(/^[-*•]\s/, "")}`);
    }
    // Regular paragraphs
    else {
      formattedLines.push(line);
      // Add spacing after paragraphs (except for the last one)
      if (index < lines.length - 1 && !lines[index + 1].match(/^[-*•]\s/)) {
        formattedLines.push("");
      }
    }
  });

  return formattedLines.join("\n").trim();
}

function displayOutput(text) {
  if (outputContent) outputContent.textContent = text;
  if (outputSection) outputSection.classList.add("visible");
  
  // Smooth scroll to output
  setTimeout(() => {
    if (outputSection) {
      outputSection.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  }, 300);
}

function toggleProfileDropdown() {
  const dropdown = document.getElementById("profileDropdown");
  if (!dropdown) return;

  isProfileDropdownOpen = !isProfileDropdownOpen;

  if (isProfileDropdownOpen) {
    dropdown.classList.add("visible");
  } else {
    dropdown.classList.remove("visible");
  }
}

function closeProfileDropdown() {
  const dropdown = document.getElementById("profileDropdown");
  if (dropdown) {
    dropdown.classList.remove("visible");
  }
  isProfileDropdownOpen = false;
}

// Close dropdown when clicking outside
document.addEventListener("click", function (e) {
  if (
    isProfileDropdownOpen &&
    !e.target.closest(".profile-dropdown") &&
    !e.target.closest(".profile-button")
  ) {
    closeProfileDropdown();
  }
});

// Handle profile menu actions
document.addEventListener("click", function (e) {
  const menuItem = e.target.closest(".profile-menu-item");
  if (menuItem) {
    e.preventDefault();
    const action = menuItem.getAttribute("data-action");
    handleProfileAction(action);
    closeProfileDropdown();
  }
});

function handleProfileAction(action) {
  switch (action) {
    case "settings":
      showStatus("Settings page coming soon! ⚙️", "success");
      break;
    case "help":
      showStatus("Help & Support coming soon! 🛟", "success");
      break;
    case "about":
      showStatus("About page coming soon! ℹ️", "success");
      break;
    case "privacy":
      showStatus("Privacy settings coming soon! 🔒", "success");
      break;
    case "logout":
      if (confirm("Are you sure you want to logout?")) {
        showStatus("Logging out... 👋", "success");
        FirebaseLogout();
      }
      break;
    default:
      showStatus("Feature coming soon!", "success");
  }
}

// Initialize logout button functionality
function initializeLogoutButton() {
  const logoutBtn = document.getElementById("logout");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      if (confirm("Are you sure you want to logout?")) {
        showStatus("Logging out... 👋", "success");
        FirebaseLogout();
      }
    });
  }
}

function showStatus(message, type = "success") {
  // Remove existing status messages
  const existingStatus = document.querySelector(".status-message");
  if (existingStatus) {
    existingStatus.remove();
  }

  const statusDiv = document.createElement("div");
  statusDiv.className = `status-message ${type}`;
  statusDiv.textContent = message;

  document.body.appendChild(statusDiv);

  // Show with animation
  setTimeout(() => statusDiv.classList.add("visible"), 10);

  // Auto-hide after 3 seconds
  setTimeout(() => {
    if (statusDiv.parentNode) {
      statusDiv.classList.remove("visible");
      setTimeout(() => statusDiv.remove(), 300);
    }
  }, 3000);
}


const userEmail = localStorage.getItem("userEmail");
const userName = localStorage.getItem("userName");
const userUid = localStorage.getItem("userUid");
const test = localStorage.getItem("Test");
console.log("Name: ", userName);
console.log("Email: ",userEmail);
console.log("UID: ", userUid);
console.log("Is new user?: ", test);


// Get user details from localStorage
const storedUser = localStorage.getItem("userDetails");
// OR
// const storedUser = sessionStorage.getItem("userDetails");

if (storedUser) {
  const userDetails = JSON.parse(storedUser);
  console.log("UID: ,", userDetails.uid);
  console.log("email: ,", userDetails.email);
  console.log("photoURL,", userDetails.photoURL);
  console.log("Welcome back,", userDetails.UserMetadata);
  console.log("emailVerified,", userDetails.emailVerified);
  console.log("creationTime,", userDetails.creationTime);
  console.log("lastSignInTime,", userDetails.lastSignInTime);
  // You can use userDetails.email, userDetails.uid, etc.
} else {
  console.log("No user data found. Please log in.");
}
