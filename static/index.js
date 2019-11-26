var xhr = new XMLHttpRequest();
xhr.open('GET', "/send_values");
xhr.send();

xhr.onload = function() {
  if (xhr.status != 200) { // analyze HTTP status of the response
    alert(`Error ${xhr.status}: ${xhr.statusText}`); // e.g. 404: Not Found
  }
};

xhr.onprogress = function(event) {
  if (event.lengthComputable) {
    var config = JSON.parse(xhr.responseText);
    document.getElementById("CAP_PROP_BRIGHTNESS").value = config["CAP_PROP_BRIGHTNESS"];
    document.getElementById("CAP_PROP_CONTRAST").value = config["CAP_PROP_CONTRAST"];
    document.getElementById("CAP_PROP_SATURATION").value = config["CAP_PROP_SATURATION"];
    document.getElementById("CAP_PROP_SHARPNESS").value = config["CAP_PROP_SHARPNESS"];
    document.getElementById("CAP_PROP_GAMMA").value = config["CAP_PROP_GAMMA"];
    document.getElementById("CAP_PROP_WHITE_BALANCE_BLUE_U").value = config["CAP_PROP_WHITE_BALANCE_BLUE_U"];
    document.getElementById("CAP_PROP_GAIN").value = config["CAP_PROP_GAIN"];
    document.getElementById("CAP_PROP_PAN").value = config["CAP_PROP_PAN"];
    document.getElementById("CAP_PROP_TILT").value = config["CAP_PROP_TILT"];
    document.getElementById("CAP_PROP_ZOOM").value = config["CAP_PROP_ZOOM"];
    document.getElementById("CAP_PROP_EXPOSURE").value = config["CAP_PROP_EXPOSURE"];
    document.getElementById("CAP_PROP_BACKLIGHT").value = config["CAP_PROP_BACKLIGHT"];
    document.getElementById("CAP_PROP_ROLL").value = config["CAP_PROP_ROLL"];
    document.getElementById("CAP_PROP_IRIS").value = config["CAP_PROP_IRIS"];
    document.getElementById("CAP_PROP_FOCUS").value = config["CAP_PROP_FOCUS"];
    document.getElementById("CAP_PROP_HUE").value = config["CAP_PROP_HUE"];
  }
};

xhr.onerror = function() {
  alert("Request failed");
};
