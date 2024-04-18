if (!window.dash_clientside) {window.dash_clientside = {};}
<<<<<<< HEAD

window.dash_clientside.clientside = {
    trigger_gsap_animation: function() {
        gsap.registerPlugin(ScrollTrigger);
        gsap.from("#m1", {scrollTrigger: {scrub: true}, y: 200});
        gsap.from("#m2", {scrollTrigger: {scrub: true}, y: 100});
        gsap.from("#t2", {scrollTrigger: {scrub: true}, x: -100});
        gsap.from("#t1", {scrollTrigger: {scrub: true}, x: 50});
        gsap.from("#man", {scrollTrigger: {scrub: true}, x: -200});
        gsap.from("#plants", {scrollTrigger: {scrub: true}, x: -100});
        
        return window.dash_clientside.no_update; // Important for preventing update loops
=======
 
window.dash_clientside.clientside = {
    trigger_gsap_animation: function() {
        gsap.registerPlugin(ScrollTrigger);
        gsap.from("#m1", {scrollTrigger: {scrub: true}, x: 200});
        gsap.from("#m2", {scrollTrigger: {scrub: true}, x: 100});
        gsap.from("#t2", {scrollTrigger: {scrub: true}, x: -100});
        gsap.from("#t1", {scrollTrigger: {scrub: true}, x: 100});
        gsap.from("#man", {scrollTrigger: {scrub: true}, x: -200});
        gsap.from("#plants", {scrollTrigger: {scrub: true}, x: -100});
        gsap.from("#right1", {scrollTrigger: {scrub: true}, x: -700});
        gsap.from("#left1", {scrollTrigger: {scrub: true}, x: 150});
        gsap.from("#right2", {scrollTrigger: {scrub: true}, x: -150});
        gsap.from("#left2", {scrollTrigger: {scrub: true}, x: 700});
        gsap.from("#alert", {
            scrollTrigger: {
                trigger: "#alert",
                start: "top bottom", // When the top of #line_c hits the bottom of the viewport
                end: "bottom top",
                scrub: true
            },
            x: -1050
        });
        gsap.from("#line_c", {
            scrollTrigger: {
                trigger: "#line_c",
                start: "top bottom", // When the top of #line_c hits the bottom of the viewport
                end: "bottom top",
                scrub: true
            },
            x: -150
        });
        gsap.from("#pie", {
            scrollTrigger: {
                trigger: "#pie",
                start: "top bottom", // When the top of #pie hits the bottom of the viewport
                end: "bottom top",
                scrub: true
            },
            x: 150
        });
       
        return window.dash_clientside.no_update; // Important for preventing update loops
    },
 
    scroll_to_map: function(selected_trail) {
        if(selected_trail) {
            setTimeout(function() {
                document.getElementById('mytrail-map').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 100); // A slight delay to ensure the DOM has updated
        }
        return window.dash_clientside.no_update; // Prevent updating any Output
    },

    scroll_to_text: function(n_clicks) {
        if(n_clicks > 0) {
            setTimeout(function() {
                document.getElementById('additional-content').scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }, 200); // A slight delay to ensure the DOM has updated
        }
        return ''; // Prevent updating any Output
>>>>>>> 5da007c (A brief description of the changes)
    }
}
