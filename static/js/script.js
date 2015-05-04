var app = angular.module('app', ['ngRoute', 'angular-loading-bar']);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.config(['$routeProvider', '$locationProvider', function($routeProvider, $locationProvider) {
    $locationProvider.html5Mode(true);
    $routeProvider
        .when('/', {
            templateUrl: '/?ng',
            controller: 'IndexCtrl',
            resolve: {
                articles: ['articleService', function(articleService) {
                    return articleService.get();
                }]
            }
        })
        .when('/contribute/', {
            templateUrl: '/contribute/?ng',
            controller: 'ContributeCtrl'
        })
        .when('/:template*', {
            template: '<ng-include src="templatePath"></ng-include>',
            controller: 'CatchAllCtrl'
        })
}]);

app.factory('articleService', ['$http', function($http) {
    return {
        get: function() {
            return $http.get('/index.json');
        }
    };
}]);

app.controller('AtopieCtrl', ['$rootScope', '$scope', function($rootScope, $scope) {
}]);

app.controller('IndexCtrl', ['$scope', '$sce', 'articles', function($scope, $sce, articles) {
    $scope.articles = articles.data.articles;
    $scope.articles.forEach(function(article) {
        article.html = $sce.trustAsHtml(article.html);
    });
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

app.controller('CatchAllCtrl', ['$routeParams', '$scope', function($routeParams, $scope) {
    $scope.templatePath = $routeParams.template + '?ng';
}]);
