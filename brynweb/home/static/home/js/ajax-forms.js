// AJAX post
function ajaxPost(form, resetOnSuccess, afterSuccess) {
  var teamContainer = $(form).closest('.team-container');

  // optional resetOnSuccess=true
  if (resetOnSuccess === undefined) {
    var resetOnSuccess = true;
  }

  // Remove errors before new request
  $('.has-error', form).removeClass('has-error');
  $('.help-block', form).remove();

  // Update button to show in-progress spinner
  $('button[type="submit"] i', form).addClass('fa-spin fa-spinner');

  // Make the ajax request
  $.ajax({
    url : $(form).attr('action'),
    type : $(form).attr('method'),
    data : $(form).serialize(),

    success : function(json) {
      if (resetOnSuccess) {
        $(form).trigger("reset");
      }
      if (afterSuccess !== undefined) {
        afterSuccess(form);
      }
    },

    error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      var json = JSON.parse(xhr.responseText);
      if ('errors' in json) {
        for (var error in json.errors) {
          var id = '#id_' + error;
          var parent = $(id, form).parents('.form-group');
          parent.addClass('has-error');
          if ($('.help-block', parent).length) {
            $('.help-block', parent).text(json.errors[error]);
          } else {
            parent.append('<span class="help-block">' + json.errors[error] + '</span>');
          }
        }
      }
    },

    complete : function(xhr, status) {
      $('button[type="submit"] i', form).removeClass('fa-spin fa-spinner');
      var json = JSON.parse(xhr.responseText);
      if ('messages_html' in json) {
        $('.messages-container', teamContainer).html(json.messages_html);
      }
      $('.messages-container', teamContainer).children().hide().fadeIn(500).delay(10000).fadeOut(500);
    }
  });
}

$(function() {
  /*
  Ajax CSRF
  */

  // Create a header with csrftoken

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
    beforeSend: function(xhr, settings) {
      if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
        // Send the token to same-origin, relative URLs only.
        // Send the token only if the method warrants CSRF protection
        // Using the CSRFToken value acquired earlier
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
      }
    }
  });

  function refreshInstanceAfterForm(form) {
    var tableContainer = $(form).closest('.team-container').find('.instances-table-container');
    $('html, body').stop().animate({scrollTop: tableContainer.offset().top}, '500', 'swing');
    setTimeout(refreshInstanceTable, 2000, tableContainer);
    setTimeout(refreshInstanceTable, 10000, tableContainer);
  }

  // AJAX post on submit
  $(document).on('submit', '.launch-custom-form', function(event){
    event.preventDefault();
    ajaxPost(this, true, refreshInstanceAfterForm);
  });
  $(document).on('submit', '.launch-gvl-form', function(event){
    event.preventDefault();
    ajaxPost(this, true, refreshInstanceAfterForm);
  });
});