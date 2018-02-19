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

        // Only do this for screen sizes less than 800px
        if (isElementInViewport($elem) && !window.matchMedia("(min-width: 800px)").matches) {
            // Start the animation
            $elem.className = "image-button-wrapper image-button-animation";
        } else {
            $elem.className = "image-button-wrapper";
        }
    }
}

// Capture scroll events
$(window).scroll(function(){
    checkAnimation();
});

$(document).ready(function(){
    $('#hero #family').click(function(){
        $('#hero').css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4) ), url(./assets/imgs/hero_family.jpg)');
        $(this).text('family');
    })
})
