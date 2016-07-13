$(function() {
  // Instances table refresh button
  $(document).on('click', 'button[data-team-action="resfresh"]', function(event){
    $('i', this).addClass('fa-spin fa-spinner');
    refreshInstanceTable($(this).closest('.instances-table-container'));
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
  var container = $(event.target).closest('.instances-table-container');
  event.preventDefault();
  $.ajax({
      url: url,
      type: 'get',

      complete: function(xhr, status) {
        var json = JSON.parse(xhr.responseText);
        if ('messages_html' in json) {
          $('#messages-container').empty(); // clear messages div
          $('#messages-container').html(json.messages_html);
        }
        $('#messages-container').children().hide().fadeIn(500).delay(4000).fadeOut(500);
        refreshInstanceTable(container);
        setTimeout(refreshInstanceTable, 2000, container);
        setTimeout(refreshInstanceTable, 5000, container);
      }
    });
}
