/**
 * Created by yoadf on 6/10/2017.
 */
angular.module('nodeFeeds', [])
    .controller('mainController', ($scope, $http) => {
        $scope.formData = {};
        $scope.feedData = {};
        // Get all feeds
        $http.get('/feeds')
            .success((data) => {
                $scope.feedData = data;
                console.log(data);
            })
            .error((error) => {
                console.log('Error: ' + error);
            });
    });