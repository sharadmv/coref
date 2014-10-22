qb.controller('AnnotationController', ['$scope', 'Question', function($scope, Question) {

    $scope.annotate = function(result) {
        Question.annotate({
            id: $scope.question.id,
            phrases: $scope.question.phrases,
            result: result
        })
    }

    Question.fetch(function(result) {
        $scope.question = result;
        $scope.question_parts = [];
        $scope.phrase_text = [];

        var index = 0;
        for (var i = 0; i < result.phrases.length; i++) {
            var phrase = result.phrases[i];
            var beforeText = $scope.question.text.slice(index, phrase[0]);
            var phraseText = $scope.question.text.slice(phrase[0], phrase[1]);
            $scope.phrase_text.push(phraseText);
            $scope.question_parts.push({
                highlight: false,
                type: 'raw',
                text: beforeText
            });
            $scope.question_parts.push({
                highlight: true,
                type: 'highlight',
                text: phraseText
            });
            index = phrase[1];
        }
        var afterText = $scope.question.text.slice(index);
        $scope.question_parts.push({
            type: 'raw',
            text: afterText
        });
    });
}])
qb.controller('QuestionViewController', function($scope) {
});

qb.controller('AnnotationBoxController', function($scope) {
});
