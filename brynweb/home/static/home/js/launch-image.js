$(function() {
  $('#id_server_key_name').closest('.form-group').hide();
  $('#id_server_key').closest('.form-group').hide();

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
