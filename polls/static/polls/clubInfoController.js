var app = angular.module('footsi');

app.controller("clubInfoController", function ($http, $location, $scope, sharedObject) {




    $scope.clubMatchs = sharedObject.getObject().clubMatchs;
    $scope.stadiumInfo = sharedObject.getObject().stadiumInfo;
    $scope.clubInfo = sharedObject.getObject().clubInfo;

    console.log("response : " );
    console.log($scope.response);

    $scope.goBack = function () {
        $location.path("/");

    }
});

