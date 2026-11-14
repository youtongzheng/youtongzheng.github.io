---
title: "Live Weather"
permalink: /weather/
author_profile: true
---

Live maps from NOAA. Radar and satellite images are animated loops of the most recent hours; the weather maps are the latest official analysis and forecast. Every image reloads by itself while this page is open. Click an image for its source page.

### Houston radar (KHGX)
<a href="https://radar.weather.gov/station/khgx/standard"><img class="live" data-refresh="2" src="https://radar.weather.gov/ridge/standard/KHGX_loop.gif" alt="Houston radar loop"></a>
<small class="stamp"></small>

### GOES-19 GeoColor satellite loop (continental U.S.)
<a href="https://www.star.nesdis.noaa.gov/GOES/conus_band.php?sat=G19&band=GEOCOLOR&length=24"><img class="live" data-refresh="15" src="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/GEOCOLOR/GOES19-CONUS-GEOCOLOR-625x375.gif" alt="GOES-19 GeoColor loop"></a>
<small class="stamp"></small>

### GOES-19 upper-level water vapor loop (band 8)
<a href="https://www.star.nesdis.noaa.gov/GOES/conus_band.php?sat=G19&band=08&length=24"><img class="live" data-refresh="15" src="https://cdn.star.nesdis.noaa.gov/GOES19/ABI/CONUS/08/GOES19-CONUS-08-625x375.gif" alt="GOES-19 water vapor loop"></a>
<small class="stamp"></small>

### U.S. radar mosaic
<a href="https://radar.weather.gov/"><img class="live" data-refresh="2" src="https://radar.weather.gov/ridge/standard/CONUS_loop.gif" alt="U.S. radar mosaic loop"></a>
<small class="stamp"></small>

### NWS surface analysis (latest, issued every 3 hours)
<a href="https://www.wpc.ncep.noaa.gov/html/sfc-zoom.php"><img class="live" data-refresh="30" src="https://www.wpc.ncep.noaa.gov/sfc/namussfcwbg.gif" alt="NWS surface analysis"></a>
<small class="stamp"></small>

### WPC short-range forecast (latest day-1 forecast)
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
