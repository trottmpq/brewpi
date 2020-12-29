# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest

from brewpi.devices.models import TempSensor


@pytest.mark.usefixtures("db")
class TestTempSensor:
    """TempSensor tests."""

    def test_get_by_id(self):
        """Get temp_sensor by ID."""
        temp_sensor = TempSensor("foo", 2)
        temp_sensor.save()
        assert TempSensor.get_by_id(temp_sensor.id) is temp_sensor

    def test_create_direct(self):
        """Create a temp_sensor."""
        temp_sensor = TempSensor(name="foo", gpio_num=1)
        temp_sensor.save()
        assert temp_sensor.name == "foo"
        assert temp_sensor.gpio_num == 1
        assert temp_sensor.temperature == 0.0
        assert TempSensor.query.get(temp_sensor.id) is temp_sensor

    def test_create_method(self):
        """Create a temp_sensor."""
        temp_sensor = TempSensor.create(name="foo", gpio_num=1)

        assert "foo" == temp_sensor.name
        assert 1 == temp_sensor.gpio_num
        assert temp_sensor.temperature == 0.0
        assert TempSensor.query.get(temp_sensor.id) is temp_sensor

    def test_create_method_kwargs(self):
        """Create a temp_sensor."""
        data = {"name": "foo", "gpio_num": 1}
        temp_sensor = TempSensor.create(**data)

        assert "foo" == temp_sensor.name
        assert 1 == temp_sensor.gpio_num
        assert temp_sensor.temperature == 0.0
        assert TempSensor.query.get(temp_sensor.id) is temp_sensor

    def test_update_method(self):
        """Update a temp_sensor."""
        temp_sensor = TempSensor.create(name="foo", gpio_num=1)
        assert 1 == temp_sensor.gpio_num
        temp_sensor.update(gpio_num=2)
        assert 2 == temp_sensor.gpio_num

    def test_current_temperature(self, mocker):
        """Test current temperature gets the latest temp."""
        mocker.patch(
            "brewpi.devices.drivers.TempSensorDriver.get_temp_c", return_value=50.0
        )

        TempSensor.create(name="foo", gpio_num=1)
        temp_sensor = TempSensor.get_by_id(1)
        assert temp_sensor.current_temperature == 50.0
        assert type(temp_sensor.current_temperature) is float

    def test_repr(self):
        """Test for the repr method."""
        temp_sensor = TempSensor.create(name="foo", gpio_num=1)
        assert repr(temp_sensor) == "<TempSensor(foo: 1)>"
