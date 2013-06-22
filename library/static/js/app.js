'use strict';

var app = angular.module("MusicLibrary", ["restangular"]);

app.config(function (RestangularProvider) {
    RestangularProvider.setBaseUrl('/api');
    RestangularProvider.setResponseExtractor(function (response, operation, what, url) {
        if (operation == 'getList') {
            var newResponse;
            if ('results' in response) {
                newResponse = response.results;
                newResponse.metadata = {
                    count: response.count,
                    next: response.next,
                    previous: response.previous
                };
            } else {
                newResponse = response;
            }
            return newResponse;
        } else {
            return response;
        }
    });
    RestangularProvider.setListTypeIsArray(false);
});

