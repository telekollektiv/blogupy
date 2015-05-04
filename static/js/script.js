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

app.controller('CatchAllCtrl', ['$routeParams', '$scope', function($routeParams, $scope) {
    $scope.templatePath = $routeParams.template + '?ng';
}]);
