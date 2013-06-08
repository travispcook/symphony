'use strict';

app.controller("PieceList", function ($scope, Pieces) {
    $scope.$watch(function () { return Pieces.piece; },
        function (pieces) { $scope.pieces = pieces; }, true);
});