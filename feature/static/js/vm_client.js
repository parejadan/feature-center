// view routers
function clientView(view) {
    var mapping = { //possible routings for view
        clients: "#clients",
        features: "#features",
        feature_add: "#feature_add",
        reports: "#reports",
    }

    //init presenter and define routings
    view.presenter = ko.observable(mapping.clients)
    function anchor(vm, anc) {
        if (window.location.hash != anc) {
            window.location.hash = anc
        }
        vm.presenter(anc)
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

var clientViewModel = function() {
    this.navbar = ko.observable("#navbar")
    this.client_list = ko.observable([
        {name: "Joe Comp", email_address: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_type: '3'},
        {name: "Joe Comp", email_address: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_type: '3'},
        {name: "Joe Comp", email_address: "joe@comp.com",
         phone_number: "912-345-9213", request_cnt: '3', product_type: '3'},
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
    clientView(this) //apply routings
}

ko.applyBindings(clientViewModel)