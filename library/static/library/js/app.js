'use strict';

angular.module("MusicLibrary", ["ui.bootstrap", "ui.keypress", "restangular"])

.config(['RestangularProvider', function (RestangularProvider) {
    RestangularProvider.setBaseUrl('/api/');
    RestangularProvider.setRequestSuffix('/');
}])

