// Check if a specific HTML element is in view
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
    var $elems = $('.image-button');
    for (var i = 0; i < $elems.length; i++) {
        $elem = $elems[i];

        // Only do this for screen sizes less than 800px
        if (isElementInViewport($elem) && !window.matchMedia("(min-width: 800px)").matches) {
            // Start the animation
            $elem.className = "image-button image-button-animation";
        } else {
            $elem.className = "image-button";
        }
    }
}

// Anything related to the navigation menu
function navMenu() {
    let speed = "fast";
    $( ".menu li" ).click(function() {
        $( ".cross" ).hide();
        $( ".hamburger" ).show();
        $( ".menu" ).slideToggle(speed);
    });

    $( ".hamburger" ).click(function() {
        $( ".hamburger" ).hide();
        $( ".cross" ).show();
        $( ".menu" ).slideToggle(speed);
    });

    $( ".cross" ).click(function() {
        $( ".cross" ).hide();
        $( ".hamburger" ).show();
        $( ".menu" ).slideToggle(speed);
    });

    $('html').on('click touchstart', function() {
        if ($('.menu').is(':visible')) {
            $( ".cross" ).hide();
            $( ".hamburger" ).show();
            $( ".menu" ).slideToggle(speed);
        }
    });

    $('#nav-wrapper').on('click touchstart', function() {
        event.stopPropagation();
    });
}

function showAllCompanies() {
    $("#portfolio #show-all-button").click(function() {
        $("#photobanner").toggleClass("photobanner-scroll photobanner-show-all");
    });
}

function easterEgg(){
    $('#hero #family').click(function(){
        $('#hero').css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4) ), url(./assets/imgs/hero_family.jpg)');
        $(this).text('family');
    })
}

// Capture scroll events
$(window).scroll(function(){
    checkAnimation();
});

$(document).ready(function(){
    navMenu();
    easterEgg();
    showAllCompanies();
})

particlesJS.load('particles', '/assets/js/particles.json', function() {
  console.log('callback - particles.js config loaded');
});
