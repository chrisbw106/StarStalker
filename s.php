<?php 
//Check if they set their stuff
if(!isset($_GET['location'])){
	header('Location: index.html');    
}
if(($_GET['location'] == "City, State") or ($_GET['location'] == "")){
	header('Location: index.html');
}
if(($_GET['location'] == "City, State") and ($_GET['starname'] == "Star Name (optional)")){
	header('Location: index.html');
}
//If so save it to file for the python to use
$input_location =  $_GET["location"] . "\n";
$input_name = $_GET["starname"] . "\n";
$input_lat = $_GET["lat"] . "\n";
$input_lng = $_GET["lng"];

if(($_GET['starname'] == "Star Name (optional)") or ($_GET['starname'] == "")){
	$input_name = "null\n";
}

$inputFile = "input_data.txt";
$fh = fopen($inputFile, 'w') or die("Unable to use input!");
fwrite($fh, $input_location);
fwrite($fh, $input_name);
fwrite($fh, $input_lat);
fwrite($fh, $input_lng);
fclose($fh);

//Call Python here

//Read Python Rankings

?>

<!DOCTYPE html>
<html>
<head>
<link rel="icon" 
      type="image/png" 
      href="http://i1200.photobucket.com/albums/bb323/coharkyaeon/favicon.png">
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no" />
    <style type="text/css">
      body { height: 100%; margin: 0; padding: 0 }
      #map-canvas { height: 800px; width:100% }
    </style>
    <script type="text/javascript"
      src="https://maps.googleapis.com/maps/api/js?key=AIzaSyAJew0TdvMP0xMR5I87tRB1jXDZJWh20HA&sensor=false">
    </script>
    <script>
	//Parse out the URL since javascript is lame
	function getUrlVars() {
		var vars = {};
		var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,    
		function(m,key,value) {
		  vars[key] = value;
		});
		return vars;
	  }
	var geocoder;
	var map;
	var x=document.getElementById("flocation");
	
	function initialize() {
      var lat = parseFloat(getUrlVars()["lat"]);
	  var lng = parseFloat(getUrlVars()["lng"]);
	  geocoder = new google.maps.Geocoder();
	  var latlng = new google.maps.LatLng(lat, lng);
	  var mapOptions = {
		zoom: 12,
		center: latlng
	  }
	  map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);
	}
	
	//Adjust map to current set location
	function codeAddress() {
	  var address = document.getElementById('flocation').value;
	  geocoder.geocode( { 'address': address}, function(results, status) {
		if (status == google.maps.GeocoderStatus.OK) {
		  map.setCenter(results[0].geometry.location);
		  var marker = new google.maps.Marker({
			  map: map,
			  position: results[0].geometry.location
		  });
		} else {
		  alert('Geocode was not successful for the following reason: ' + status);
		}
	  });
	}
	//Get the Lat and Lng for the form fields so the map knows where to go upon loading
	function getLatLng() {
		var y=document.getElementById("flat");
		var z=document.getElementById("flng");
		var addy = document.getElementById("flocation").value;
		alert(addy);
		geocoder.geocode( { 'address': addy}, function(results2, status2) {
		if (status2 == google.maps.GeocoderStatus.OK) {
			  var input2 = results2[0].geometry.location;
			  var latlngStr2 = String(input2).split(',', 2);
			  var lat2 = parseFloat(latlngStr2[0].substring(1));
			  var lng2 = parseFloat(latlngStr2[1]);
			  y.value=lat2;
			  z.value=lng2;
		} else {
		  alert('Geocode was not successful for the following reason: ' + status);
		}
		});
	}

      google.maps.event.addDomListener(window, 'load', initialize);
	  window.onload = codeAddress();
    </script>
    
<title>Star Stalker</title>
  <link href="style.css" rel="stylesheet" type="text/css">
</head>
<body>
<table id="searchbar" width="100%"  height="75px" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="350px"><a href="index.html"><img src="sbanner.png" width="350" height="75" alt="Star Stalker"></a></td>
    <td><form id="stalk" name="stalk" method="get" action="s.php" onsubmit="this.submit();return false;"> <table width="600" border="0" cellspacing="0" cellpadding="0">
          <tr valign="middle">
            <td valign="middle" align="center"><input name="location" type="text" id="flocation" value="<?php echo $_GET["location"]; ?>" onChange="getLatLng()"/></td>
            <td valign="middle" align="center"><input name="starname" type="text" id="fstarname" value="<?php echo $_GET["starname"]; ?>" /></td>      <input name="lat" type="hidden" id="flat" value="<?php echo $_GET["lat"]; ?>" />
      		<input name="lng" type="hidden" id="flng" value="<?php echo $_GET["lng"]; ?>" />
            <td valign="middle" align="center"><input type="image" id="submit" src="slbutton.png" height="51" width="50" /></td>
          </tr>
        </table>      
    </form></td>
  </tr>
</table>
<table width="100%" height="100%" border="0" cellspacing="0" cellpadding="0">
  <tr>
    <td width="300px" valign="top">Location: 
    <?php echo $_GET["location"]; ?><br>
Star Name: <?php echo $_GET["starname"]; ?><br>
<input type="button" value="Find" onclick="codeAddress()">
</td>
    <td valign="top"><div id="map-canvas"/></td>
  </tr>
</table>


</body>
</html>