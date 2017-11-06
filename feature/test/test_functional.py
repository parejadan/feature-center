import pytest
from random import random
import platform
from feature import env_config
from selenium import webdriver


class TestFunctional:
    def __init__(self):
        self.base_url = env_config.REGRESSION_TEST_HOST
        self.driver = webdriver.Chrome(executable_path=r'' + env_config.REGRESSION_DRIVER.format(platform.system()))


# functional test that should get written:
# bug 1 (fixed): navigate to reports tab with existing feature requests already in database,
#### validate when user navigate between feature_add and reports, that number of overall features
####   in reports do not exceed number of records in database
# bug 2 (fixed): validate that when user adds a feature request, after hitting submit, overall available features
####   only show those currently not allocaed to client
# bug 3 (fixed): validate that when a client exceeds their number of available feature requests,
####   when a feature's priority gets updated, that all other features get their priority rank updated correctly
####   (not to be confused with unit test that only validates priority set uniqueness)
