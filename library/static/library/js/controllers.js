'use strict';

angular.module("MusicLibrary")

.controller("PieceList", ['$scope', 'Library', function ($scope, Library) {
    Library.Pieces.options()
    .then(function (response) {
        $scope.difficultyChoices = response.actions.POST.difficulty.choices;
    });

    Library.ScoreTypes.getList()
    .then(function (scoretypes) {
        $scope.scoreTypes = {};
        for (var i in scoretypes) {
            var score = scoretypes[i];
            if (score && score.id) {
                $scope.scoreTypes[score.id] = score;
            }
        }
    });

    $scope.piece_rows = [];

    $scope.doSearch = function () {
        Library.Pieces.getList({search: $scope.search})
        .then(function (pieces) {
            var row, piece;
            $scope.piece_rows.length = 0;
            row = [];
            for (var i in pieces) {
                piece = pieces[i];
                if (piece && piece.id) {
                    row.push(piece);
                    if ((i + 1) % 3 == 0) {
                        $scope.piece_rows.push(row);
                        row = [];
                    }
                }
            }
            $scope.piece_rows.push(row);
        });
    };
}])
