define([
    'jquery',
    'app/models',
    'app/collections',
    'app/views'
],

function($, Models, Collections, Views) {

    var WordIndexCollection = new Collections.WordIndexCollection(),
        ViewCollection = {};

    return {
        initialize: function() {
            var AppView = new Views.AppView(WordIndexCollection);
            ViewCollection['AppView'] = AppView;
        },
        showList: function(listId) {
            var wordListCollection = new Collections.WordListCollection(listId);
            new Views.WordListView(wordListCollection);
        },
        unbindCurrentView: function() {
            ViewCollection.AppView.unbindContentView();
        }
    }
});
