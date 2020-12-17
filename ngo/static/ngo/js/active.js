(function ($) {
    'use strict';

    var browserWindow = $(window);

    // :: 1.0 Preloader Active Code
    browserWindow.on('load', function () {
        $('.preloader').fadeOut('slow', function () {
            $(this).remove();
        });
        var hashcode = window.location.hash;
        if (hashcode != ""){
            $('html,body').animate({scrollTop: $(hashcode).position().top-51},'slow');
        }
    });

    // :: 2.0 Nav Active Code
    if ($.fn.classyNav) {
        $('#croseNav').classyNav();
    }

    // :: 3.0 Search Active Code
    $('#header-search').on('click', function () {
        $('.search-form-area').toggleClass('search-on');
    });
    $('#searchCloseIcon').on('click', function () {
        $('.search-form-area').removeClass('search-on');
    });

    // :: 4.0 Sliders Active Code
    if ($.fn.owlCarousel) {
        var welcomeSlide = $('.hero-post-slides');
        var upcomingSlides = $('.upcoming-slides');

        welcomeSlide.owlCarousel({
            items: 1,
            margin: 0,
            loop: true,
            nav: false,
            dots: false,
            autoplay: true,
            center: true,
            autoplayTimeout: 7000,
            smartSpeed: 1000
        });

        welcomeSlide.on('translate.owl.carousel', function () {
            var slideLayer = $("[data-animation]");
            slideLayer.each(function () {
                var anim_name = $(this).data('animation');
                $(this).removeClass('animated ' + anim_name).css('opacity', '0');
            });
        });

        welcomeSlide.on('translated.owl.carousel', function () {
            var slideLayer = welcomeSlide.find('.owl-item.active').find("[data-animation]");
            slideLayer.each(function () {
                var anim_name = $(this).data('animation');
                $(this).addClass('animated ' + anim_name).css('opacity', '1');
            });
        });

        $("[data-delay]").each(function () {
            var anim_del = $(this).data('delay');
            $(this).css('animation-delay', anim_del);
        });

        $("[data-duration]").each(function () {
            var anim_dur = $(this).data('duration');
            $(this).css('animation-duration', anim_dur);
        });

        upcomingSlides.owlCarousel({
            items: 1,
            margin: 0,
            loop: true,
            nav: true,
            navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
            dots: false,
            autoplay: true,
            autoplayTimeout: 7000,
            smartSpeed: 1500
        });
    }
    
    // :: 5.0 magnificPopup Active Code
    if ($.fn.magnificPopup) {
        $('.gallery-img').magnificPopup({
            gallery: {
                enabled: true
            },
            type: 'image'
        });
        //CUSTOM FOR VIDEOS
        var embed = $('#video-clip').attr('data-embed');
        $('#video-clip').magnificPopup({
            type: 'iframe',
            // other options
            iframe: {
            markup: '<div class="mfp-iframe-scaler">'+
                      '<div class="mfp-close"></div>'+ embed +
                    '</div>',
          
            patterns: {
              youtube: {
                index: 'youtube.com/', 
                src: 'https://www.youtube.com/embed/B-t6M6b2ToU'
              },
              vimeo: {
                index: 'vimeo.com/',
                id: '/',
                src: '//player.vimeo.com/video/%id%?autoplay=1'
              },
              gmaps: {
                index: '//maps.google.',
                src: '%id%&output=embed'
              }
            },
            srcAction: 'iframe_src',
          }
          });
          
    }
    
    // :: 6.0 ScrollUp Active Code
    if ($.fn.scrollUp) {
        browserWindow.scrollUp({
            scrollSpeed: 1500,
            scrollText: '<i class="fa fa-angle-up"></i>'
        });
    }

    // :: 7.0 Sticky Active Code
    if ($.fn.sticky) {
        $(".crose-main-menu").sticky({
            topSpacing: 0
        });
    }

    // :: 8.0 Tooltip Active Code
    if ($.fn.tooltip) {
        $('[data-toggle="tooltip"]').tooltip()
    }

    // :: 9.0 prevent default a click
    $('a[href="#"]').on('click', function ($) {
        $.preventDefault();
    });


    if ($('#toast')){
        $('#toast').each(function(){
            $(this).toast('show');
            $(this).addClass('slideInRight')
            $(this).removeClass('slideOutRight')
        })

        $('#toast').each(function(){
            $(this).on('shown.bs.toast', function () {
                var b = $(this)
            setTimeout( function(){
                console.log(b);
                b.addClass('slideOutRight');
                b.removeClass('slideInRight');
                setTimeout(function(){
                    b.toast('hide');
                }, 500)
            }, 6000);
        })
        })
        $('#toast .toast-body button').each(function(){
            $(this).click(function () {
                $(this).parent().parent().addClass('slideOutRight');
                $(this).parent().parent().removeClass('slideInRight');
                console.log('DONE');
                setTimeout(function(){
                    $(this).parent().toast('hide');
                }, 500)
        })
        })
    }

    if ($('.img-overlay')){
        $('.img-overlay').click(function(){
            $('#id_picture').click()
        });
        $('.img-overlay').hover(function(){
            $('#id_picture').addClass('bg-overlay')
        });
        $("#id_picture").change(function(){
          $('.picture-form').submit();
          $('.picture-form').submit(function(){
            alert("The Image has been changed.");
          })
        });
    }

    if ($('.md-textarea.textarea')){
        $('.md-textarea.textarea').on('focus', function (e) {
            $('.textarea-label').addClass('active');
             console.log("focused")
           })
           $('.md-textarea.textarea').on('blur', function (e) {
            $('.textarea-label').removeClass('active');
            if($('.textarea-label').attr('textContent') != ""){
             $('.textarea-label').addClass('active');
           }
             console.log("blurred")
           })
           if($('.textarea-label').attr('textContent') != ""){
             $('.textarea-label').addClass('active');
           }
    }

    if ($('[data-toggle="slide-collapse"]')){
        // mobile menu slide from the left 
        $('[data-toggle="slide-collapse"]').on('click', function() {
            $($(this).data('target')).css('transform','translateX(0rem)');
            
            $('.sidenav-overlay').css('display','block');
            // navMenuCont.animate({'transform':'toggle'}, "translateX(15rem)"); 
        });
        $('[data-dismiss="close"]').on('click', function() {
            $($(this).data('target')).css('transform','translateX(-15rem)');
            $('.sidenav-overlay').css('display','none');
            // $navMenuCont.animate({'transform':'toggle'}, "-15rem"); 
        });
        $('.dashboard-btn').click(function(){
            $('.dashboard-btn').css({"border":'0px'})
        })
        $('.sidenav-overlay').click(function(){
            $($(this).data('target')).css('transform','translateX(-15rem)');
            $('.sidenav-overlay').css('display','none');
        })
    }

    // :: 10.0 wow Active Code
    if (browserWindow.width() > 767) {
        new WOW().init();
    }
    
})(jQuery);