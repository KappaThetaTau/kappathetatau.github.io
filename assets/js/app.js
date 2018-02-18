function isElementInViewport(elem) {
    var $elem = $(elem);
    var halfWindow = $(window).height() / 2;

    // Get the position of the element on the page.
    var elemTop = Math.round( $elem.offset().top );
    var elemBottom = elemTop + $elem.height();

    return ((elemTop < window.scrollY + halfWindow) && (elemBottom > window.scrollY + halfWindow));
}

// Check if it's time to start the animation.
function checkAnimation() {
    var $elems = $('.image-button-wrapper');
    for (var i = 0; i < $elems.length; i++) {
        $elem = $elems[i];

        if (isElementInViewport($elem)) {
            // Start the animation
            $elem.className += " image-button-animation";
        } else {
            $elem.className = "image-button-wrapper";
        }
    }
}

// Capture scroll events
$(window).scroll(function(){
    checkAnimation();
});

