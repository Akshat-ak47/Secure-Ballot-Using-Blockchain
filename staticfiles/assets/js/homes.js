function openSection(sectionId) {
    // Hide all sections
    $('#dashboard, #history, #settings, #contact, #profile').hide();
    // Show the selected section
    $('#' + sectionId).show();

    // Call fetchProfileData function if the profile section is opened
    if (sectionId === 'profile') {
        const uniqueAddress = $('.unique-address').text();
        fetchProfileData(uniqueAddress);
    }
}

function toggleDarkMode() {
    if ($('#darkMode').text() === 'Dark Mode') {
        $('body').css('background-color', '#343a40');
        $('#sidebar').css('background-color', '#212529');
        $('#sidebar, #main-content').css('color', 'white');
        $('#darkMode').text('Light Mode');
    } else {
        $('body').css('background-color', '#f8f9fa');
        $('#sidebar').css('background-color', '#343a40');
        $('#sidebar, #main-content').css('color', 'black');
        $('#darkMode').text('Dark Mode');
    }
}

function showPopup(eventName, eventId, eventPurpose, teamData) {
    console.log("Showing popup for event:", eventName); // Debugging statement
    $('#popup-window').show();
    $('#popup-content').empty();
    let teamArray = [];
    try {
        teamArray = JSON.parse(teamData[eventId]);
    } catch (error) {
        console.error('Error parsing team data:', error);
    }
    if (eventName === 'Harmony Poll: The Ayodhya Accord') {
        $('#popup-content').html(`
            <h2>${eventName}</h2>
            <div class="event-details">
                <p>
                    The Harmony Poll: The Ayodhya Accord aims to engage the community in a constructive dialogue, fostering a spirit of reconciliation and collective decision-making regarding the development of the Ayodhya site. It’s a platform for people to voice their opinions and vote on proposals that honor the diverse cultural and historical significance of the location, while looking forward to a peaceful and inclusive future.
                </p>
                <div class="event-images">
                    <img src="/static/assets/img/ram_mandir.jpg" alt="Ram Mandir" style="float: left; margin-right: 10px;">
                    <img src="/static/assets/img/babri_masjid.jpg" alt="Babri Masjid" style="float: right; margin-left: 10px;">
                </div>
                <div style="clear: both;"></div>
                <div class="vote-options">
                    <button id="vote-for">Vote</button>
                    <button id="vote-against">Vote</button>
                </div>
                <div id="result" style="text-align: center;">
                    <h3>Result</h3>
                    <p>Ram Mandir - 100 votes</p>
                    <p>Babri Masjid - 1 vote</p>
                    <p>Winner - Ram Mandir</p>
                </div>
            </div>
        `);

        $('#vote-for').click(function() {
            alert('Event has ended');
        });
        
        $('#vote-against').click(function() {
            alert('Event has ended');
        });
    } else {
        let teamsHTML = '';
        // Check if teamArray is an array and not empty
        if (Array.isArray(teamArray) && teamArray.length > 0) {
            teamArray.forEach(team => {
                let imagePath = `../${team.fields.image}`;
                console.log('Constructed Image Path:', imagePath);
                teamsHTML += `
                    <div class="team">
                        <img src="../static/${team.fields.image}" alt="${team.fields.name}" style="width: 100px; height: 100px;">
                        <p>${team.fields.name}</p>
                        <div class="vote-options">
                            <button class="vote-for">Vote for ${team.fields.name}</button>
                        </div>
                    </div>
                `;
            });
        } else {
            teamsHTML = '<p>No teams found for this event.</p>';
        }
    
        $('#popup-content').html(`
            <h2>${eventName}</h2>
            <h4>${eventId}</h4>
            <h4>${eventPurpose}</h4>
            <div class="teams-container">
                ${teamsHTML}
            </div>
        `);
    
        // Attach click event listener to vote buttons
        $('.vote-for').click(function() {
        // Disable the button to prevent multiple votes
        $(this).prop('disabled', true);
        $(this).addClass('voted');

        // Get the team name associated with the button
        var teamName = $(this).closest('.team').find('p').text();

        // Simulate sending a notification to the officials
        $.ajax({
            url: '/send-notification/',
            type: 'POST',
            data: {
                'team_name': teamName,
                'message': 'Alert: User attempted to vote'
            },
            success: function(response) {
                // Show a success message to the user
                alert("Voted successfully!");
            },
            error: function(xhr, status, error) {
                // Enable the button in case of error
                $(this).prop('disabled', false);
                alert("Failed to send notification: " + error);
            }
        });
    });
}
}    
function hidePopup() {
    document.getElementById('popup-container').style.display = 'none';
}


function loadEvents() {
    const pastEvents = [
        'Harmony Poll: The Ayodhya Accord'
    ];

    // Display past events
    const $pastEvents = $('#past-events');
    pastEvents.forEach(event => {
        $pastEvents.append(`<div class="event-block" onclick="showPopup('${event}')">${event}</div>`);
    });
}

// Call loadEvents function when the page loads
$(document).ready(function() {
    loadEvents();
});

function closePopup() {
    // Hide the popup window
    $('#popup-window').hide();
}

function voteFor(eventName) {
    // Handle voting for the specified event (e.g., increment vote count)
    console.log('Voted for ' + eventName);
}

function voteAgainst(eventName) {
    // Handle voting against the specified event (e.g., decrement vote count)
    console.log('Voted against ' + eventName);
}
