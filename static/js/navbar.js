App.Navbar = {

    CLASS_NAVBAR: 'js-navbar',
    CLASS_TOGGLE: 'js-navbar--toggle',
    CLASS_OPEN: 'open',

    EVENT_NAME_OPEN: 'open',
    EVENT_NAME_CLOSE: 'close',

    registerEvents: function(){
        $('.' + this.CLASS_NAVBAR).on(this.EVENT_NAME_OPEN, function(event){
            // So far only adding CLASS_OPEN class.
            $(this).addClass(App.Navbar.CLASS_OPEN);

        }).on(this.EVENT_NAME_CLOSE, function(event){
            // So far only removing CLASS_OPEN class.
            $(this).removeClass(App.Navbar.CLASS_OPEN);

        });

        $('.' + this.CLASS_TOGGLE).on('click', function(event){
            var navbar = $(this).closest('.' + App.Navbar.CLASS_NAVBAR);
            var eventToTrigger = navbar.hasClass(App.Navbar.CLASS_OPEN) ?
                App.Navbar.EVENT_NAME_CLOSE :
                App.Navbar.EVENT_NAME_OPEN;

            navbar.trigger(eventToTrigger);
        })
    },
    init: function(){
        this.registerEvents();
    }
};

App.Navbar.init();
