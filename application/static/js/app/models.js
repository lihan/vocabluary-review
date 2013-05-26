define(
    ['backbone'],

function(Backbone) {

    // UI models

    var Header = Backbone.Model.extend({
        defaults: {
            title: "Select Learning module"
        }
    });

    // Server model
    var Word = Backbone.Model.extend({
        defaults: {
            "word"      :  "None",
            "meaning"   :  "None"
          }
    });

    var WordIndex = Backbone.Model.extend({});

    return {
        'Word': Word,
        'WordIndex': WordIndex,
        'Header': Header
    };
});