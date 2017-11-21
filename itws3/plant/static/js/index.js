'use strict';

function showWeather(data1, data2, data3) {
  var today = data1.current_observation,
      forecast = data2.forecast.simpleforecast.forecastday;

  // To Be Implemented:  hourly = data3[0].hourly_forecast;

  // Five regions use Fahrenheit by default. For simplicity, assuming
  // these regions are okay with miles and inches as well
  var imperialUnitRegions = ['US', 'BS', 'BZ', 'KY', 'PL'],
      region = today.display_location.country_iso3166;

  var units = 'celsius';
  if (imperialUnitRegions.indexOf(region) > -1) units = 'fahrenheit';

  // Display date/time formats in US format by default unless browser language is available
  var locale = 'en-US';
  if (navigator.language) locale = navigator.language;

  var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
      currentDay = new Date().toLocaleDateString(locale, {
    weekday: 'long'
  }),
      currentTime = new Date().toLocaleTimeString(locale, {
    hour: '2-digit',
    minute: '2-digit'
  }),
      dateToday = currentDay + ', ' + currentTime;

  $('#city').text(today.display_location.full);
  $('#date').text(dateToday);
  $('#current-conditions').text(today.weather);
  $('#weather-icon').attr('src', today.icon_url.replace('http://', 'https://'));
  $('#humidity').text(today.relative_humidity);

  function showImperialUnits() {
    $('#temperature').text(today.temp_f.toFixed(0));
    $('#degree-units').text('°F | °C');
    $('#precipitation').text(today.precip_today_in + '"');
    $('#wind').text(today.wind_mph + ' mph');
  }

  function showMetricUnits() {
    $('#temperature').text(today.temp_c);
    $('#degree-units').text('°C | °F');
    $('#precipitation').text(today.precip_today_metric + 'mm');
    $('#wind').text(today.wind_kph + ' kph');
  }

  units === 'fahrenheit' ? showImperialUnits() : showMetricUnits();

  // Change units when clicking on the "F | C"
  $('#degree-units').on('click', function (e) {
    if ($('#degree-units').text() === '°C | °F') {
      // convert to fahrenheit
      showImperialUnits();
      $.each($('.high-temp, .low-temp'), function (i, val) {
        return $(val).html($(val).data('fahrenheit') + '&deg;');
      });
    } else {
      // convert to celsius
      showMetricUnits();
      $.each($('.high-temp, .low-temp'), function (i, val) {
        return $(val).html($(val).data('celsius') + '&deg;');
      });
    }
  });

  // 6-day forecast
  for (var i = 0; i < 6; i++) {
    $('#weather-forecast').append('<div class="col s6 m2 forecast-day center-align">\n         <div>' + forecast[i].date.weekday_short + '</div>\n         <div><img src="' + forecast[i].icon_url.replace('http://', 'https://') + '" alt="weather icon"></div>\n         <div class="col s6 high-temp" \n              data-celsius="' + forecast[i].high.celsius + '" \n              data-fahrenheit="' + forecast[i].high.fahrenheit + '">\n           ' + forecast[i].high[units] + '&deg;\n         </div>\n         <div class="col s6 low-temp" \n              data-celsius="' + forecast[i].low.celsius + '" \n              data-fahrenheit="' + forecast[i].low.fahrenheit + '">\n           ' + forecast[i].low[units] + '&deg;\n         </div>\n       </div>');
  }
  // Initialize tooltips
  $('.tooltipped').tooltip({
    delay: 50
  });

  // Close tooltips on mobile and reinitialize
  $('#weather-card').on('click', function (e) {
    $('.tooltipped').tooltip('close').tooltip({
      delay: 50
    });
  });

  displayFinalPage();
}

// Display errors from API calls
function ApiError(err) {
  $('#error').html('Error. Please try again later.');
  $('.spinner').hide();
}

