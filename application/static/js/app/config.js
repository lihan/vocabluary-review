// Set the require.js configuration for your application.
require.config({
  baseUrl: "/static/js",
  deps: ["app/main"],
  paths: {
    "jquery": "libs/jquery-2.0.0",
    "backbone": "libs/backbone",
    "underscore": "libs/underscore"

  },
  map: {

  },
  shim: {
    'backbone': {
        deps: ['underscore', 'jquery'],
        //Once loaded, use the global 'Backbone' as the
        //module value.
        exports: 'Backbone'
    },
    'underscore': {
        exports: '_'
    }
  }

});
