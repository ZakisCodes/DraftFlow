
    // DOM elements
    const textEditor = document.getElementById('textEditor');
    const generateBtn = document.getElementById('generateBtn');
    const clearBtn = document.getElementById('clearBtn');
    const outputSection = document.getElementById('outputSection');
    const outputContent = document.getElementById('outputContent');
    const copyBtn = document.getElementById('copyBtn');
    const charCounter = document.getElementById('charCounter');
    const buttonText = document.getElementById('buttonText');
    const profileBtn = document.getElementById('profileBtn');

    // State
    let isGenerating = false;

    // Initialize
    document.addEventListener('DOMContentLoaded', function() {
      // Focus on text editor
      textEditor.focus();
      
      // Add entrance animations
      setTimeout(() => {
        document.querySelector('.hero-section').style.opacity = '1';
      }, 100);
    });

    // Character counter
    textEditor.addEventListener('input', function() {
      const count = this.value.length;
      charCounter.textContent = `${count} characters`;
      
      // Update counter color based on length
      if (count > 5000) {
        charCounter.style.color = '#ef4444';
      } else if (count > 3000) {
        charCounter.style.color = '#f59e0b';
      } else {
        charCounter.style.color = 'var(--text-muted)';
      }
    });

    // Generate button functionality
    generateBtn.addEventListener('click', async function() {
      if (isGenerating) return;
      
      const text = textEditor.value.trim();
      if (!text) {
        showStatus('Please enter some text to transform!', 'error');
        textEditor.focus();
        return;
      }

      setLoadingState(true);
      
      try {
        // Simulate API call with realistic delay
        await new Promise(resolve => setTimeout(resolve, 2000 + Math.random() * 2000));
        
        const transformedText = transformText(text);
        displayOutput(transformedText);
        showStatus('Text transformed successfully! ✨', 'success');
        
      } catch (error) {
        showStatus('Something went wrong. Please try again.', 'error');
        console.error('Transform error:', error);
      } finally {
        setLoadingState(false);
      }
    });

    // Clear button functionality
    clearBtn.addEventListener('click', function() {
      if (textEditor.value || outputContent.textContent) {
        textEditor.value = '';
        outputContent.textContent = '';
        outputSection.classList.remove('visible');
        charCounter.textContent = '0 characters';
        charCounter.style.color = 'var(--text-muted)';
        textEditor.focus();
        showStatus('Content cleared', 'success');
      }
    });

    // Copy button functionality
    copyBtn.addEventListener('click', async function() {
      try {
        await navigator.clipboard.writeText(outputContent.textContent);
        showStatus('Copied to clipboard! 📋', 'success');
        
        // Visual feedback
        const originalText = copyBtn.textContent;
        copyBtn.textContent = 'Copied!';
        copyBtn.style.background = 'var(--accent-success)';
        copyBtn.style.color = 'var(--text-primary)';
        
        setTimeout(() => {
          copyBtn.textContent = originalText;
          copyBtn.style.background = '';
          copyBtn.style.color = '';
        }, 2000);
        
      } catch (error) {
        showStatus('Failed to copy. Please select and copy manually.', 'error');
      }
    });

    // Profile button (placeholder functionality)
    profileBtn.addEventListener('click', function() {
      showStatus('Profile menu coming soon! 👤', 'success');
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
      // Ctrl/Cmd + Enter to generate
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!isGenerating) generateBtn.click();
      }
      
      // Ctrl/Cmd + Shift + C to clear
      if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'C') {
        e.preventDefault();
        clearBtn.click();
      }
    });

    // Utility functions
    function setLoadingState(loading) {
      isGenerating = loading;
      generateBtn.classList.toggle('loading', loading);
      
      if (loading) {
        buttonText.innerHTML = `
          <span>Transforming</span>
          <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
          </div>
        `;
        generateBtn.style.pointerEvents = 'none';
      } else {
        buttonText.textContent = 'Transform Text';
        generateBtn.style.pointerEvents = '';
      }
    }

    function transformText(text) {
      // Enhanced text transformation with multiple formatting improvements
      let transformed = text;

      // Fix common formatting issues
      transformed = transformed
        // Fix multiple spaces
        .replace(/\s+/g, ' ')
        // Fix line breaks
        .replace(/\n\s*\n\s*\n/g, '\n\n')
        // Add proper sentence spacing
        .replace(/([.!?])\s*([A-Z])/g, '$1 $2')
        // Fix quotes
        .replace(/"/g, '"').replace(/"/g, '"')
        .replace(/'/g, '"').replace(/'/g, '"')
        // Capitalize first letter of sentences
        .replace(/(^|[.!?]\s+)([a-z])/g, (match, p1, p2) => p1 + p2.toUpperCase());

      // Add structure and formatting
      const lines = transformed.split('\n').filter(line => line.trim());
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
          formattedLines.push(`• ${line.replace(/^[-*•]\s/, '')}`);
        }
        // Regular paragraphs
        else {
          formattedLines.push(line);
          // Add spacing after paragraphs (except for the last one)
          if (index < lines.length - 1 && !lines[index + 1].match(/^[-*•]\s/)) {
            formattedLines.push('');
          }
        }
      });

      return formattedLines.join('\n').trim();
    }

    function displayOutput(text) {
      outputContent.textContent = text;
      outputSection.classList.add('visible');
      
      // Smooth scroll to output
      setTimeout(() => {
        outputSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start' 
        });
      }, 300);
    }

    function showStatus(message, type = 'success') {
      // Remove existing status messages
      const existingStatus = document.querySelector('.status-message');
      if (existingStatus) {
        existingStatus.remove();
      }

      const statusDiv = document.createElement('div');
      statusDiv.className = `status-message ${type}`;
      statusDiv.textContent = message;
      
      document.body.appendChild(statusDiv);
      
      // Show with animation
      setTimeout(() => statusDiv.classList.add('visible'), 100);
      
      // Auto-hide after 3
    }