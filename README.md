Backend (& UI model) TODO
----
- [x] service call for submitting new feature requests
- [x] prevent user from exceeding their limit requests
- [x] service & call for pulling clients
- [x] service & call for pulling existing features
- [x] service & call for pulling existing products
- [x] service call for pulling priority list for a given client
- [x] load model test data from csv files
- [x] database build up and tear down checks
- [x] revise code documentation and exception handling
- [ ] add unit tests

UI TODO
-------
- [x] disable feature submission until a client is selected in adding feature
- [x] once a client is selected show existing client features request
- [x] allow features to be viewed,updated, and details whenever a feature is clicked
- [x] when a client is selected show their existing features


Infrastructure TODO
-------------------
- [ ] setup deployment pipeline from git
- [x] refactor project structure for different service version supports (follow javascript/bootstrap practices)

Extra
-----
- [ ] In reports tab, compose a reports for a given client, given product, or no product
- [ ] in reports show message stating when a client's reached their feature request limit
- [ ] show default products list by default  ordered in desc by num of feature requests
- [ ] add form validations for adding feature (date min 3 months in the future), title, and description need to be entered