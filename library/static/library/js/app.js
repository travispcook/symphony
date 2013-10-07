'use strict';

angular.module("MusicLibrary", ["ui.bootstrap", "ui.keypress", "restangular"])

.config(function (RestangularProvider) {
    RestangularProvider.setBaseUrl('/api/');
    RestangularProvider.setRequestSuffix('/');
})

