Intro
-----
> Minimalist POC web app for client ticketing system for desired 'feature enhancements' to available products. 
> Application is designed considering the MVP, MVVC architectural patterns with a aim for CI development.
> Unit tests are aimed to maintain obscure logic within the code with respect to python backend, while 
> Selenium test cases cover issues encountered during development of knockoutjs code. 
> Selenium was chosen for functional testing because it can be scaled to End-to-End validation (DB-BLL-API-UI)


Setup Guide for Localhost
-----------
- developed using Python3+
- Smoke tested with: Windows Subsystem Linix, Linux
- __Installing Python Dependencies__
  1. `sudo apt-get install python3-pip` # get package manager
  2. `sudo pip3 install virtualenv` # for making sure python setup is clean
  3. `virtualenv env` # execute this within project directory
  4. `source env/bin/activate` # you're now in virtual environment and ready to install python depencendies
  5. `pip3 install -r requirements.txt` # install required packages for development and testing
- __Setting Up Database:__
  - `sudo apt-get update && apt-get install postgresql postgresql-contrib` # installing postgres database if you don't have it
  - once database is installed you need to create postgres role (user) and database (db) specified in config.json
  - login credentials of that user should then get specified in config.json file located in root of this directory
  1. `sudo su postgres` # postgres creates user postgres with empty password
  2. `psql` # if don't get the stupid _'.s.PGSQL.5432?'_ (PORT ERROR), skip steps 3-5 
  3. in postgres type `\q` then exit postgres account using `exit`
  4. `sudo service postgres restart` # if this doesn't work google is your best friend
  5. `sudo su postgres` to go back to posgres account, then `psql` should work now
  6. `CREATE ROLE _enter_config_user_name;` # semicolen is important; then setup password for roll (google)
  7. `ALTER ROLE _enter_config_user_name CREATEDB;`
  8. `CREATE DATABASE _enter_config_database_name;`
  9. `GRANT ALL PRIVILEGES ON DATABASE enter_config_database_name TO _enter_config_user_name`
  10. `\q` # exit so we can execute initdb.py
  11. `python3 initdb.py` # if you get error beccause some package is not install repeat step 4 in Python Dependencies section
  12. `python3 runserveer.py` # already setup to run app with waitress wsgi (works on windows/ubuntu)
  13. Navigate in your browser to localhost:8080
  14. Break it and post issues :)
  

Executing Tests
---------------
- Within project root, execute `python3 py.test` (if it breaks execute step 4 in Python dependencies)

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
- [x] add unit tests

UI TODO
-------
- [x] disable feature submission until a client is selected in adding feature
- [x] once a client is selected show existing client features request
- [x] allow features to be viewed,updated, and details whenever a feature is clicked
- [x] when a client is selected show their existing features


Infrastructure TODO
-------------------
- [x] setup deployment pipeline from git (requires dynamic dns setup script, and checking to live branch auto execute runserver.py)
- [x] refactor project structure for different service version supports (follow javascript/bootstrap practices)
- [ ] create script for dynamic dns setup if IP changes
- [ ] trouble shoot script that detects checkin to 'live' branch
- [x] create script to send out email of whatever tests that fail in remote branch (travis CI)

Extra/Missing
-------------
- [ ] In reports tab, compose a reports for a given client, given product, or no product
- [ ] in reports show message stating when a client's reached their feature request limit
- [ ] form validations for adding feature (date min 3 months in the future), title, and description need to be entered
- [ ] success/failure UI messages for every transaction
- [-] add functional tests using selenium web driver and phantomJS
