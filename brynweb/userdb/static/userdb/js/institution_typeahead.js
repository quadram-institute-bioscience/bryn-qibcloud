 $(function() {
  var institutions = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.whitespace,
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    prefetch: '/user/institutions/typeahead/'
  });
  $('#id_institution').typeahead({
    hint: true,
    highlight: true,
    minLength: 0
  },
  {
    name: 'institutions',
    source: institutions,
    limit: 10
  });
});