Backend (& UI model) TODO
----
- [x] service call for submitting new feature requests
- [ ] validate that added feature id doesn't currently exists when submitting new feature
- [ ] validate that before going into the process of adding a feature, that client doesnt reach feature lim (config val)
- [x] service & call for pulling clients
- [x] service & call for pulling existing features
- [x] service & call for pulling existing products
- [x] service call for pulling priority list for a given client
- [x] load model test data from csv files
- [x] database build up and tear down checks
- [ ] revise code documentation and exception handling
- [ ] add logging
- [ ] add unit tests

UI TODO
-------
- [x] disable feature submission until a client is selected in adding feature
- [ ] once a client is selected show to the right existing client features request
- [ ] allow features to be dragged and dropped for ranking priority (priority ID gets updated in UI)
- [ ] lock adding feature form if user is updating priority - unlock after update is complete
- [ ] add form validations for adding feature (date min 3 months in the future), title, and description need to be entered
- [ ] when client features are shown and feature is clicked, replace client_feature_view with feature_details


Infrastructure TODO
-------------------
- [ ] setup deployment pipeline from git
- [x] refactor project structure for differnt service version supports (follow javascript/bootstrap practices)

Extra
-----
- [ ] In reports tab, compose a reports for a given client, given product, or no product
- [ ] in reports show message stating when a client's reached their feature request limit
- [ ] show default products list by default  ordered in desc by num of feature requests