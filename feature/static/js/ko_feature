function FeatureViewModel() {
    this.fullName = ko.observable('bert')
    this.displayName = ko.compute(function() {
        return this.displayName.toUpperCase()
    }, this)
}

ko.applyBinding(new FeatureViewModel())