/**
 * Created with PyCharm.
 * User: lihanli
 * Date: 24/05/13
 * Time: 11:59 PM
 * To change this template use File | Settings | File Templates.
 */
define(
    ['backbone', 'underscore', 'app/models', 'app/collections'],

function(Backbone, _, Models, Collections) {

    var header = new Models.Header();
    var BookmarkedWord = Models.BookmarkedWord;




    var HeaderView = Backbone.View.extend({
        template: _.template($('.tmpl-header').html()),
        initialize: function() {
           this.model.on("change:title", this.render, this);
        },
        render: function() {
            this.$el.html(this.template(this.model.attributes));
            return this;
        }
    });

    var FooterView = Backbone.View.extend({
        template: _.template($('.tmpl-footer').html()),
        render: function() {
            this.$el.html(this.template({}));
            return this;
        }
    });


    var WordListView = Backbone.View.extend({
        el: '.js-main-view',
        template: _.template($('.tmpl-word-list').html()),
        events: {
            'click li': 'wordClickedHandler'
        },
        initialize: function(wordListCollection) {
            this.wordListCollection = wordListCollection;
            // todo: We definitely don't want to do this render it after it all fetched
            this.wordListCollection.on('add', this.render, this);
            this.wordListCollection.fetch();
        },
        wordClickedHandler: function(ev) {
            var wordId = $(ev.target).data('id');

            var bookmark = new BookmarkedWord({
                'word': {
                    'id': wordId
                }
            });
            bookmark.save();
        },
        render: function() {
            var self = this;
            this.$el.html(this.template({
                wordList: self.wordListCollection.toJSON()
            }));
            return this;
        }
    });

    var WordListIndexView = Backbone.View.extend({
        el: '.js-main-view',
        template: _.template($('.tmpl-word-index').html()),
        collection: null,
        events: {
            'click li': 'itemClickedHandler'
        },
        initialize: function() {
            // todo: We definitely don't want to do this
            // render it after it all fetched
            this.render();
            this.collection.on('add', this.render, this);
            this.collection.fetch();

        },
        itemClickedHandler: function(e) {
            // todo: circular dependency, fix!!!
            var App = require('app/app');
            var clickedId = $(e.target).data('list-id');
            App.router.navigate('list/' + clickedId, {trigger: true});
        },
        render: function() {
            var self = this;
            this.$el.html(this.template({
                indexes: self.collection.toJSON()
            }));
            return this;
        }
    });

    var BookmarkItemView = Backbone.View.extend({
        tagName: 'li',
        template: _.template($('.tmpl-bookmark-item-view').html()),
        events: {
            'click': 'deleteItem'
        },
        initialize: function() {

            this.render();
            _.bindAll(this, 'showDeleteItem');
            this.model.on('destroy', this.showDeleteItem);
        },
        showDeleteItem: function() {
            this.$el.slideUp();
        },
        deleteItem: function(ev) {
            this.model.destroy();
        },
        render: function() {
            this.$el.html(
            this.template({
                id: this.model.toJSON().id,
                word: this.model.get('word').get('word')
            }));
            return this;
        }
    });

    var BookmarkListView = Backbone.View.extend({
        el: $('.js-main-view'),
        template: _.template($('.tmpl-bookmark-view').html()),
        initialize: function() {
            this.render();
            this.bookmarkedWordCollection = new Collections.BookmarkedWordCollection();
            this.bookmarkedWordCollection
            this.bookmarkedWordCollection.fetch();
            this.renderCollection();
            this.listenTo(this.bookmarkedWordCollection, 'add', this.addItem);
        },
        render: function() {
            this.$el.html(this.template({}));
            return this;
        },
        renderCollection: function() {

            var i = 0,
                j = this.bookmarkedWordCollection.length;

            for (; i < j; i++) {
                var instance = this.bookmarkedWordCollection.models[i];
                this.addItem(instance);
            }
        },
        addItem: function(instance) {
            var $el = $(this.el);

            if (this.bookmarkedWordCollection.indexOf(instance) != -1) {
                view = new BookmarkItemView({
                    model: instance
                });
                $el.find('.js-word-list').append(view.$el);
            }
        }
    });

    var AppView = Backbone.View.extend({
        el: $('.js-app'),
        initialize: function() {
            _.bindAll(this, 'renderSubViews');
            this.renderSubViews();
        },
        renderSubViews: function() {
            new HeaderView({el: $('.js-top-bar'), model: header}).render();
            new FooterView({el: $('.js-footer-menu')}).render();
        }

    });

    return {
        'AppView': AppView,
        'WordListView': WordListView,
        'WordListIndexView': WordListIndexView,
        'BookmarkListView': BookmarkListView
    }
});