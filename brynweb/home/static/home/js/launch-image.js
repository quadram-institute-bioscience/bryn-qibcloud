$(function() {
  $('#id_server_key_name').closest('.form-group').hide();

  $('#id_server_key_name_choice').change(function() {
    var target = $('#id_server_key_name').closest('.form-group').show();
    if ($(this).val() == 'bryn:new') {
      target.show();
    } else {
      $('input', target).val('');
      target.hide();
    }
  });
});
