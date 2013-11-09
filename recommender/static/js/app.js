window.app = angular.module('app', []);

app.directive('eRating', function() {
    return {
        restrict: 'A', // attribute
        templateUrl: '/static/templates/rating.html',
        scope: {
            eRating: '=', // optionally represents a max rating (default=5)
            ratingValue: '=', // current rating (default=0)
            readOnly: '@', // if a rating shouldn't be editable
            onRatingChange: '&' // a callback for reacting to a rating change
        },
        link: function (scope, elem, attrs) {
            // debug

            //console.log("rating", scope.eRating, scope.ratingValue, scope.readOnly, scope.onRatingSelected);
            //console.log('attrs', attrs.ratingValue);

            // reactors

            function setStars() {
                // stars are bound to the template list item
                scope.stars = [];
                for (var i = 1; i < scope.eRating+1; i++) {
                    scope.stars.push({empty: (i > scope.tempValue)});
                }
            }

            // event methods

            scope.toggle = function(index) {
                if (scope.readonly && scope.readonly === "true") {
                    return;
                }
                scope.ratingValue = index + 1;
                scope.tempValue = scope.ratingValue;
                setStars();
                scope.onRatingChange({newRating: index + 1});
            };

            scope.hover = function(index) {
                scope.tempValue = index + 1;
                setStars();
            };

            scope.resetHover = function() {
                scope.tempValue = scope.ratingValue;
                setStars();
            };

            // defaults

            scope.eRating = scope.eRating || 5;
            scope.ratingValue = (attrs.ratingValue === 'None') ? 0 : attrs.ratingValue;
            scope.tempValue = scope.ratingValue;

            setStars();

        }
    };
});

app.factory("api", function($http, $resource, settings) {
    delete $http.defaults.headers.common['X-Requested-With'];
    var api = $resource("/api/v1/:type/:id",
                        {
                            type: '@type',
                            api_key: function() {localStorage.getItem('api_key');},
                            id: '@id'
                        },
                        {
                            create: {method: 'POST', headers: {'Content-Type': 'application/json'}},
                            update: {method: 'PUT', headers: {'Content-Type': 'application/json'}},
                            delete: {method: 'DELETE', headers: {'Content-Type': 'application/json'}}
                        });

    return api;
});

// runs before startup, doesn't have a fully bootstrapped environment
app.config(function() {});

// same as jQuery(window).ready(function(){});
// or $(window).ready(function(){});
// or $(function(){});
app.run(function() {
    return console.log('Array(16).join("lol" - 2) + " Batman!";');
});

app.controller('AppCtrl', function($scope, $location) {
    $scope.saveVotes = function() {
        // TODO
    };
});
