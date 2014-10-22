qb.factory('Question', ['$resource', function($resource) {
    return $resource('/api/question/:id', {}, {
        fetch: {
            method: 'GET',
            url: '/api/fetch'
        },
        annotate: {
            method: 'POST',
            url: '/api/annotate'
        }
    })
}]);
