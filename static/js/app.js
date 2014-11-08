var qb = angular.module('qb', ['ngResource', 'ui.bootstrap']);

qb.directive('questionViewer', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/partials/question-viewer.html',
    };
});

qb.directive('annotationBox', function() {
    return {
        restrict: 'E',
        templateUrl: '/static/partials/annotation-box.html',
    };
});

qb.directive('loginButton', function() {
    return {
        replace: true,
        restrict: 'E',
        controller: "LoginController",
        templateUrl: '/static/partials/login-button.html',
    };
});
