var qb = angular.module('qb', ['ngResource']);

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
