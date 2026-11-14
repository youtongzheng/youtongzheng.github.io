---
title: "Live Weather"
permalink: /weather/
author_profile: true
---

Live maps from NOAA. Each image reloads by itself while this page is open: radar every 2 minutes, satellite every 5, and weather maps every 30. Click an image for its source page.

### Houston radar (KHGX)
<a href="https://radar.weather.gov/station/khgx/standard"><img class="live" data-refresh="2" src="https://radar.weather.gov/ridge/standard/KHGX_loop.gif" alt="Houston radar loop"></a>
<small class="stamp"></small>

### GOES-19 GeoColor satellite image (continental U.S.)
<a href="https://www.star.nesdis.noaa.gov/GOES/conus.php?sat=G19"><img class="live" data-refresh="5" src="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/1250x750.jpg" alt="GOES-19 GeoColor"></a>
<small class="stamp"></small>

### GOES-19 water vapor imagery (band 9)
<a href="https://www.star.nesdis.noaa.gov/GOES/conus.php?sat=G19"><img class="live" data-refresh="5" src="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/09/1250x750.jpg" alt="GOES-19 water vapor"></a>
<small class="stamp"></small>

### U.S. radar mosaic
<a href="https://radar.weather.gov/"><img class="live" data-refresh="2" src="https://radar.weather.gov/ridge/standard/CONUS_loop.gif" alt="U.S. radar mosaic loop"></a>
<small class="stamp"></small>

### NWS surface analysis
<a href="https://www.wpc.ncep.noaa.gov/html/sfc-zoom.php"><img class="live" data-refresh="30" src="https://www.wpc.ncep.noaa.gov/sfc/namussfcwbg.gif" alt="NWS surface analysis"></a>
<small class="stamp"></small>

### WPC short-range forecast (day 1)
<a href="https://www.wpc.ncep.noaa.gov/basicwx/basicwx_ndfd.php"><img class="live" data-refresh="30" src="https://www.wpc.ncep.noaa.gov/basicwx/92fndfd.gif" alt="WPC day 1 forecast"></a>
<small class="stamp"></small>

Sources: [NOAA/NESDIS STAR](https://www.star.nesdis.noaa.gov/GOES/), [National Weather Service](https://radar.weather.gov/), [Weather Prediction Center](https://www.wpc.ncep.noaa.gov/).

<script>
(function () {
  var imgs = document.querySelectorAll("img.live");
  function load(img) {
    var base = img.getAttribute("data-base") || img.src.split("?")[0];
    img.setAttribute("data-base", base);
    img.src = base + "?t=" + Date.now();
  }
  imgs.forEach(function (img) {
    img.addEventListener("load", function () {
      var s = img.parentNode.nextElementSibling;
      if (s && s.classList.contains("stamp")) s.textContent = "Loaded " + new Date().toLocaleTimeString([], {hour: "numeric", minute: "2-digit"});
    });
    load(img);
    setInterval(function () { load(img); }, parseFloat(img.getAttribute("data-refresh")) * 60000);
  });
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "visible") imgs.forEach(load);
  });
})();
</script>
