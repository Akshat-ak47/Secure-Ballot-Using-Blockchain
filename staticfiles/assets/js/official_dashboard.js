function showSection(section) {
    document.getElementById('dashboard-section').style.display = 'none';
    document.getElementById('event-section').style.display = 'none';
    document.getElementById('profile-section').style.display = 'none';
    document.getElementById('settings-section').style.display = 'none';

    document.getElementById(section + '-section').style.display = 'block';

    // Highlight the active section in the sidebar
    document.querySelectorAll('#sidebar ul li').forEach(function(item) {
        item.classList.remove('active');
    });
    document.getElementById(section).classList.add('active');
}

function openPopup() {
    console.log("Opening popup...");
    document.getElementById("popup").style.display = "block";
}
function closePopup() {
    console.log("Closing popup...");
    document.getElementById("popup").style.display = "none";
}

function addPartyRows() {
    var numTeams = document.getElementById("num-teams").value;
    var partyRows = document.getElementById("party-rows");

    // Clear previous party rows
    partyRows.innerHTML = "";

    // Add new party name and image upload fields
    for (var i = 1; i <= numTeams; i++) {
        var partyRow = document.createElement("div");
        partyRow.classList.add("party-row");

        var nameLabel = document.createElement("label");
        nameLabel.htmlFor = "party-name-" + i;
        nameLabel.textContent = "Name of Party " + i + ":";

        var nameInput = document.createElement("input");
        nameInput.type = "text";
        nameInput.id = "party-name-" + i;
        nameInput.name = "party-name-" + i;

        var imageLabel = document.createElement("label");
        imageLabel.htmlFor = "party-image-" + i;
        imageLabel.textContent = "Image for Party " + i + ":";

        var imageInput = document.createElement("input");
        imageInput.type = "file";
        imageInput.id = "party-image-" + i;
        imageInput.name = "party-image-" + i;

        partyRow.appendChild(nameLabel);
        partyRow.appendChild(nameInput);
        partyRow.appendChild(imageLabel);
        partyRow.appendChild(imageInput);

        partyRows.appendChild(partyRow);
    }
}


function addEvent(event) {
    event.preventDefault();

    // Get form values
    var eventName = document.getElementById("event-name").value;
    var numTeams = document.getElementById("num-teams").value;
    var eventPurpose = document.getElementById("event-purpose").value;

    // Close popup
    closePopup();

    // Create FormData object to store form data
    var formData = new FormData();
    formData.append('event_name', eventName);
    formData.append('num_teams', numTeams);
    formData.append('event_purpose', eventPurpose);

    // Add party details to FormData object
    for (var i = 1; i <= numTeams; i++) {
        var partyName = document.getElementById("party-name-" + i).value;
        var partyImage = document.getElementById("party-image-" + i).files[0];
        formData.append('parties[' + i + '][name]', partyName);
        formData.append('parties[' + i + '][image]', partyImage);
    }

    // Send POST request to Django view
    fetch('/add_event/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // After successfully adding the event, dynamically create a button for it
        addEventButton(eventName, eventPurpose);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function addEventButton(eventName, eventPurpose) {
    // Create a new button element for the event
    var button = document.createElement("button");
    button.textContent = eventName;
    button.onclick = function() {
        showEventDetails(eventName);
    };

    // Create a new row in the event table and append the button
    var row = document.createElement("tr");
    var eventNameCell = document.createElement("td");
    eventNameCell.appendChild(button);
    row.appendChild(eventNameCell);

    var eventPurposeCell = document.createElement("td");
    eventPurposeCell.textContent = eventPurpose;
    row.appendChild(eventPurposeCell);

    // Append the new row to the event table body
    var eventTableBody = document.getElementById("event-table-body");
    eventTableBody.appendChild(row);
}

// Function to load and display the event table
function loadEventTable() {
    fetch('/api/events/')  // Assuming you have an API endpoint to fetch events
    .then(response => response.json())
    .then(events => {
        var eventTableBody = document.getElementById('event-table-body');
        eventTableBody.innerHTML = ''; // Clear existing rows

        events.forEach(event => {
            var row = document.createElement('tr');
            var cell = document.createElement('td');
            cell.textContent = event.event_name;
            row.appendChild(cell);
            cell = document.createElement('td');
            cell.textContent = event.event_purpose;
            row.appendChild(cell);
            cell = document.createElement('td');
            // Add more cells for other event details as needed
            row.appendChild(cell);

            eventTableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error fetching events:', error);
    });
}

function showEventDetails(eventName) {
    // Fetch event details for the clicked event from the server
    fetch(`/api/event_details/${eventName}/`) // Replace with your actual endpoint URL
    .then(response => response.json())
    .then(eventDetails => {
        // Create a popup content element
        var popupContent = document.createElement('div');

        // Create a title for the popup
        var title = document.createElement('h3');
        title.textContent = eventName;
        popupContent.appendChild(title);

        // Create a list to display team names and images
        var teamList = document.createElement('ul');
        eventDetails.teams.forEach(team => {
            var listItem = document.createElement('li');
            listItem.textContent = team.name;

            // Add image if available
            if (team.image) {
                var image = document.createElement('img');
                image.src = `/media/${team.image}`;
                image.alt = team.name;
                listItem.appendChild(image);
            }

            teamList.appendChild(listItem);
        });

        // Append the team list to the popup content
        popupContent.appendChild(teamList);

        // Display the popup content
        openEventPopup(popupContent);
    })
    .catch(error => {
        console.error('Error fetching event details:', error);
    });
}

function openEventPopup(content) {
    var popupContent = document.getElementById('event-popup-content');
    popupContent.innerHTML = ''; // Clear existing content
    popupContent.appendChild(content);

    // Display the event popup
    document.getElementById('event-popup').style.display = 'block';
}

function closeEventPopup() {
    // Close the event popup
    document.getElementById('event-popup').style.display = 'none';
}

function showEventPopup() {
    document.getElementById('event-popup').style.display = 'block';
}

// JavaScript to close the popup
function closeEventPopup() {
    document.getElementById('event-popup').style.display = 'none';
}

// Function to delete event
function deleteEvent(eventName) {
    // Send DELETE request to Django view
    fetch(`/delete_event/${eventName}/`, {
        method: 'DELETE',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Handle response data if needed
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
