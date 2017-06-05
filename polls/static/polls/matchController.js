var app = angular.module('footsi');

app.controller("matchController", function ($http, $location, $scope, sharedObject) {



    $scope.hostTeams = sharedObject.getObject().clubslist;
    $scope.guestTeams = sharedObject.getObject().clubslist;

    $scope.currentHostSelected = '';
    $scope.currentGuestSelected = '';


    $scope.selectThisHost = function (selectedId) {
        $scope.currentHostSelected = selectedId;
        $scope.activePlayButton = $scope.currentGuestSelected != '' && $scope.currentHostSelected != ''  ;

    }

    $scope.selectThisGuest = function (selectedId) {
        $scope.currentGuestSelected = selectedId;
        $scope.activePlayButton = $scope.currentGuestSelected != '' && $scope.currentHostSelected != ''  ;

    }

    $scope.goBack = function () {
        $location.path("/");

    }


    $scope.playMatch = function () {

        if ($scope.currentGuestSelected == $scope.currentHostSelected){
            console.log("the same team!!!");
            return;
        }

        if ($scope.currentGuestSelected == '' || $scope.currentHostSelected == ''){
            console.log("select two team!!!");
            return;
        }

        console.log("two team will be :");
        console.log("host " + $scope.currentHostSelected);
        console.log("guest " + $scope.currentGuestSelected);

        $http({
            url: "playmatch/",
            method: "GET",
            params: {hostKey : $scope.currentHostSelected,
                    guestKey : $scope.currentGuestSelected}
        }).then(function (response) {

            if (response.status !== 200) {

                alert('Something baaad happend');
                return;
            }

            console.log("the result of game is :");
            console.log(response.data);
            $location.path("/");
        });
    }
});

