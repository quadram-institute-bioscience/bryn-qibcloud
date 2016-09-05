$(function() {
  // Instances table refresh button
  $(document).on('click', 'button[data-team-action="resfresh"]', function(event){
    $('i', this).addClass('fa-spin fa-spinner');
    refreshInstanceTable($(this).closest('.instances-table-container'));
  });

  // Custom launch form toggle ssh key fields
  if ($('#id_server_key_name_choice').val() != 'bryn:new') {
    $('#id_server_key_name').closest('.form-group').hide();
    $('#id_server_key').closest('.form-group').hide();
  }

  $('#id_server_key_name_choice').change(function() {
    var key_name = $('#id_server_key_name').closest('.form-group');
    var key = $('#id_server_key').closest('.form-group');
    if ($(this).val() == 'bryn:new') {
      key_name.show();
      key.show();
    } else {
      key_name.hide();
      key.hide();
    }
  });
});

// Refresh instaces table
function refreshInstanceTable(container) {
  $.ajax({
      url: '/get_instances_table',
      type: 'get',
      data: {team_id: $(container).attr('data-team-id')},

      success: function(json) {
        $('.instances-table-container').html(json.instances_table);
      },
    })
}

// Instance actions
function ajaxInstanceAction(event, url) {
  event.preventDefault();
  $(event.target).closest('ul').siblings('.dropdown-toggle').children('i:first-child').addClass('fa-spin fa-spinner');
  var teamContainer = $(event.target).closest('.team-container');
  var tableContainer = $(event.target).closest('.instances-table-container');
  $.ajax({
      url: url,
      type: 'get',

      complete: function(xhr, status) {
        var json = JSON.parse(xhr.responseText);
        if ('messages_html' in json) {
          $('.messages-container', teamContainer).empty(); // clear messages div
          $('.messages-container', teamContainer).html(json.messages_html);
        }
        $('.messages-container', teamContainer).children().hide().fadeIn(500).delay(10000).fadeOut(500);
        refreshInstanceTable(tableContainer);
        setTimeout(refreshInstanceTable, 2000, tableContainer);
        setTimeout(refreshInstanceTable, 5000, tableContainer);
      }
    });
}
