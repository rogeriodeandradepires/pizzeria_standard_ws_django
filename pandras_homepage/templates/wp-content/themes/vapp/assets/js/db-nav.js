/*!
 * DB Nav Responsive Dropdown Navigation Menu
 * (c) 2018 Faridul Haque | Team Dhrubok
 */
;
(function($, window, document, undefined) {


    $.navigation = function(element, options) {
        $(document).ready(function() {
            checkWidth(true);

            $(window).resize(function() {
                checkWidth(false);
            });
        });

        var hoverShowEvents = "mouseenter focusin";
        var hoverHideEvents = "mouseleave focusout";


        function checkWidth(init) {
            // If browser resized, check width again
            if ($(window).width() <= 1025) {
                $(element).addClass('navigation__portrait');
                $(element).removeClass('navigation__landscape');
                $(".navigation-dropdown").css({
                    "display": "none"
                });
            } else {
                if (!init) {
                    $('html').removeClass('navigation__portrait');
                    $(".navigation-dropdown").css({
                        "display": "block"
                    });
                }
            }
            if ($(window).width() > 1025) {
                $(element).addClass('navigation__landscape');
                $(element).removeClass('navigation__portrait');
                $(element).removeClass('offcanvas__overlay');
                $('body').removeClass('scroll-prevent');
                $('.navigation-wrapper').removeClass('offcanvas__is-open');
            } else {
                if (!init) {
                    $(element).removeClass('navigation__landscape');
                }
            }
            // dropdown auto aligned
            if ($(window).width() <= 1280) {
                $('.navigation-dropdown .navigation-dropdown').addClass('algin-to-left');
            } else {
                $('.navigation-dropdown .navigation-dropdown').removeClass('algin-to-left');
            }

        }

        // Submenu
        $(element).find('.navigation-menu__link').on(hoverShowEvents, function() {
            $(element).find('.navigation-menu__link').parent().children(".nav-submenu").stop(true, true).delay(0).fadeIn(300);
        }).on(hoverHideEvents, function() {
            $(element).find('.navigation-menu__link').parent().children(".nav-submenu").stop(true, true).delay(0).fadeOut(300);

        });

        // offcanvas reveal
        $('.navigation__toggler').on('click', function() {

            $('.navigation-wrapper').addClass('offcanvas__is-open');
            $('.navigation').addClass('offcanvas__overlay');
            $('body').toggleClass('scroll-prevent');
        });
        // offcanvas remove class
        $('body, .offcanvas__close, .navigation-menu .menu-item:not(.menu-item-has-children)').on('click', function() {
            $('.navigation-wrapper').removeClass('offcanvas__is-open')
            $(element).removeClass('offcanvas__overlay');
            $('body').removeClass('scroll-prevent');
        });

        // offcanvas prevent from toggle
        $('.navigation__toggler').on('click', function(e) {
            e.stopPropagation();
        });

        $('body').on('click', '.navigation-wrapper', function(e) {
            e.stopPropagation();
        });

        // offcanvas menu dropdown and caret slide
        $('body').find('.navigation-menu__link').on('click', '.submenu-icon', function(e) {
            if ($(".navigation__portrait").length > 0) {
                e.stopPropagation();
                if ($(".navigation-dropdown").length > 0) {
                    $(this).parent('a').parent('.navigation-menu__item').children('.navigation-dropdown').slideToggle();
                    $(this).parent('a').toggleClass('highlight');
                    $(this).toggleClass('submenu-icon__caret--up');
                }
            }
        });

        // dropdown submenu icon append
        $(element).find("li").each(function() {
            if ($(this).children(".navigation-dropdown").length > 0) {
                // $(this).children(".navigation-dropdown").addClass("nav-submenu");
                $(this).children("a").append(
                    "<span class='submenu-icon'>" +
                    "<span class='submenu-icon__caret'></span>" +
                    "</span>"
                );
            }
        });
        $('body').on('click', '.submenu-icon', function(e) {
            e.stopPropagation();
        });

        // sticky nav
        $(window).on('scroll', function() {
            if ($(window).scrollTop() > 50) {
                if( $('body').hasClass('use-sticky-nav') ) {
                    $(element).addClass('sticky-nav');
                }
            } else {
                $(element).removeClass('sticky-nav');
            }
        });

    };


    $.fn.navigation = function(options) {
        return this.each(function() {
            if (undefined === $(this).data("navigation")) {
                var plugin = new $.navigation(this, options);
                $(this).data("navigation", plugin);
            }
        });
    };

    // Select all links with hashes
    $('a[href*="#"]')
      // Remove links that don't actually link to anything
      .not('[href="#"]')
      .not('[href="#0"]')
      .click(function(event) {
        // On-page links
        if (
          location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '')
          &&
          location.hostname == this.hostname
        ) {
          // Figure out element to scroll to
          var target = $(this.hash);
          target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
          // Does a scroll target exist?
          if (target.length) {
            // Only prevent default if animation is actually gonna happen
            event.preventDefault();
            $('html, body').animate({
              scrollTop: target.offset().top
          }, 500, function() {
              // Callback after animation
              // Must change focus!
              var $target = $(target);
              $target.focus();
              if ($target.is(":focus")) { // Checking if the target was focused
                return false;
              } else {
                $target.attr('tabindex','-1'); // Adding tabindex for elements not focusable
                $target.focus(); // Set focus again
              };
            });
          }
        }
      });


    // nav init
    $(document).ready(function() {
        $(".navigation.site-nav").navigation();
    });

})(jQuery, window, document);
