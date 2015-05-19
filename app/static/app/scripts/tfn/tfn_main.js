var tfn = window.tfn || {};

jQuery(function($){
  tfn.wrapper = $("#tfn-app .partial");
  tfn.partial = tfn.wrapper.attr("data-partial");
  tfn.home_category = tfn.home_category || "all";
  //router
  switch(tfn.partial){
    case "home":
      tfn.home();
      break;
    default:
  }

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
  
  //click events
  $('.header-tabs .tab').click(function(){
    if(tfn.selected_channel){
      var isDiffChannel = $(this).attr('data-selection') == tfn.selected_channel;
    }
    tfn.selected_channel = $(this).attr('data-selection');
    var header_dropdown = $('.header-dropdown');
    var expanded = header_dropdown.hasClass('expanded');
    $('.header-tabs .tab').removeClass('selected');
    $(this).addClass('selected');
    if(expanded && isDiffChannel){
      header_dropdown.removeClass('expanded');
    }else{
      header_dropdown.addClass('expanded');
    }
          
  });
  
});

tfn.home = function(){
  var fake_rundown_posts = [
    {
      title: "This is a LCS Rundown podcast episode",
      content: "This is the new website and here is the place an excerpt would go to show the general details of this post!",
      show: "rundown",
      hosts: ["motgnarom", "optimustom", "tsepha", "crediblemushroom", "cerealbawkz"],
      tags: ["esports", "pro play", "strategy", "poppywatch 2015", "guest", "NME gaming"],
      category: "podcast",
      video_url: "http://youtu.be/8x1oHRd46QM",
      image_url: "http://imgur.com/gallery/eRcR1fQ",
      stitcher_url: "http://app.stitcher.com/splayer/f/45272/36934480",
      itunes_url: "https://itunes.apple.com/us/podcast/lcs-podcast/id822327403"
    },
    {
      title: "This is a LCS Rundown podcast episode",
      content: "This is the new website and here is the place an excerpt would go to show the general details of this post!",
      show: "LCS Rundown",
      hosts: ["motgnarom", "optimustom", "tsepha", "crediblemushroom", "cerealbawkz"],
      tags: ["esports", "pro play", "strategy", "poppywatch 2015", "guest", "NME gaming"],
      category: "podcast",
      video_url: "http://youtu.be/8x1oHRd46QM",
      image_url: "http://imgur.com/gallery/eRcR1fQ",
      stitcher_url: "http://app.stitcher.com/splayer/f/45272/36934480",
      itunes_url: "https://itunes.apple.com/us/podcast/lcs-podcast/id822327403"
    }
  ];
  var fake_proper_posts = [
    {
      title: "This is a Tforce proper podcast episode",
      content: "This is the new website and here is the place an excerpt would go to show the general details of this post!",
      show: "proper",
      hosts: ["pwnophobia", "declawd", "daysuntold", "chirajaeden", "punchinjello"],
      tags: ["patch 5.2", "mechanics", "wave manipulation", "mailbag", "top lane", "dyrus"],
      category: "podcast",
      video_url: "http://youtu.be/8x1oHRd46QM",
      image_url: "http://imgur.com/gallery/eRcR1fQ",
      stitcher_url: "http://app.stitcher.com/splayer/f/27428/36930238",
      itunes_url: "https://itunes.apple.com/us/podcast/trinity-force-podcast-league/id485769640"
    },
    {
      title: "This is a Tforce proper podcast episode",
      content: "This is the new website and here is the place an excerpt would go to show the general details of this post!",
      show: "proper",
      hosts: ["pwnophobia", "declawd", "daysuntold", "chirajaeden", "punchinjello"],
      tags: ["patch 5.2", "mechanics", "wave manipulation", "mailbag", "top lane", "dyrus"],
      category: "podcast",
      video_url: "http://youtu.be/8x1oHRd46QM",
      image_url: "http://imgur.com/gallery/eRcR1fQ",
      stitcher_url: "http://app.stitcher.com/splayer/f/27428/36930238",
      itunes_url: "https://itunes.apple.com/us/podcast/trinity-force-podcast-league/id485769640"
    }
  ];
  var post_card = tfn.wrapper.find('.main__posts .post.template').clone();
  var body = tfn.wrapper.find('.main__posts');
  body.find('.post.cloned').remove();
  var target_posts;
  if(tfn.home_category == "all"){
    target_posts = fake_proper_posts;
  }
  
  switch(tfn.home_category){
    case "all":
      target_posts = fake_proper_posts.concat(fake_rundown_posts);
      fill_in_posts(target_posts);
      break;
    case "home":
      target_posts = fake_proper_posts.concat(fake_rundown_posts);
      fill_in_posts(target_posts);
      break;
    case "rundown":
      target_posts = fake_rundown_posts;
      fill_in_posts(target_posts);
      break;
    case "proper":
      target_posts = fake_proper_posts;
      fill_in_posts(target_posts);
      break;
    default:
      body.append("<span class=\"post cloned\">No posts are available for this category.</span>");
  }
  
  function fill_in_posts(target_posts){
    for(var i=0;i<target_posts.length;i++){
      var post = target_posts[i];
      var temp_card = post_card.clone().removeClass("template").addClass("cloned");
      temp_card.find('.post-title').html(post.title);
      temp_card.find('.post-content').html(post.content);
      temp_card.find('.post-show').html(post.show);
      var hosts_string = "Hosted by:";
      for(var j=0;j<post.hosts.length;j++){
        hosts_string = hosts_string + " " + post.hosts[j];
      }
      temp_card.find('.hosted-by').html(hosts_string);
      temp_card.find('.post-content').html(post.content);
      var tags_string = "Tags:";
      for(var k=0;k<post.tags.length;k++){
        tags_string = tags_string + " <a href=\"#\">" + post.tags[k] + "</a>";
      }
      temp_card.find('.post-tags').html(tags_string);
      body.append(temp_card);
    }
  }

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
  //END EXTRENAL CODE
}
















