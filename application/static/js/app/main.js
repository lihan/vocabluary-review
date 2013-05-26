require([
  "jquery",
  "app/app",
  "app/router"
],
function($, app, Router, Mobile) {
    app.router = new Router();
    Backbone.history.start({ pushate: false, root: app.root });
});
