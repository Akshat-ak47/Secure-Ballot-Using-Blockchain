// Function to load events from local storage and display them
function loadEventsFromLocal() {
    // Retrieve events from local storage
    var events = JSON.parse(localStorage.getItem('events')) || [];

    // Display each event
    events.forEach(function(event) {
        var eventName = event.eventName;
        var partyDetails = event.partyDetails;

        // Display event details
        displayEvent(eventName, partyDetails);
    });
}

// Function to display event details
function displayEvent(eventName, partyDetails) {
    var eventList = document.getElementById('event-list');

    // Create list item for event
    var listItem = document.createElement('li');
    listItem.textContent = eventName;

    // Add event to list
    eventList.appendChild(listItem);
}

function deleteEvent(eventName) {
    // Retrieve existing events from local storage
    var events = JSON.parse(localStorage.getItem('events')) || [];

    // Remove the event with matching name
    events = events.filter(function(event) {
        return event.eventName !== eventName;
    });

    // Save the updated events back to local storage
    localStorage.setItem('events', JSON.stringify(events));

    // Remove the event from official_dashboard.html
    var eventSection = document.querySelector('h2:contains("' + eventName + '")').parentNode;
    eventSection.remove();

    // Remove the event from voter_login.html
    var eventList = document.getElementById('event-list');
    var eventListItem = eventList.querySelector('li:contains("' + eventName + '")');
    eventListItem.remove();
}

// Call the loadEventsFromLocal function when the page loads to display previously saved events
window.onload = loadEventsFromLocal;
