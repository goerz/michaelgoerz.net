//http://stackoverflow.com/questions/17534661/make-anchor-link-go-some-pixels-above-where-its-linked-to

// The function actually applying the offset
function offsetAnchor() {
    // This if statement is optional. It is just making sure that
    // there is a valid anchor to offset from.
    if($(location.hash).length !== 0) {
        window.scrollTo(window.scrollX, window.scrollY - 60);
    }
}

// This will capture hash changes while you are on the same page
$(window).on("hashchange", function () {
    offsetAnchor();
    location.hash && $(location.hash + '.collapse').collapse('show');
});

// This is here so that when you enter the page with a hash,
// it can provide the offset in that case too. Having a timeout
// seems necessary to allow the browser to jump to the anchor first.
window.setTimeout(function() {
    offsetAnchor();
}, 100); // The delay of 1 is arbitrary and may not always work right (although it did in my testing).
