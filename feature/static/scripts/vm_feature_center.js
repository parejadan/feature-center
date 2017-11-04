// service mediator
function model(view) {
    base_url = "/api/v1/"
    function post(url_path, payload) {
        $.ajax({
            type: "POST",
            url: url_path,
            data: JSON.stringify(payload),
            success: function(data) {
                console.log("success" + url_path)
                return true
            },
            error: function(data) {
                console.log("failure with url" + url_path)
                return false
            }
        })
    }

    function get(url, observer) {
        $.get(url)
            .done(function(data) {
                data = JSON.parse(data)
                for(i = 0; i < data.length; i++)
                    observer.push(data[i])
                console.log("success pulling from " + url)
            }).fail(function(data) {
                console.log("failure " + url)
            })
    }

    function get_client_features(client_id, priority_list, client_requests) {
        $.ajax({
            type: "GET",
            url: base_url + "features/getClientRequests/" + client_id,
            data: "",
            async: false,
            success: function(data) {
                data = JSON.parse(data)
                //todo add parallel the following lines
                data.available_requests.forEach(function(itm) { priority_list.push(itm)} )
                data.existing_requests.forEach(function(itm) { client_requests.push(itm)} )
                data.existing_requests
                return data
            },
            error: function(data) {
                console.log("failure" + url)
                return data
            }
        })
    }

    view.sync_client_requests = function() {
        client_feature_relations = {}
        get_client_features($("#client_id").val(), view.priority_list, view.client_requests)
        $("#feature_create").prop("disabled", false)
    }

        get(base_url + "clients", view.client_list)
        get(base_url + "products", view.product_list)
        get(base_url + "features", view.feature_list)
}

// view routers
function viewModel(view) {
    var mapping = { //possible routings for view
        feature_add: "#feature_add",
        features: "#features",
        reports: "#reports",
    }

    function anchor(vm, anc) {
        // update url anchor
        if (window.location.hash != anc) {
            window.location.hash = anc
        }
        vm.presenter(anc) //actually anchor to view
    }

    view.feature_add = function() {
        anchor(view, mapping.feature_add)
    }
    view.features = function() {
        anchor(view, mapping.features) 
    }
    view.reports = function() { 
        anchor(view, mapping.reports) 
    }

    //init presenter and define routings
    anchor(view, mapping.feature_add)
}

//view objects
var clientViewModel = function() {
    this.presenter = ko.observable()
    this.client_list = ko.observableArray([])
    this.feature_list = ko.observableArray([])
    this.priority_list = ko.observableArray([])
    this.product_list = ko.observableArray([])
    this.client_requests = ko.observableArray([])

    model(this) //apply model
    viewModel(this) //apply routings
}

ko.applyBindings(clientViewModel)