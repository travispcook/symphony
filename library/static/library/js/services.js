'use strict';

angular.module("MusicLibrary")

.service('Library', ['Restangular', function (Restangular) {
    var library = this;
    this.Pieces = Restangular.all('piece');
    this.ScoreTypes = Restangular.all('scoretype');
    this.Containers = Restangular.all('container');
    this.Orchestras = Restangular.all('orchestra');
    this.Performances = Restangular.all('performance');

    //this.pieces = this.Pieces.getList();
    //this.scoretypes = this.ScoreTypes.getList();
    //this.containers = this.Containers.getList();
    //this.orchestras = this.Orchestras.getList();
    //this.performances = this.Performances.getList();

}]);
