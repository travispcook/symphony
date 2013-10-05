'use strict';

angular.module("MusicLibrary")

.controller("PieceList", ['$scope', 'Library', function ($scope, Library) {
    $scope.pieces = Library.pieces;
}])
