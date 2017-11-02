// view routers
function viewModel(view) {
    var mapping = { //possible routings for view
        clients: "#clients",
        features: "#features",
        feature_add: "#feature_add",
        reports: "#reports",
    }

    //init presenter and define routings
    view.presenter = ko.observable(mapping.clients)
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

}

// service mediator
function model(view) {
    base_url = "/api/v1/"
    function post(url, payload) {
        $.post(url, payload)
            .done(function () {
                console.log("success" + url)
            }).fail(function (data) {
                console.log("failure with url" + url)
            })
    }

    view.feature_create = function () {
        $("#feature_create").prop("disabled", true)
        payload = {
            title: $("#title").val(),
            description: $("#description").val(),
            client_id: $("#client_id").val(),
            product_id: $("#product_id").val(),
            date_target: $("#date_target").val(),
            priority_id: $("#priority_id").val()
        }
        post(base_url + "features/create", payload)
    }

}

var clientViewModel = function() {
    this.client_list = ko.observable([
        {name: "Joe Comp", email: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_id: '3'},
        {name: "Joe Comp", email: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_id: '3'},
        {name: "Joe Comp", email: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_id: '3'},
        ])
    this.product_type = [
        {id: "1", name: "Sales Analysis"},
        {id: "2", name: "Payroll"},
        {id: "3:", name: "Revaniew Analysis"},
        ]

    this.priority_list = [
        {id: "1", name: "1"},
        {id: "2", name: "2"},
        {id: "3", name: "3"},
        {id: "4", name: "4"},
        {id: "5", name: "5"},
        {id: "6", name: "6"},
        {id: "7", name: "7"},
        ]
    viewModel(this) //apply routings
    model(this) //apply model
}

ko.applyBindings(clientViewModel)