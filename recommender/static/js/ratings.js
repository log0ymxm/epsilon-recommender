// https://raw.github.com/thomporter/angular-ratings/master/angular.ratings.js
// PE modified for use with our rating system

angular.module('ratings', []);

angular.module('ratings').directive("angularRatings", function() {
    return {
        restrict: 'E',
        scope: {
            rating: '@rating',
            notifyId: '=notifyId',
            csrf: '=csrf'
        },
        replace: true,
        //transclude: true,
        templateUrl: '/static/templates/rating.html',
        controller: function($scope, $attrs, $http) {
            $scope.over = 0;
            $scope.setRating = function(rating) {
                $scope.rating = rating;
                $scope.$apply();
                if ($attrs.notifyUrl !== void 0 && $scope.notifyId) {
                    var url = $attrs.notifyUrl + "/" + $scope.notifyId + "/" + rating;
                    return $http({
                        method: 'POST',
                        url: url,
                        headers: {
                            'X-CSRFToken': $attrs.csrf
                        }
                    }).error(function(data) {
			console.log(data);
                        return $scope.rating = 0;
                    }).success(function(data) {
			console.log(data);
			if (data === "Too many votes from this IP address for this object.") {
			    alert("Too many votes for this game!");
			    $scope.rating = 0;
			}
			    
		    });
                }
            };
            return $scope.setOver = function(n) {
                $scope.over = n;
                return $scope.$apply();
            };
        },
        link: function(scope, iElem, iAttrs) {
            if (iAttrs.rating === 'None') iAttrs.rating = 0;
            scope.rating = parseInt(iAttrs.rating);
            if (iAttrs.notifyUrl !== void 0) {
                return angular.forEach(iElem.children(), function(star) {
                    star.addEventListener('mouseover', function() {
                        return scope.setOver(parseInt(star.title));
                    });
                    star.addEventListener('mouseout', function() {
                        return scope.setOver(0);
                    });
                    return star.addEventListener('click', function() {
                        return scope.setRating(parseInt(star.title));
                    });
                });
            }
        }
    };
});
