define([
    'jquery',
    'app/models',
    'app/collections',
    'app/views'
],
function($, Models, Collections, Views) {

    var WordIndexCollection = new Collections.WordIndexCollection(),
        contentViews = null;

    return {
        initialize: function() {
            new Views.AppView();
        },
        showIndex: function() {
            contentViews = new Views.WordListIndexView({collection: WordIndexCollection});
        },
        showList: function(listId) {
            var wordListCollection = new Collections.WordListCollection(listId),
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
