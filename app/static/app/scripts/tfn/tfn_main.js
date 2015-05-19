jQuery(function($){

  // On click event for fourwards podcast #proof of concept
  $('#filter').on('submit', function (event) {
      event.preventDefault();
      filterType = "title"
      showName = "four wards"
      $.ajax({
          url: "filter/", // the endpoint
          type: "POST", // http method type
          data: { categoryToFilter: filterType, dbKey: showName }, // variables sent with the post request

          // handle a successful response
          success: function (json) {
              console.log("success"); //sanity check
              console.log(json); // log the returned json to the console
              //json.output will contain all of the actual info about shows
              //this will follow the format fake rundown and proper posts
              console.log(json.output[0]) //print info about first shwo returned
          },

          // handle a non-successful response
          error: function (xhr, errmsg, err) {
              $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                  " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
              console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
          }
      });
  });

  //START EXTERNAL CODE
  //Code for crfs token taken from https://gist.github.com/broinjc/db6e0ac214c355c887e5
  //Add {% csrf_token %} to forms that need to call down into python.
  // This function gets cookie with a given name
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }
  function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
          (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
          // or any other URL that isn't scheme relative or absolute i.e relative.
          !(/^(\/\/|http:|https:).*/.test(url));
  }

  $.ajaxSetup({
      beforeSend: function (xhr, settings) {
          if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
              // Send the token to same-origin, relative URLs only.
              // Send the token only if the method warrants CSRF protection
              // Using the CSRFToken value acquired earlier
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
  });
}
















