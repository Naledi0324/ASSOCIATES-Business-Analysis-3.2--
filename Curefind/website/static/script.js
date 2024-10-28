//This file contains the JavaScript code that adds interactivity to the website, like form validation, chatbot responses, and speech recognition.

// Form validation for Sign Up and Login pages
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.getElementsByTagName('input');
    let isValid = true;
  
    
    for (let i = 0; i < inputs.length; i++) {
      if (inputs[i].hasAttribute('required') && inputs[i].value.trim() === '') {
        inputs[i].classList.add('is-invalid');
        isValid = false;
      } else {
        inputs[i].classList.remove('is-invalid');
      }
    }
  
    if (!isValid) {
      alert("Please fill in all required fields.");
    }
  
    return isValid;
  }
  
  document.addEventListener("DOMContentLoaded", function() {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
  
    if (signupForm) {
      signupForm.onsubmit = function(event) {
        if (!validateForm('signupForm')) {
          event.preventDefault();
        }
      };
    }
  
    if (loginForm) {
      loginForm.onsubmit = function(event) {
        if (!validateForm('loginForm')) {
          event.preventDefault();
        }
      };
    }
  });
  
  // AI Chatbot functionality
  const chatbotResponses = {
    'hello': 'Hello! How can I help you today?',
    'what is my medication': 'You can take a look at your medications in the list above.',
    'thank you': 'You\'re welcome!',
    'bye': 'Goodbye! Have a great day!'
  };
  
  function sendMessage() {
    const userInput = document.getElementById('user-input').value.toLowerCase();
    addChatMessage('You', userInput);
  
    let botResponse = 'I\'m not sure how to respond to that.';
    if (chatbotResponses[userInput]) {
      botResponse = chatbotResponses[userInput];
    }
    addChatMessage('Bot', botResponse);
  
    document.getElementById('user-input').value = '';  // Clear input field
  }
  
  function addChatMessage(sender, message) {
    const chatWindow = document.getElementById('chat-window');
    const newMessage = `<p><strong>${sender}:</strong> ${message}</p>`;
    chatWindow.innerHTML += newMessage;
    chatWindow.scrollTop = chatWindow.scrollHeight;  // Scroll to the bottom
  }
  
  // Speech recognition for chatbot
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  
  function startRecognition() {
    recognition.start();
  }
  
  recognition.onresult = function(event) {
    const spokenWords = event.results[0][0].transcript.toLowerCase();
    addChatMessage('You', spokenWords);
    
    let botResponse = 'I\'m not sure how to respond to that.';
    if (chatbotResponses[spokenWords]) {
      botResponse = chatbotResponses[spokenWords];
    }
    addChatMessage('Bot', botResponse);
  };
  
  recognition.onerror = function(event) {
    console.log('Speech recognition error:', event.error);
  };
  
  // Medication list interactivity
  document.addEventListener("DOMContentLoaded", function() {
    const medicationItems = document.querySelectorAll('.list-group-item');
  
    medicationItems.forEach(function(item) {
      item.addEventListener('click', function() {
        alert('You clicked on: ' + this.textContent);
      });
    });
  });
  
  // Toggle password visibility (Sign up & Login forms)
  function togglePasswordVisibility() {
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach(function(passwordField) {
      if (passwordField.type === "password") {
        passwordField.type = "text";
      } else {
        passwordField.type = "password";
      }
    });
  }
  
  // Add toggle password feature to relevant forms
  document.addEventListener("DOMContentLoaded", function() {
    const togglePasswordBtn = document.getElementById('toggle-password-btn');
  
    if (togglePasswordBtn) {
      togglePasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility();
      });
    }
  });
  
