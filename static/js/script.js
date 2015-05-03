var app = angular.module('app', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('AtopieCtrl', ['$scope', function AtopieCtrl($scope) {
    $scope.ohai = '^-^';
}]);
