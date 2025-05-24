const signUpButton = document.getElementById("signUp");
const signInButton = document.getElementById("signIn");
const signUpBtn = document.getElementById("signUpBtn");
const signInBtn = document.getElementById("signInBtn");
const container = document.getElementById("container");
const loginForm = document.getElementById("loginForm");
const signupForm = document.getElementById("signupForm");
const googleLoginBtn = document.getElementById("googleLoginBtn");
const googleSignupBtn = document.getElementById("googleSignupBtn");
const mobileBackBtn = document.getElementById("mobileBackBtn");

// Check if device is mobile
function isMobile() {
  return window.innerWidth <= 768;
}

// Toggle to signup mode
function switchToSignup() {
  if (isMobile()) {
    container.classList.add("mobile-signup");
  } else {
    container.classList.add("signup-mode");
  }
}

// Toggle to signin mode
function switchToSignin() {
  if (isMobile()) {
    container.classList.remove("mobile-signup");
  } else {
    container.classList.remove("signup-mode");
  }
}

// Event listeners for overlay buttons (desktop only)
if (signUpButton) signUpButton.addEventListener("click", switchToSignup);
if (signInButton) signInButton.addEventListener("click", switchToSignin);

// Event listeners for form switch links
signUpBtn.addEventListener("click", switchToSignup);
signInBtn.addEventListener("click", switchToSignin);

// Mobile back button
mobileBackBtn.addEventListener("click", switchToSignin);

// Handle window resize
window.addEventListener("resize", function () {
  // Reset classes when switching between mobile and desktop
  if (!isMobile()) {
    container.classList.remove("mobile-signup");
  } else {
    container.classList.remove("signup-mode");
  }
});

// Handle login form submission
loginForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const email = e.target.querySelector('input[type="email"]').value;
  const password = e.target.querySelector('input[type="password"]').value;

  console.log("Login attempt:", { email, password });
  alert("Login form submitted! Check console for details.");
});

// Handle signup form submission
signupForm.addEventListener("submit", function (e) {
  e.preventDefault();
  const formData = new FormData(e.target);
  const inputs = e.target.querySelectorAll("input");
  const fullName = inputs[0].value;
  const email = inputs[1].value;
  const password = inputs[2].value;
  const confirmPassword = inputs[3].value;

  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return;
  }

  console.log("Signup attempt:", { fullName, email, password });
  alert("Signup form submitted! Check console for details.");
});

// Google Authentication (placeholder functions)
function handleGoogleAuth(action) {
  console.log(`Google ${action} initiated`);

  // Placeholder for Google OAuth integration
  // In a real implementation, you would integrate with Google OAuth 2.0
  alert(
    `Google ${action} would be initiated here. You'll need to integrate with Google OAuth 2.0 API.`
  );

  // Example implementation structure:
  /*
            gapi.load('auth2', function() {
                gapi.auth2.init({
                    client_id: 'YOUR_GOOGLE_CLIENT_ID'
                }).then(function() {
                    const authInstance = gapi.auth2.getAuthInstance();
                    authInstance.signIn().then(function(user) {
                        const profile = user.getBasicProfile();
                        console.log('Google user:', {
                            id: profile.getId(),
                            name: profile.getName(),
                            email: profile.getEmail()
                        });
                    });
                });
            });
            */
}

googleLoginBtn.addEventListener("click", () => handleGoogleAuth("login"));
googleSignupBtn.addEventListener("click", () => handleGoogleAuth("signup"));

// Add smooth focus transitions
document.querySelectorAll(".input-field").forEach((input) => {
  input.addEventListener("focus", function () {
    this.parentElement.style.transform = "scale(1.01)";
  });

  input.addEventListener("blur", function () {
    this.parentElement.style.transform = "scale(1)";
  });
});

// Add loading state for buttons
document.querySelectorAll(".btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    if (this.type === "submit") {
      const originalText = this.textContent;
      this.textContent = "Loading...";
      this.disabled = true;

      setTimeout(() => {
        this.textContent = originalText;
        this.disabled = false;
      }, 2000);
    }
  });
});
