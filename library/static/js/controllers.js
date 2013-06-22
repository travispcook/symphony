'use strict';

app.controller("PieceList", function ($scope, Library) {
    $scope.pieces = Library.pieces;
});
