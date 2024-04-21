<!-- official_signup.html -->

{% if show_popup %}
<script>
    // Display the OTP popup
    document.addEventListener('DOMContentLoaded', function () {
        document.getElementById('otpPopup').style.display = 'block';
    });

    // Handle OTP submission
    document.getElementById('otpForm').addEventListener('submit', function (event) {
        event.preventDefault();
        var otp = document.getElementById('otpInput').value;
        // Submit the OTP to the server for verification using AJAX
        // Implement the AJAX request here
    });
</script>
{% endif %}

<!-- OTP popup -->
<div id="otpPopup" style="display: none;">
    <h2>Enter OTP</h2>
    <form id="otpForm">
        <input type="text" id="otpInput" required>
        <button type="submit">Submit</button>
    </form>
</div>

<!-- Your signup form -->
<form method="POST">
    <!-- Your form fields -->
</form>
