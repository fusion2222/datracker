var Navbar = {

    CLASS_NAVBAR: 'js-navbar',
    CLASS_TOGGLE: 'js-navbar--toggle',
    CLASS_OPEN: 'open',

    EVENT_NAME_OPEN: 'open',
    EVENT_NAME_CLOSE: 'close',

    registerEvents: function(){
        $('.' + this.CLASS_NAVBAR).on(this.EVENT_NAME_OPEN, function(event){
            // So far only adding CLASS_OPEN class.
            $(this).addClass(Navbar.CLASS_OPEN);

        }).on(this.EVENT_NAME_CLOSE, function(event){
            // So far only removing CLASS_OPEN class.
            $(this).removeClass(Navbar.CLASS_OPEN);

        });

        $('.' + this.CLASS_TOGGLE).on('click', function(event){
            var navbar = $(this).closest('.' + Navbar.CLASS_NAVBAR);
            var eventToTrigger = navbar.hasClass(Navbar.CLASS_OPEN) ?
                Navbar.EVENT_NAME_CLOSE :
                Navbar.EVENT_NAME_OPEN;

            navbar.trigger(eventToTrigger);
        })
    },
    init: function(){
        this.registerEvents();
    }
};

Navbar.init();
