window.app = angular.module('app', ['ratings', 'ngResource']);

app.factory("api", function($http, $resource) {
    delete $http.defaults.headers.common['X-Requested-With'];
    var api = $resource("/api/v1/:type/:id",
                        {
                            type: '@type',
                            api_key: function() {localStorage.getItem('api_key');},
                            id: '@id'
                        },
                        {
                            create: {method: 'POST', headers: {'Content-Type': 'application/json'}},
                            replace: {method: 'PUT', headers: {'Content-Type': 'application/json'}},
                            update: {method: 'PATCH', headers: {'Content-Type': 'application/json'}},
                            delete: {method: 'DELETE', headers: {'Content-Type': 'application/json'}}
                        });

    return api;
});

// runs before startup, doesn't have a fully bootstrapped environment
app.config(function() {});

// similar to jQuery(window).ready(function(){});
// or $(window).ready(function(){});
// or $(function(){});
app.run(function() {
    return console.log('Array(16).join("lol" - 2) + " Batman!";');
});

app.controller('AppCtrl', function() {});
