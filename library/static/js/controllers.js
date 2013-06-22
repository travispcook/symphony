'use strict';

app.controller("PieceList", function ($scope, Pieces) {
    $scope.pieces = Pieces.items;
});
