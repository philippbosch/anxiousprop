$(document).ready(function() {
    $('a[href="#case-3-pdf"]').click(function(e) {
        var $link = $(this);
        if ($link.data('running')) {
            alert('We are still creating your publication. Please bear with us.');
            return false;
        } else if ($link.data('ready')) {
            return true;
        }
        $link.data('running', true);
        e.preventDefault();
        $link.closest('article').append('<p class="pdf-status running">The content of your feuilleton is being randomized …</p>');
        $.getJSON('http://theanxiousprop.pb.io/randomize-publication/?callback=?', function(data) {
            if (data['status'] != 'ok') {
                alert('An error occured. Sorry.');
                return;
            }
            var interval = window.setInterval(function() {
                $.getJSON('http://theanxiousprop.pb.io' + data['pick_up_url'] + '?callback=?', function(data) {
                    if (data['status'] == 'ready') {
                        window.clearInterval(interval);
                        $('.pdf-status').removeClass('running').html('<a href="' + data['pdf_url'] + '">Click here for your version of the The Black Swan Issue</a>.');
                        $link.attr('href', data['pdf_url']);
                        $link.data('ready', true);
                        $link.data('running', false);
                    }
                });
            }, 1000);
        });
    });
});