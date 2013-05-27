require([
  "app/app",
  "app/router"
],
function(app, Router) {
    app.router = new Router();
    Backbone.history.start({ pushate: false, root: app.root });
});
