"use strict";
let map;

const labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let labelIndex = 0;

function initMap() {
    map = new google.maps.Map(document.getElementById("request_map"), {
    center: {lat: 38.094850, lng: -122.571530},
    scrollwheel: false,
    zoom: 13,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  
  // To do this, we'll define a single InfoWindow instance. All markers will
  // share this instance.
  const userInfo = new google.maps.InfoWindow();

  // Retrieving the information with AJAX.
  // If you want to see what `/api/carpoolers` returns, you should check `server.py`
  // $.get('/api/request_peson', (carpoolers) => {
  $.get('/request_peson/json', (carpoolers) => {
    for (const carpooler of carpoolers) {
      // Define the content of the infoWindow
      const userInfoContent = (`
        <div class="window-content">
          <div class="user-thumbnail">
            <img
              src="/static/img/carpool.jpg"
              alt="carpooler"
            />
          </div>

          <ul class="user-info">
            <li><b>Name: </b>${carpooler.name}</li>
            <li><b>Address: </b>${carpooler.street}</li>
            <li><b>Phone: </b>${carpooler.phone}</li>
            <li><b>Email: </b>${carpooler.email}</li>
          </ul>
        </div>
      `);

      const userMarker = new google.maps.Marker({
        position: {
          lat: carpooler.userLat,
          lng: carpooler.userLong
        },

        label: labels[labelIndex++ % labels.length],
        title: `User ID: ${carpooler.user_id}`,
        map: map,
      });

      userMarker.addListener('click', () => {
        userInfo.close();
        userInfo.setContent(userInfoContent);
        userInfo.open(map, userMarker);
      });


    }
  }).fail(() => {
    alert((`
      We were unable to retrieve data about user :(
    `));
  });

}

$('individual_request_form').on('submit', (evt) => {
  evt.preventDefault();

  //Get user input from a form
  const formData = {
    'requestnote': $('#request_note').text
  };

  // Send formData to the server (becomes a query string)
  $.post('/send_request_phone', formInputs, (res) => {
    // Display response from the server
    alert(`Sent the user_id to server`);
  });
});
