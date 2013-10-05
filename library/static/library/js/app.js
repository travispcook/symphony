'use strict';

angular.module("MusicLibrary", ["ui.bootstrap", "restangular"])

.config(function (RestangularProvider) {
    RestangularProvider.setBaseUrl('/api/');
    RestangularProvider.setRequestSuffix('/');
})

