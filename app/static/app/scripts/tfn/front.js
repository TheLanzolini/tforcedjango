front.jsvar tfn = window.tfn || {};

jQuery(function($){
  tfn.wrapper = $("#tfn-app .partial");
  tfn.partial = tfn.wrapper.attr("data-partial");
  tfn.selected_show = "featured";
  tfn.home_category = tfn.home_category || "league";
  //router
  switch(tfn.partial){
    case "home":
      tfn.home();
      break;
    default:
  }
  
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

  $('.dropdown-content .dropdown-channel').click(function(){
    tfn.selected_show = $(this).attr('data-channel');
    console.log(tfn.selected_show);
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
  var post_sections = body.find('post-section');

  switch(tfn.home_category){
    case "league":
      fillLeague();
      break;
  }

  function fillLeague(){
    switch(tfn.selected_show){
      case "featured":
        // tfn.queriedPosts = 
        fillPosts(fake_proper_posts.concat(fake_rundown_posts));
        break;
      case "proper":
        fillPosts("proper");
        break;
    }
  }

  function fillPosts(posts){
    console.log(posts);
    var num_posts = posts.length;
    var num_sections = Math.ceil(num_posts/6);
    console.log(num_sections);
    var stop = 6;
    for(var i=0;i<num_sections;i++){
      var section = $('.post-section.template').clone().addClass('cloned').removeClass('template');
      var post = section.find('.post.template').clone().addClass('cloned').removeClass('template');
      console.log(post);
      for(var j=0;j<6;j++){
        var p = post.clone();
        var target_post = posts[j];
        if(target_post){
          p.find('.post-title').html(target_post.title);
          p.find('.post-info .excerpt').html(target_post.content);
          section.append(p);
        }
      }
      body.append(section);
    }
  }

  console.log(tfn);
}
















