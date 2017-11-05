function model(viewModel) {
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
                console.log("failure: " + base_url + "features/getClientRequests/")
            }
        })
    }

    function searchObservableArray(_list, id) {
        token = -1
        ko.utils.arrayForEach(_list(), function(itm) {
            if (itm.id == id) {
                token = itm
                return
            }
        })
        return token
    }

    viewModel.feature_create = function() {
        viewModel.disable_feature_add_button(true)
        payload = {
            "title": $("#title").val(),
            "description": $("#description").val(),
            "client_id": $("#client_id").val(),
            "product_id": $("#product_id").val(),
            "priority_id": $("#priority_id").val(),
            "date_target": $("#date_target").val(),
        }
        post(base_url + "features/create", payload)
        viewModel.sync_client_requests()
    }

    viewModel.sync_client_requests = function() {
        viewModel.reset_client_data()
        get_client_features($("#client_id").val(), viewModel.priority_list, viewModel.client_requests)
        viewModel.disable_feature_add_button(false)
    }

    viewModel.sync_reports = function() {
            get(base_url + "features", viewModel.feature_list)
    }

    viewModel.get_client_name = function(client_id) {
        return searchObservableArray(viewModel.client_list, client_id).name;
    }

    viewModel.get_product_name = function(product_id) {
        return searchObservableArray(viewModel.product_list, product_id).product_code;
    }

    get(base_url + "clients", viewModel.client_list)
    get(base_url + "products", viewModel.product_list)
}

function viewModel(view) {
    var mapping = { //possible routings for view
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

    view.disable_feature_add_button = function(disable_btn) {
        $("#feature_create").prop("disabled", disable_btn)
    }

    view.reset_client_data = function() {
        view.priority_list([])
        view.client_requests([])
    }

    view.clean_feature_form = function() {
        $("#feature_add_form")[0].reset()
        view.reset_client_data()
        view.disable_feature_add_button(true)
    }

    view.feature_add = function() {
        anchor(view, mapping.feature_add)
    }

    view.reports = function() {
        view.sync_reports()
        anchor(view, mapping.reports) 
    }

    view.view_feature_details = function(feature_id) {
        console.log(feature_id)
        view.feature_article(feature_id)
    }

    //init presenter and define routings
    anchor(view, mapping.feature_add)
    view.modal_presenter("#feature_details") //for viewing feature details and allowing updates and deletes
}

//view objects
var featureAddViewModel = function() {
    this.presenter = ko.observable()
    this.modal_presenter = ko.observable()
    this.feature_article = ko.observable()
    this.client_list = ko.observableArray([])
    this.feature_list = ko.observableArray([])
    this.priority_list = ko.observableArray([])
    this.product_list = ko.observableArray([])
    this.client_requests = ko.observableArray([])

    viewModel(this) //apply routings
    model(this) //apply model
}

ko.applyBindings(featureAddViewModel)