'use strict';

angular.module("MusicLibrary")

.factory('RestCommon', ['Restangular', function (Restangular) {

    return function(resource){
        var service = {};
        service.rest = Restangular.all(resource);
        service[resource] = [];

        service.read = function () {
            var promise =  this.rest.getList();
            promise.then(function (response) {
                service[resource].length = 0
                service[resource].push.apply(service[resource], response);
                if ('metadata' in response) {
                    service[resource].metadata = response.metadata;
                }
            });
            return promise;
        };

        service.post = function (data) {
            var promise = this.rest.post(data);
            return promise.then(function (newItem) {
                service[resource].push(newItem);
                return newItem;
            });
        };

        service.put = function (item, data) {
            $.extend(item, data);
            return item.put();
        };

        service.delete = function (item) {
            var resource = this[resource];
            for (var i = 0; i < resource.length; i++) {
                if (resource[i] == item) {
                    var promise = item.remove();
                    resource.splice(i, 1);
                    return promise
                }
            }
        };

        return service;
    };
}])

.service('Library', ['RestCommon', function (RestCommon) {
    var library = this;
    this.Artists = RestCommon('artist');
    this.Pieces = RestCommon('piece');
    this.ScoreTypes = RestCommon('scoretype');
    this.Containers = RestCommon('container');
    this.Orchestras = RestCommon('orchestra');
    this.Performances = RestCommon('performance');

    this.artists = [];
    this.pieces = [];
    this.scoretypes = [];
    this.containers = [];
    this.orchestras = [];
    this.performances = [];

    var makeGenericRead = function (Resource, items) {
        return function () {
            return Resource.read().then(function (response) {
                items.length = 0;
                items.push.apply(items, response);
            });
        }
    }

    this.getArtists = makeGenericRead(this.Artists, this.artists);
    this.getScoreTypes = makeGenericRead(this.ScoreTypes, this.scoretypes);
    this.getOrchestras = makeGenericRead(this.Orchestras, this.orchestras);
    this.getPerformances = makeGenericRead(this.Performances, this.performances);

    this.getContainers = function () {
        return this.Containers.read().then(function (response) {
            library.containers.length = 0;
            for (var i in response) {
                var container = response[i];
                if (!_.isNull(container.parent)) {
                    for (var j in response) {
                        var parent = response[j];
                        if (container.parent == parent.id) {
                            container.parent = parent;
                            break;
                        }
                    }
                }
            }
            library.containers.push.apply(library.pieces, response);
        });
    }

    this.getPieces = function () {
        return this.Pieces.read().then(function (response) {
            library.pieces.length = 0
            for (var p in response) {
                var piece = response[p];
                for (var i in piece.composer) {
                    var composer_id = piece.composer[i];
                    for (var j in library.artists) {
                        var composer = library.artists[j];
                        if (composer_id == composer.id) {
                            piece.composer[i] = composer;
                            break;
                        };
                    }
                };
                for (var i in piece.arranger) {
                    var arranger_id = piece.arranger[i];
                    for (var j in library.artists) {
                        var arranger = library.artists[j];
                        if (arranger_id == arranger.id) {
                            piece.arranger[i] = arranger;
                            break;
                        };
                    }
                }
                for (var i in library.containers) {
                    var container = library.containers[i];
                    if (container.id == piece.container) {
                        piece.container = container;
                        break;
                    }
                };
                for (var i in library.scoretypes) {
                    var scoretype = library.scoretypes[i];
                    if (scoretype.id == piece.score) {
                        piece.score = scoretype;
                        break;
                    }
                };
            };
            library.pieces.push.apply(library.pieces, response);
        });
    };

    this.getScoreTypes();
    this.getOrchestras();
    this.getPerformances();
    this.getArtists().then(function () {
        library.getContainers().then(function () {
            library.getPieces();
        });
    });
}]);
