'use strict';

var RestCommon = function (resource) {
    return function (Restangular) {
        this.rest = Restangular.all(resource);
        this[resource] = [];
        this.items = this[resource];

        this.read = function () {
            var promise =  this.rest.getList();
            var service = this;
            promise.then(function (response) {
                service[resource].length = 0
                service[resource].push.apply(service[resource], response);
                if ('metadata' in response) {
                    service[resource].metadata = response.metadata;
                }
            });
            return promise;
        };

        this.post = function (data) {
            var service = this;
            var promise = this.rest.post(data);
            return promise.then(function (newItem) {
                service[resource].push(newItem);
                return newItem;
            });
        };

        this.put = function (item, data) {
            $.extend(item, data);
            return item.put();
        };

        this.delete = function (item) {
            var resource = this[resource];
            for (var i = 0; i < resource.length; i++) {
                if (resource[i] == item) {
                    var promise = item.remove();
                    resource.splice(i, 1);
                    return promise
                }
            }
        };

        this.read();
    }
};

app.service('Artists', RestCommon('artists'));
app.service('Pieces', RestCommon('piece'));
app.service('ScoreType', RestCommon('scoretype'));
app.service('Containers', RestCommon('containers'));
app.service('Orchestras', RestCommon('orchestras'));
app.service('Performances', RestCommon('performances'));
