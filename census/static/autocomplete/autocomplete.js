// Taken from this example:
// https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/javascript/examples/places-autocomplete-addressform

// This will look at element with ID autoCompleteElemendId and apply Google's Web API Auto-complete.

// In the geolocate() function we apply a bias towards the "center" of Alameda county and a 4KM radius
// This gives an autocomplete with more Alameda County relevant addresses

var placeSearch, autocomplete;
var autoCompleteElemendId = 'id_location';
lat_id = 'id_lat';
lon_id = 'id_lon';

function initAutocomplete() {
  // Create the autocomplete object, restricting the search predictions to
  // geographical location types.
  autocomplete = new google.maps.places.Autocomplete(
      document.getElementById(autoCompleteElemendId));

  // Avoid paying for data that you don't need by restricting the set of
  // place fields that are returned to just the address components.
  autocomplete.setFields(['address_component', 'geometry']);

  // When the user selects an address from the drop-down, populate the
  // address fields in the form.
  autocomplete.addListener('place_changed', fillInAddress);
  geolocate();
}

function fillInAddress() {
  // Get the place details from the autocomplete object.
  var place = autocomplete.getPlace();
  // https://developers-dot-devsite-v2-prod.appspot.com/maps/documentation/javascript/reference/coordinates#LatLngBounds
  // var bounds = autocomplete.getBounds();
  lat = place.geometry.location.lat().toFixed(6)
  lon = place.geometry.location.lng().toFixed(6)
  lat_input = document.getElementById(lat_id);
  lon_input = document.getElementById(lon_id);
  if (lat_input) { lat_input.value = lat };
  if (lon_input) { lon_input.value = lon };
}

// Bias the autocomplete object to the user's geographical location,
// as supplied by the browser's 'navigator.geolocation' object.
function geolocate() {
  // Set the center in Alameda county with 4 KM radius
  var geolocation = {
    lat: 37.609241,
    lng: -121.834599
  };
  var circle = new google.maps.Circle({ center: geolocation, radius: 40000 });
  autocomplete.setBounds(circle.getBounds());
}