var app = angular.module("footsi", ["ngRoute"]);

app.config(function ($routeProvider, $interpolateProvider) {


    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');

    $routeProvider
        .when("/", {
            title : 'Footsi',
            templateUrl : "../static/polls/Newclubs.htm",
            controller : "clubListController"
        })
        .when("/clubinfo", {
            templateUrl :  "../static/polls/Newclubinfo.htm",
            controller : "clubInfoController"
        })
        .when("/newmatch", {
            templateUrl :  "../static/polls/Newmatch.htm",
            controller : "matchController"
        });
});

app.factory('sharedObject', function () {

    var state = {};

    return {
        getObject: function () {
            return state;
        },
        setObject: function (newObject) {
            state = newObject;
        }
    };

});

app.controller("clubListController", function ($http, $location, $scope, sharedObject) {


    $scope.newMatch = function () {

        $http({
            url: "getteams/",
            method: "GET"
        }).then(function (response) {

            if(response.status !== 200) {

                alert('Something baaad happend');
                return;
            }

            sharedObject.setObject(response.data);
            $location.path("/newmatch")

            console.log(response.data);
        })
    }
    $scope.goToClub = function(clubKey) {

        console.log("club key : " + clubKey);
        $http({
            url: "getclubinfo/",
            method: "GET",
            params: {clubKey : clubKey}
        }).then(function (response) {
            if(response.status !== 200) {

                alert('Something baaad happend');
                return;
            }

            console.log(response.data);
            sharedObject.setObject(response.data);
            $location.path("/clubinfo");
        });

    }

    $http({
        url: "getteams/",
        method: "GET"
    }).then(function (response) {

        if(response.status !== 200) {

            alert('Something baaad happend');
            return;
        }

        $scope.clubs = response.data.clubslist;

        console.log($scope.clubs);
    })

});