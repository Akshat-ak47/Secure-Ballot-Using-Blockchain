document.addEventListener("DOMContentLoaded", function() {
    const video = document.getElementById('video');
    const captureButton = document.getElementById('capture-btn');
    const registerButton = document.getElementById('register-btn');
    let capturedImage; // Define capturedImage variable in a scope accessible to both event listeners

    // Access webcam
    async function initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            video.srcObject = stream;
        } catch (err) {
            console.error("Error accessing webcam:", err);
        }
    }

    initCamera();

    // Capture image
    captureButton.addEventListener('click', function() {
        // Pause video playback
        video.pause();

        // Create a canvas element to capture the current frame
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
        capturedImage = canvas.toDataURL('image/jpeg'); // Assign capturedImage here
        // You can now store `capturedImage` for further processing or display
        console.log('Captured image:', capturedImage);

        // Replace the video element with an image element displaying the captured image
        const imageElement = document.createElement('img');
        imageElement.src = capturedImage;
        video.parentNode.replaceChild(imageElement, video);
    });

    // Register button
    registerButton.addEventListener('click', function() {
        if (capturedImage) {
            // Set the captured image value to the hidden input field
            document.getElementById('face_image').value = capturedImage;
    
            // Submit the form
            document.getElementById('registration-form').submit();
        } else {
            console.error("No image captured yet.");
            // Handle the case where no image is captured yet
        }
    });
