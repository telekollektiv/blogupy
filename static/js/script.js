var app = angular.module('app', ['ngRoute', 'angular-loading-bar']);

var breakouts = [
    'feed'
];

var random = function(len) {
    var ret = '';


    while(ret.length < len) {
        ret += Math.random().toString(36).replace(/[^a-z]/ig, '');
    }

    return ret.substr(0, len);
};

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol(random(128));
    $interpolateProvider.endSymbol(random(128));
}]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider
        .when('/', {
            templateUrl: '/?ng'
        })
        .when('/contribute/', {
            templateUrl: '/contribute/?ng',
            controller: 'ContributeCtrl'
        })
        .when('/contribute/events', {
            templateUrl: '/contribute/events?ng',
            controller: 'EventContributeCtrl'
        })
        .when('/:template*', {
            template: '<ng-include src="templatePath"></ng-include>',
            controller: 'CatchAllCtrl'
        })
}]);

app.controller('AtopieCtrl', ['$rootScope', '$scope', function($rootScope, $scope) {
}]);

app.controller('ContributeCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.data = {};

    $scope.submit = function($e) {
        $e.preventDefault();

        $scope.data.csrf_token = $('#csrf_token').val();

        $http({
            method: 'POST',
            url: '/contribute/?ng',
            data: $.param($scope.data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function() {
            $location.path('/contribute/done');
        }).error(function() {
            console.log('oh noes');
        });
    };
}]);

app.controller('EventContributeCtrl', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.data = {};

    $scope.submit = function($e) {
        $e.preventDefault();

        $scope.data.csrf_token = $('#csrf_token').val();

        $http({
            method: 'POST',
            url: '/contribute/events?ng',
            data: $.param($scope.data),
            headers: {'Content-Type': 'application/x-www-form-urlencoded'}
        }).success(function() {
            $location.path('/contribute/done');
        }).error(function() {
            console.log('oh noes');
        });
    };
}]);

app.controller('CatchAllCtrl', ['$routeParams', '$scope', function($routeParams, $scope) {
    var route = $routeParams.template;

    if(~breakouts.indexOf(route)) {
        location.reload();
    } else {
        $scope.templatePath = route + '?ng';
    }
}]);
