define([
    'jquery',
    'app/models',
    'app/collections',
    'app/views'
],

function($, Models, Collections, Views) {


    var WordIndexCollection = new Collections.WordIndexCollection(),
        ViewCollection = {},
        contentViews = null;

    return {
        initialize: function() {
            var AppView = new Views.AppView();
            ViewCollection['AppView'] = AppView;
        },
        showIndex: function() {
            contentViews = new Views.WordListIndexView({collection: WordIndexCollection});
        },
        showList: function(listId) {
            var wordListCollection = new Collections.WordListCollection(listId);
            contentViews = new Views.WordListView(wordListCollection);
        },
        showBookmarkView: function() {

            contentViews = new Views.BookmarkListView();
        },
        unbindCurrentView: function() {
            if (contentViews) {
                $(contentViews.el).off();
            }

        }

    }
});