function getWeatherData(location) {
  var key = 'd301cc052928a635',
      todayURL = 'https://api.wunderground.com/api/' + key.replace(/g/g, 'c') + '/conditions/q/' + location + '.json?callback=?',
      hourlyURL = 'https://api.wunderground.com/api/' + key.replace(/g/g, 'c') + '/hourly/q/' + location + '.json?callback=?',
      tenDayForecastURL = 'https://api.wunderground.com/api/' + key.replace(/g/g, 'c') + '/forecast10day/q/' + location + '.json?callback=?';

  $.getJSON(todayURL).done(function (data1) {
    $.getJSON(tenDayForecastURL).done(function (data2) {
      showWeather(data1, data2);
    }).fail(ApiError);
  }).fail(ApiError);
}

// Attempt to get location via navigator.geolocation first
// If that is blocked or fails, use Weather Underground's IP-based location.
function getLocation() {

  // navigator.geolocation supported and not blocked
  function success(pos) {
    var url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng=' + pos.coords.latitude + ',' + pos.coords.longitude;

    // navigator.geolocation doesn't give us a city name
    // use the Google Maps reverse geocode API to get the city name
    $.getJSON(url, function (data) {
      for (var i = 0; i < data.results.length; i++) {
        if (data.results[i].types.includes('locality')) {
          getWeatherData(pos.coords.latitude + ',' + pos.coords.longitude);
          //getBackgroundImage(pos.coords.latitude, pos.coords.longitude, data.results[i].formatted_address);
          return;
        }
      }
    }).fail(ApiError);
  }

  // navigator.geolocation blocked/not supported
  function error() {
    getWeatherData('autoip');

    // let users know their location can be more accurate over HTTPS
    if (window.location.protocol === 'http:') $('#weather-card').append('<div class="location-warning">** <small>Open this page over HTTPS and enable \n       location for more accurate results</small></div>');

    function freeGeoIp() {
      $.getJSON('https://freegeoip.net/json?callback=?', function (data) {
        getBackgroundImage(data.latitude, data.longitude, data.city);
      }).fail(ApiError);
    }

    function ipinfo() {
      $.getJSON('https://ipinfo.io/json?callback=?', function (data) {
        getBackgroundImage(data.loc.split(',')[0], data.loc.split(',')[1], data.city);
      }).fail(freeGeoIp);
    }

    ipinfo();
  }

  navigator.geolocation.getCurrentPosition(success, error);
}

function getBackgroundImage(lat, lon, city) {
  var key = 'd58351e65962ehd35f44h614512ca451',
      url = 'https://api.flickr.com/services/rest/?method=flickr.photos.search&api_key=' + key.replace(/h/g, 'b').replace(/6/g, '9') + '&lat=' + lat + '&lon=' + lon + '&accuracy=11&extras=url_l,tags&format=json' + '&sort=interestingness-desc&per_page=100&' + 'tags=' + city.split(',')[0] + ',monument,landmark,sunrise&nojsoncallback=1';

  $.getJSON(url, function (data) {
    // get a random unsplash nature photo if Flickr doesn't return any results
    if (data.photos.total === '0') {
      displayBackground('https://source.unsplash.com/category/nature/1600x900');
      return;
    }

    // Try to get the best picture based on screen size
    // landscape display
    if (window.innerHeight <= window.innerWidth) {
      for (var i = 0; i < data.photos.photo.length; i++) {
        if (+data.photos.photo[i].height_l <= +data.photos.photo[i].width_l && +data.photos.photo[i].height_l <= window.innerHeight) {
          displayBackground(data.photos.photo[i].url_l);
          return;
        }
      }
    } else {
      // portrait display
      for (var i = 0; i < data.photos.photo.length; i++) {
        if (+data.photos.photo[i].height_l >= +data.photos.photo[i].width_l && +data.photos.photo[i].height_l <= window.innerWidth) {
          displayBackground(data.photos.photo[i].url_l);
          return;
        }
      }
    }

    // if no suitable image based on screen size, just give the first one from the results
    if ($('body').css('background-image') === 'none') {
      displayBackground(data.photos.photo[0].url_l);
    }
  }).fail(ApiError);
}
// callback for determining when async functions are complete
// if we have a background image and weather data ready, display the page
function displayFinalPage() {
  if ($('#weather-forecast').html() !== "") {
    $('.spinner').hide();
    $('.hide').removeClass('hide');
    $('main').hide().fadeIn(3000);
    $('#weather-card').hide().fadeIn(3000);
  }
}

$(document).ready(getLocation);