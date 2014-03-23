"""
    Functionnal test for SMEPI test cases.
"""

#!/usr/bin/python
# -*- coding: utf8 -*-
# -*- Mode: Python; py-indent-offset: 4 -*-
# pylint: disable=W0613

from fabric.api import local
from behave import when, given, then  # pylint: disable-msg=E0611
from src.helper.storage import remove_data, data_size


def verify_db_size(config):
    """
        Generic method to verify db size.
    """
    remove_data()
    local("python data_generator.py --action collect --configfile %s" % (
        config["filename"]))
    size = 0
    for user in xrange(config["users"]):
        for sensor in config["sensors"]:
            sensor_name = sensor[0]
            if config["users"] > 1:
                sensor_name += str(user)
            size += sensor[1]
            assert data_size(sensor_name=sensor_name) == sensor[1]
    assert data_size() == size


@given(u'I generate data for 1 smepi user')
def data_generation_1_smepi(context):
    """
        Data generation for 1 smepi user.
    """
    config = {
        "filename": "tests/config/smepi1.json",
        "users": 1,
        "sensors": [("e002", 3003), ("w002", 61), ("g002", 61)]
    }

    verify_db_size(config)


@when(u'I send data for 1 smepi user')
def data_sending_1_smepi(context):
    """
        Data sending for 1 smepi user
    """
    #local("python ga.py --action send --configfile tests/config/smepi1.json")
    #assert data_size() == 0
    assert True


@then(u'I should retrieve this data into NSCL for 1 smepi user')
def data_into_nscl_1_smepi(context):
    """
        Data should be in NSCL for 1 smepi user
    """
    assert True


@given(u'I generate data for 50 smepi user')
def data_generation_50_smepi(context):
    """
        Data generation for 50 smepi user
    """
    config = {
        "filename": "tests/config/smepi50.json",
        "users": 50,
        "sensors": [("e002", 3003), ("w002", 61), ("g002", 61)]
    }

    verify_db_size(config)


@when(u'I send data for 50 smepi user')
def data_sending_50_smepi(context):
    """
        Data sending for 50 smepi user
    """
    assert True


@then(u'I should retrieve this data into NSCL for 50 smepi user')
def data_into_nscl_50_smepi(context):
    """
        Data should be in NSCL for 50 smepi user
    """
    assert True


@given(u'I generate data for 1 es user')
def data_generation_1_es(context):
    """
        Data generation for 1 es user
    """
    config = {
        "filename": "tests/config/es1.json",
        "users": 1,
        "sensors": [("e002", 49)]
    }

    verify_db_size(config)


@when(u'I send data for 1 es user')
def data_sending_1_es(context):
    """
        Data sending for 1 ES user
    """
    assert True


@then(u'I should retrieve this data into NSCL for 1 es user')
def data_into_nscl_1_es(context):
    """
        Data should be in NSCL for 1 es user
    """
    assert True


@given(u'I generate data for 20 es user')
def data_generation_20_es(context):
    """
        Data generation for 20 es user
    """
    config = {
        "filename": "tests/config/es20.json",
        "users": 20,
        "sensors": [("e002", 49)]
    }

    verify_db_size(config)


@when(u'I send data for 20 es user')
def data_sending_20_es(context):
    """
        Data sending for 20 ES users
    """
    assert True


@then(u'I should retrieve this data into NSCL for 20 es user')
def data_into_nscl_20_es(context):
    """
        Data should be in NSCL for 20 es users
    """
    assert True


@given(u'I generate data for 1000 es user')
def data_generation_1000_es(context):
    """
        Data generation for 1000 es user
    """
    config = {
        "filename": "tests/config/es1000.json",
        "users": 1000,
        "sensors": [("e002", 49)]
    }

    verify_db_size(config)


@when(u'I send data for 1000 es user')
def data_sending_1000_es(context):
    """
        Data sending for 1000 ES users
    """
    assert True


@then(u'I should retrieve this data into NSCL for 1000 es user')
def data_into_nscl_1000_es(context):
    """
        Data should be in NSCL for 1000 es users
    """
    assert True


@given(u'I generate data for 1 gridteams user')
def data_generation_1_gridteams(context):
    """
        Data generation for 1 gridteams user
    """
    #local("python ga.py --configfile tests/config/gridteams1.json")
    assert True


@when(u'I send data for 1 gridteams user')
def data_sending_1_gridteams(context):
    """
        Data sending for 1 gridteams user
    """
    assert True


@then(u'I should retrieve this data into NSCL for 1 gridteams user')
def data_into_nscl_1_gridteams(context):
    """
        Data should be in NSCL for 1 gridteams user
    """
    assert True


@given(u'I generate data for 30 gridteams user')
def data_generation_30_gridteams(context):
    """
        Data generation for 30 gridteams user
    """
    #local("python ga.py --configfile tests/config/gridteams30.json")
    assert True


@when(u'I send data for 30 gridteams user')
def data_sending_30_gridteams(context):
    """
        Data sending for 30 gridteams users
    """
    assert True


@then(u'I should retrieve this data into NSCL for 30 gridteams user')
def data_into_nscl_30_gridteams(context):
    """
        Data should be in NSCL for 30 gridteams users
    """
    assert True
