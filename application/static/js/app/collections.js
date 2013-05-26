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
            // todo: I believe this is joke
            // fix the ugly string concatenation
            return window.location.protocol + "//" + window.location.host + '/api/v1/word_index/';
        }
    });

    var WordListCollection = Backbone.Collection.extend({
        model: Models.Word,
        initialize: function(wordListId) {
            this.id = wordListId;
        },
        url: function() {
            // todo: I believe this is joke
            return window.location.protocol + "//" + window.location.host + '/api/v1/word_list/' + this.id;
        }
    });

    return {
        'WordIndexCollection': WordIndexCollection,
        'WordListCollection': WordListCollection
    }

});