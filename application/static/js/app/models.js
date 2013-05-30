define(
    ['backbone'],

function(Backbone) {

    // UI models
    var Header = Backbone.Model.extend({
        defaults: {
            title: "Beat IELTS vocabulary"
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

    var BookmarkedWord = Backbone.Model.extend({
        urlRoot: '/api/v1/bookmarks/',
        defaults: {
            'word': {
                "word"      :  "None",
                "meaning"   :  "None"
            }
        },
        model: {
            word: Word
        },
        parse: function(response){
            for(var key in this.model) {
                var embeddedClass = this.model[key];
                var embeddedData = response[key];
                response[key] = new embeddedClass(embeddedData, {parse: true});
            }
            return response;
        }
    });
    window.BookmarkedWord = BookmarkedWord;
    return {
        'Word': Word,
        'WordIndex': WordIndex,
        'Header': Header,
        'BookmarkedWord': BookmarkedWord
    };
});