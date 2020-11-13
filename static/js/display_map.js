"use strict";
let map;

function initMap() {
    map = new google.maps.Map(document.getElementById("map"), {
    center: {lat: 38.00784, lng: -122.522375},
    scrollwheel: false,
    zoom: 10,
    zoomControl: true,
    panControl: false,
    streetViewControl: false,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });

  // When a user clicks on a bear, an info window about that bear will appear.
  //
  // When they click on another bear, we want the previous info window to
  // disappear, so that only one window is open at a time.
  //
  // To do this, we'll define a single InfoWindow instance. All markers will
  // share this instance.
//   const bearInfo = new google.maps.InfoWindow();

  // Retrieving the information with AJAX.
  //
  // If you want to see what `/api/bears` returns, you should check `server.py`
//   $.get('/api/users', (users) => {
//     for (const user of users) {
      // Define the content of the infoWindow
      // const bearInfoContent = (`
      //   <div class="window-content">
      //     <div class="bear-thumbnail">
      //       <img
      //         src="/static/img/polarbear.jpg"
      //         alt="polarbear"
      //       />
      //     </div>

      //     <ul class="bear-info">
      //       <li><b>Bear gender: </b>${bear.gender}</li>
      //       <li><b>Bear birth year: </b>${bear.birthYear}</li>
      //       <li><b>Year captured: </b>${bear.capYear}</li>
      //       <li><b>Collared: </b>${bear.collared}</li>
      //       <li><b>Location: </b>${bear.capLat}, ${bear.capLong}</li>
      //     </ul>
      //   </div>
      // `);

    //   const userMarker = new google.maps.Marker({
    //     position: {
    //       lat: user.Latitude,
    //       lng: user.Longitude
    //     },
    //     title: `User ID: ${user.user_id}`,
    //     icon: {
    //       url: '/static/img/polarBear.svg',
    //       scaledSize: new google.maps.Size(50, 50)
    //     },
    //     map: map,
    //   });

      // bearMarker.addListener('click', () => {
      //   bearInfo.close();
      //   bearInfo.setContent(bearInfoContent);
      //   bearInfo.open(map, bearMarker);
      // });


//     }
//   }).fail(() => {
//     alert((`
//       We were unable to retrieve data about user :(
//     `));
//   });

}