//http://stackoverflow.com/questions/12008389/linking-to-a-section-of-an-accordion-from-another-page
$(document).ready(function () {
  location.hash && $(location.hash + '.collapse').collapse('show');
});
