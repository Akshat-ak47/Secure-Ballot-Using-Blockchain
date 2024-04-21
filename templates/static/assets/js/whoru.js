document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('voterBtn').style.opacity = 0;
    document.getElementById('officialBtn').style.opacity = 0;
  
    // Add animation for the prompt
    document.querySelector('.prompt').addEventListener('animationend', function() {
      // After prompt animation completes, show the voter and official buttons with animation
      document.getElementById('voterBtn').style.opacity = 1;
      document.getElementById('voterBtn').style.animation = 'fadeInBtn 1s ease-in forwards';
      document.getElementById('officialBtn').style.opacity = 1;
      document.getElementById('officialBtn').style.animation = 'fadeInBtn 1s ease-in forwards';
    });

  });
  