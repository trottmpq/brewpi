# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest

from brewpi.devices.drivers import GpioControl
from brewpi.devices.models import Pump


@pytest.mark.usefixtures("db")
class TestPump:
    """Pump tests."""

    def test_get_by_id(self):
        """Get pump by ID."""
        pump = Pump("foo", 2)
        pump.save()
        assert Pump.get_by_id(pump.id) is pump

    def test_create_direct(self):
        """Create a pump."""
        pump = Pump(name="foo", gpio_num=1)
        pump.save()
        assert pump.name == "foo"
        assert pump.gpio_num == 1
        assert pump.state is False
        assert Pump.query.get(pump.id) is pump

    def test_create_method(self):
        """Create a pump."""
        pump = Pump.create(name="foo", gpio_num=1)

        assert "foo" == pump.name
        assert 1 == pump.gpio_num
        assert pump.state is False
        assert Pump.query.get(pump.id) is pump

    def test_create_method_kwargs(self):
        """Create a pump."""
        data = {"name": "foo", "gpio_num": 1}
        pump = Pump.create(**data)

        assert "foo" == pump.name
        assert 1 == pump.gpio_num
        assert pump.state is False
        assert Pump.query.get(pump.id) is pump

    def test_update_method(self):
        """Update a pump."""
        pump = Pump.create(name="foo", gpio_num=1)
        assert 1 == pump.gpio_num
        pump.update(gpio_num=2)
        assert 2 == pump.gpio_num

    def test_turn_on_turn_off(self, mocker):
        """Test turns on then off."""
        mocker.patch("brewpi.devices.drivers.GpioControl.write")
        Pump.create(name="foo", gpio_num=1)
        pump = Pump.query.get(1)
        assert pump.current_state is False
        assert not GpioControl.write.called
        pump.turn_on()
        assert pump.current_state is True
        assert GpioControl.write.assert_called_once
        pump.turn_off()
        assert pump.current_state is False
        assert GpioControl.write.assert_called

    def test_repr(self):
        """Test for the repr method."""
        pump = Pump.create(name="foo", gpio_num=1)
        assert repr(pump) == "<Pump(foo: 1, False)>"
