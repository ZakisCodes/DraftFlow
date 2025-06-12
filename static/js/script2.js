// Export modal functionality
function openExportModal() {
    const modal = document.getElementById('exportModal');
    modal.classList.add('active');
}

function closeExportModal() {
    const modal = document.getElementById('exportModal');
    modal.classList.remove('active');
}
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messagesWrapper = document.getElementById('messagesWrapper');
      
      // Predefined responses for demo
      const responses = [
        "Thank you for your message! How can I assist you further? 😊",
        "That's a great question! Let me help you with that.",
        "I understand your concern. Here's what I can tell you...",
        "Absolutely! I'd be happy to provide more information.",
        "That sounds interesting! Tell me more about what you're looking for.",
        "Perfect! I can definitely help you with that request."
      ];
      
      // Function to create typing indicator
      function createTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.innerHTML = `
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
          <div class="typing-dot"></div>
        `;
        return typingDiv;
      }
      
      // Function to add a new message
      function addMessage(text, isSent, isTyping = false) {
        const messageContainer = document.createElement('div');
        messageContainer.className = isSent ? 'message-container sent' : 'message-container received';
        
        if (isTyping) {
          messageContainer.appendChild(createTypingIndicator());
        } else {
          const message = document.createElement('div');
          message.className = isSent ? 'message message-sent' : 'message message-received';
          message.textContent = text;
          messageContainer.appendChild(message);
        }
        
        messagesWrapper.appendChild(messageContainer);
        
        // Smooth scroll to bottom
        messagesWrapper.scrollTo({
          top: messagesWrapper.scrollHeight,
          behavior: 'smooth'
        });
        
        return messageContainer;
      }
      
      // Function to remove typing indicator
      function removeTypingIndicator(container) {
        if (container && container.parentNode) {
          container.parentNode.removeChild(container);
        }
      }
      
      // Function to handle sending a message
      function sendMessage() {
        const text = messageInput.value.trim();
        if (text) {
          // Add user message
          addMessage(text, true);
          messageInput.value = '';
          
          // Show typing indicator
          const typingContainer = addMessage('', false, true);
          
          // Simulate response delay
          setTimeout(() => {
            removeTypingIndicator(typingContainer);
            const randomResponse = responses[Math.floor(Math.random() * responses.length)];
            addMessage(randomResponse, false);
          }, 1500 + Math.random() * 1000); // Random delay between 1.5-2.5 seconds
        }
      }
      
      // Event listeners
      sendButton.addEventListener('click', sendMessage);
      
      messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
          sendMessage();
        }
      });
      
      // Auto-resize input
      messageInput.addEventListener('input', (e) => {
        e.target.style.height = 'auto';
        e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
      });
      
      // Add some visual feedback to buttons
      sendButton.addEventListener('mousedown', () => {
        sendButton.style.transform = 'scale(0.95)';
      });
      
      sendButton.addEventListener('mouseup', () => {
        sendButton.style.transform = 'scale(1.1)';
      });
      
      // Focus input on load
      messageInput.focus();
      
      // Add particles effect on hover for profile avatar
      const profileAvatar = document.querySelector('.profile-avatar');
      profileAvatar.addEventListener('mouseenter', () => {
        // Create temporary glow effect
        profileAvatar.style.boxShadow = '0 12px 40px rgba(99, 102, 241, 0.8), 0 0 60px rgba(99, 102, 241, 0.4)';
      });
      
      profileAvatar.addEventListener('mouseleave', () => {
        profileAvatar.style.boxShadow = '0 8px 32px rgba(99, 102, 241, 0.4)';
      });

      // After adding navigation

      // Navigation functionality
        document.querySelectorAll('.nav-button').forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                document.querySelectorAll('.nav-button').forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
            });
        });


        // Option selection functionality
        document.querySelectorAll('.option-button').forEach(button => {
            button.addEventListener('click', function() {
                const optionType = this.dataset.option;
                const isMultiSelect = optionType === 'include';
                
                if (isMultiSelect) {
                    // Toggle selection for multi-select options
                    this.classList.toggle('selected');
                } else {
                    // Single select - remove selected from siblings and add to clicked
                    const siblings = this.parentElement.querySelectorAll('.option-button');
                    siblings.forEach(sibling => sibling.classList.remove('selected'));
                    this.classList.add('selected');
                }
            });
        });

        function confirmExport() {
            // Get selected options
            const selectedOptions = {};
            
            document.querySelectorAll('.option-group').forEach(group => {
                const buttons = group.querySelectorAll('.option-button.selected');
                const optionType = buttons[0]?.dataset.option;
                
                if (optionType === 'include') {
                    selectedOptions[optionType] = Array.from(buttons).map(btn => btn.dataset.value);
                } else {
                    selectedOptions[optionType] = buttons[0]?.dataset.value;
                }
            });
            
            console.log('Export options:', selectedOptions);
            
            // Simulate export process
            alert(`Exporting conversation as ${selectedOptions.format?.toUpperCase()} with ${selectedOptions.content} content...`);
            
            closeExportModal();
        }

        // Close modal when clicking outside
        document.getElementById('exportModal').addEventListener('click', function(e) {
            //if (e.target === this) {
              //  closeExportModal();
            //}
            console.log("Button is working");
        });

        // Close modal with Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeExportModal();
            }
        });

        loadHtmlContent()


    });

    //const Response = localStorage.getItem('Response');
    //if (Response){
      //document.getElementById('UserText').innerText = Response;
    //}
    function loadHtmlContent() {
            // Get HTML content from localStorage
            const response = localStorage.getItem('Response');
            const iframe = document.getElementById('contentFrame');
            
            if (response) {
                // Set the HTML content in the iframe
                iframe.srcdoc = response;
            } else {
                // Show message if no content found
                iframe.srcdoc = `
                    <div style="padding: 20px; text-align: center; color: #666; font-family: Arial, sans-serif;">
                        <p>No HTML content found in localStorage.</p>
                        <p>Please store your HTML content in localStorage with key 'Response'.</p>
                    </div>
                `;
            }
        }
