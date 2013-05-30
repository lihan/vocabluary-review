/**
 * Created with PyCharm.
 * User: lihanli
 * Date: 24/05/13
 * Time: 11:59 PM
 * To change this template use File | Settings | File Templates.
 */
define(
    ['backbone', 'app/models'],

function(Backbone, Models) {



    var WordIndexCollection = Backbone.Collection.extend({
        model: Models.WordIndex,
        url: function() {
            return '/api/v1/word_index/';
        }
    });

    var WordListCollection = Backbone.Collection.extend({
        model: Models.Word,
        initialize: function(wordListId) {
            this.id = wordListId;
        },
        url: function() {
            return '/api/v1/word_list/' + this.id;
        }
    });

    var BookmarkedWordCollection = Backbone.Collection.extend({
        model: Models.BookmarkedWord,
        url: '/api/v1/bookmarks/'
    });
    window.BookmarkedWordCollection = BookmarkedWordCollection

    return {
        'WordIndexCollection': WordIndexCollection,
        'WordListCollection': WordListCollection,
        'BookmarkedWordCollection': BookmarkedWordCollection
    }

});