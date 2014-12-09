qb.controller('AnnotationController', ['$scope', 'Question', function($scope, Question) {

    $scope.annotate = function(result) {
        Question.annotate({
            question_id: $scope.question.question_id,
            mention_pair_id: $scope.mentionPairs[$scope.currentPair].mention_pair_id,
            result: result
        }, function(){
          if ($scope.currentPair < $scope.mentionPairs.length - 1) {
            $scope.currentPair++;
            $scope.loadPair();
          } else {
            $scope.fetch();
          }
        });
    }

    $scope.fetch = function() {
      Question.fetch(function(result) {
          $scope.data = result;
          $scope.question = $scope.data.question;
          $scope.mentionPairs = $scope.data.mention_pairs;

          $scope.currentPair = 0;
          $scope.loadPair();
      }, function() {
      });
    }

    $scope.loadPair = function() {
      $scope.question_parts = [];
      $scope.phrase_text = [];

      if ($scope.mentionPairs.length == 0) {
        $scope.noQuestions = true;
        return;
      }

      var index = 0;
      var curPair = $scope.mentionPairs[$scope.currentPair];

      var mentions = [curPair.mention1, curPair.mention2].sort(function(m) {
        return -m.pos_start;
      })


      for (var i = 0; i < mentions.length; i++) {
          var phrase = mentions[i];
          var beforeText = $scope.question.text.slice(index, phrase.pos_start);
          var phraseText = $scope.question.text.slice(phrase.pos_start, phrase.pos_end);
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
          index = phrase.pos_end;
      }
      var afterText = $scope.question.text.slice(index);
      $scope.question_parts.push({
          type: 'raw',
          text: afterText
      });
    }

    $scope.fetch($scope.loadPair);
}])

qb.controller('QuestionViewController', function($scope) {
});

qb.controller('AnnotationBoxController', function($scope) {
});

qb.controller('LoginController', ['$scope', '$window', '$modal', '$http', function($scope, $window, $modal, $http) {
    $scope.loggedIn = $window.config.loggedIn;
    $scope.user = $window.config.user;
    $scope.action = function() {
        if ($scope.loggedIn) {
            $scope.logout();
        } else {
            $scope.login();
        }
    }
    $scope.open = function() {
        var modal = $modal.open({
          templateUrl: '/static/partials/login-modal.html',
          controller: 'LoginModalController',
          size: 'md',
        });
      };

    $scope.login = function() {
        $scope.open()
    }
    $scope.logout = function() {
        $http.post('/api/logout').success(function(data) {
            if (data.status == 200) {
                $scope.setUser(null);
            } else {
            }
        })
    }

    $scope.setUser = function(user) {
        $scope.user = user;
        if (user === null) {
            $scope.loggedIn = false;
        }
        if (user !== null) {
            $scope.loggedIn = true;
        }
    }

}]);

qb.controller('LoginModalController', ['$scope', '$http', function($scope, $http) {
    $scope.showLoginError = false;
    $scope.showRegisterError = false;

    $scope.loginInfo = {
    }
    $scope.registerInfo = {
    }

    $scope.login = function() {
        $http.post('/api/login', $scope.loginInfo).success(function(data) {
            if (data.status == 200) {
                $scope.setUser(data.data);
                $scope.$close();
            } else {
                $scope.showLoginError = true;
            }
        })
    }
    $scope.register = function() {
        $http.post('/api/register', $scope.registerInfo).success(function(data) {
            if (data.status == 200) {
                $scope.setUser(data.data);
                $scope.$close();
            } else {
                $scope.showRegisterError = true;
                $scope.registerMessage = data.message;
            }
        })
    }

    $scope.showLogin = true;

    $scope.openLogin = function() {
        $scope.showLogin = true;
    }
    $scope.openRegister = function() {
        $scope.showLogin = false;
    }
}]);
