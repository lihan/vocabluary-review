/**
 * Created with PyCharm.
 * User: lihanli
 * Date: 24/05/13
 * Time: 11:59 PM
 * To change this template use File | Settings | File Templates.
 */
define(
    ['backbone', 'underscore', 'app/models'],

function(Backbone, _, Models) {

    var header = new Models.Header();

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
        initialize: function(wordListCollection) {
            this.wordListCollection = wordListCollection;
            // todo: We definitely don't want to do this
            // render it after it all fetched
            this.wordListCollection.on('add', this.render, this);
            this.wordListCollection.fetch();
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
            this.collection.on('add', this.render, this);
            this.collection.fetch();
        },
        itemClickedHandler: function(e) {
            console.log('click');
            debugger;
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

    var AppView = Backbone.View.extend({
        el: $('.js-app'),
        initialize: function(indexCollection) {
            this.contentViews = [];
            _.bindAll(this, 'unbindContentView');
            _.bindAll(this, 'renderSubViews');
            this.indexCollection = indexCollection;
            this.renderSubViews();

        },
        renderSubViews: function() {
            new HeaderView({el: $('.js-top-bar'), model: header}).render();
            this.contentViews.push(new WordListIndexView({collection: this.indexCollection}).render());
            new FooterView({el: $('.js-footer-menu')}).render();
        },
        unbindContentView: function() {
            $.each(this.contentViews, function(i, view) {
                $(view.el).off();
            });
        }
    });

    return {
        'AppView': AppView,
        'WordListView': WordListView
    }
});