// view routers
function viewModel(view) {
    var mapping = { //possible routings for view
        clients: "#clients",
        features: "#features",
        feature_add: "#feature_add",
        reports: "#reports",
    }

    function anchor(vm, anc) {
        // update url anchor
        if (window.location.hash != anc) {
            window.location.hash = anc
        }
        vm.presenter(anc) //actually anchor to view
    }

    view.clients = function() { 
        anchor(view, mapping.clients)

    }
    view.features = function() { 
        anchor(view, mapping.features) 
    }
    view.feature_add = function() { 
        anchor(view, mapping.feature_add) 
    }
    view.reports = function() { 
        anchor(view, mapping.reports) 
    }

    //init presenter and define routings
    anchor(view, mapping.clients)
}

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

    view.feature_create = function() {
        $("#feature_create").prop("disabled", true)
        payload = {
            "info": {
                title: $("#title").val(),
                description: $("#description").val(),
                date_target: $("#date_target").val() },
            "priority": {
                id: $("#priority_id").val() },
            "client": {
                id: $("#client_id").val() },
            "product": {
                id: $("#client_id").val() },
        }
        if (post(base_url + "features/create", payload)) {
            $("#feature_add_form").reset() // allow user to easily insert new data
        }
        //$("#feature_create").prop("disabled", false)
    }

    //load all data
    //todo add lazy loading and parallel calls for everything below
    get(base_url + "clients", view.client_list)
    get(base_url + "features", view.feature_list)
    get(base_url + "priorities", view.priority_list)
    get(base_url + "products", view.product_list)
}

//view objects
var clientViewModel = function() {
    this.presenter = ko.observable()
    this.client_list = ko.observableArray([])
    this.feature_list = ko.observableArray([])
    this.priority_list = ko.observableArray([])
    this.product_list = ko.observableArray([])

    viewModel(this) //apply routings
    model(this) //apply model
}

ko.applyBindings(clientViewModel)