// service mediator
function model(view) {
    base_url = "/api/v1/"
    function post(url_path, payload) {
        $.ajax({
            type: "POST",
            url: url_path,
            async: false,
            data: JSON.stringify(payload),
            success: function(data) {
                console.log("success" + url_path)
            },
            error: function(data) {
                console.log("failure with url" + url_path)
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
            },
            error: function(data) {
                console.log("failure" + url)
            }
        })
    }

    view.feature_create = function() {
        view.disable_feature_add_button(true)
        payload = {
            "title": $("#title").val(),
            "description": $("#description").val(),
            "client_id": $("#client_id").val(),
            "product_id": $("#product_id").val(),
            "priority_id": $("#priority_id").val(),
            "date_target": $("#date_target").val(),
        }
        post(base_url + "features/create", payload, view.reset_feature_add_form)
        view.sync_client_requests()
        view.reset_feature_add_form()
    }

    view.sync_client_requests = function() {
        view.priority_list([])
        view.client_requests([])
        get_client_features($("#client_id").val(), view.priority_list, view.client_requests)
        view.disable_feature_add_button(false)
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

    view.disable_feature_add_button = function(disable_btn) {
        $("#feature_create").prop("disabled", disable_btn)
    }

    view.reset_feature_add_form = function() {
        $("#feature_add_form").reset() // allow user to easily insert new data
        view.client_requests.push(payload)
        view.disable_feature_add_button(false)
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

    viewModel(this) //apply routings
    model(this) //apply model
}

ko.applyBindings(clientViewModel)