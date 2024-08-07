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

var slideIndex = [0, 0];

function plusSlides(n, id) {
    var idx;
    switch (id) {
        case 'brotherhood':
            idx = 0;
            break;
        case 'service':
            idx = 1;
            break;
    }
    showSlides(slideIndex[idx] += n, id, idx);
}

function showSlides(n, id, idx) {
    var i;
    var slides = document.getElementsByClassName(id + "-slide");
    if (n > slides.length) {slideIndex[idx] = 1}    
    if (n < 1) {slideIndex[idx] = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";  
    }
    slides[slideIndex[idx]-1].style.display = "block";  
}

function imageSlider() {
    plusSlides(1, 'brotherhood');
    plusSlides(1, 'service');
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
        if ($(this).text() == 'family') {
            $('#hero').css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4) ), url(./assets/imgs/hero.jpg)');
            $(this).text('fraternity');
        } else {
            $('#hero').css('background-image', 'linear-gradient( rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4) ), url(./assets/imgs/hero_family.jpg)');
            $(this).text('family');
        }
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
    imageSlider();
})

particlesJS.load('particles', '/assets/js/particles.json', function() {
  console.log('callback - particles.js config loaded');
});
