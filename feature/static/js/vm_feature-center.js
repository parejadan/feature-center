// view routers
var anchors = { // template urls for navigating through single page app
    client_add: "client_add",
    client_info: "client_info",
    client_update: "client_update",
    clients_view: "clients_view",
}
function routeAnchor(vm, anc) {
    if (window.location.hash != "#" + anc) {
        window.location.hash = "#" + anc
    }
    vm.presenter(anc)
}

var viewModelFeatureCenter = function() {
    this.presenter = ko.observable("clients_view")
    this.client_list = ko.observable([])

    this.clients_view = function() {
        routeAnchor(this, anchors.clients_view)
    }
    this.client_update = function() {
        routeAnchor(this, anchors.client_update)
    }
    this.client_info = function() {
        routeAnchor(this, anchors.client_info)
    }
    this.client_add = function() {
        routeAnchor(this, anchors.client_add)
    }
}

ko.applyBindings(viewModelFeatureCenter)