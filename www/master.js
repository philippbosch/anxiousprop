$(document).ready(function() {
    $('a[href="#case-3-pdf"]').click(function(e) {
        if ($(this).data('running')) {
            alert('We are still creating your publication. Please bear with us.');
            return;
        }
        $(this).data('running', true);
        e.preventDefault();
        $(this).closest('article').append('<p class="pdf-status running">Creating your publication …</p>');
        $.getJSON('http://theanxiousprop.pb.io/randomize-publication/', function(data) {
            if (data['status'] != 'ok') {
                alert('An error occured. Sorry.');
                return;
            }
            var interval = window.setInterval(function() {
                $.getJSON('http://theanxiousprop.pb.io' + data['pick_up_url'], function(data) {
                    console.log(data);
                });
            }, 1000);
        });
    });
});