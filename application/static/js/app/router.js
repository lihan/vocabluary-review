define([
    // Application.
    "app/app",
    "backbone"

],
    function (App, Backbone) {
        App.initialize();

        return Backbone.Router.extend({
            routes: {
                "": 'init',
                "list/:id": "wordList"
            },
            init: function() {
                App.initialize();
            },
            wordList: function(id) {
                App.unbindCurrentView();
                App.showList(id);
            }
        });
    });

