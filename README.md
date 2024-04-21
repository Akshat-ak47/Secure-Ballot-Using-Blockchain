<h1 style="border-bottom: 2px solid #000; padding-bottom: 10px;">Secure Voting System</h1>

This project aims to create a secure online voting system using Python, Django framework for backend, and HTML/CSS/JavaScript for frontend. The major focus of this project is on security and user experience. It includes features such as multi-factor authentication, two-password login system, voter interface to cast votes, and a user interface to create events for voting.

**Features**

- **Multi-factor authentication system.**
- **Two-password login:**
  - *Primary password* for the normal voting process.
  - *Secondary password* for emergencies where the voter is under threat.
- **Voter interface to cast votes securely.**
- **User interface to create events for voting.**

**Technologies Used**

- **Python**
- **Django Framework**
- **HTML/CSS/JavaScript**

**Installation**

1. **Clone the repository:**

   ```bash
   https://github.com/Akshat-ak47/Secure-Ballot-Using-Blockchain.git
   cd secure-voting-system
   ```
2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Setup Django Project**
   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   ```
4. **Run development server**
   ```
   python manage.py runserver
   ```
5. Access the web application through your browser at http://127.0.0.1:8000.

**Credits**
This project is created and maintained by :
   - *Akshat - akshat4900@gmail.com*
   - *Mayank - mnegi1704@gmail.com*


**Contributing**
*Contributions are welcome! Please follow these steps to contribute:*

 - Fork the repository.
 - Create a new branch (git checkout -b feature/new-feature).
 - Make your changes.
 - Commit your changes (git commit -am 'Add new feature').
 - Push to the branch (git push origin feature/new-feature).
 - Create a new Pull Request.

<h2>Additional Setup Instructions</h2>
    <p>To integrate Twilio for authentication:</p>
    <ul>
        <li>Add your Twilio Auth token, SID, recipient number, and your Twilio number from your Twilio account to <code>views.py</code> in line 186.</li>
    </ul>
    <p>To add Tawk.to API for a chatbot:</p>
    <ul>
        <li>Add your Tawk.to API in <code>index.html</code> for the chatbot in line 122.</li>
    </ul>

