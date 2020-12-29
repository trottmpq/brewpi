# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest

from brewpi.devices.drivers import GpioControl
from brewpi.devices.models import Heater


@pytest.mark.usefixtures("db")
class TestHeater:
    """Heater tests."""

    def test_get_by_id(self):
        """Get heater by ID."""
        heater = Heater("foo", 2)
        heater.save()
        assert Heater.get_by_id(heater.id) is heater

    def test_create_direct(self):
        """Create a heater."""
        heater = Heater(name="foo", gpio_num=1)
        heater.save()
        assert heater.name == "foo"
        assert heater.gpio_num == 1
        assert heater.state is False
        assert Heater.query.get(heater.id) is heater

    def test_create_method(self):
        """Create a heater."""
        heater = Heater.create(name="foo", gpio_num=1)

        assert "foo" == heater.name
        assert 1 == heater.gpio_num
        assert heater.state is False
        assert Heater.query.get(heater.id) is heater

    def test_create_method_kwargs(self):
        """Create a heater."""
        data = {"name": "foo", "gpio_num": 1}
        heater = Heater.create(**data)

        assert "foo" == heater.name
        assert 1 == heater.gpio_num
        assert heater.state is False
        assert Heater.query.get(heater.id) is heater

    def test_update_method(self):
        """Update a heater."""
        heater = Heater.create(name="foo", gpio_num=1)
        assert 1 == heater.gpio_num
        heater.update(gpio_num=2)
        assert 2 == heater.gpio_num

    def test_turn_on_turn_off(self, mocker):
        """Test turns on then off."""
        mocker.patch("brewpi.devices.drivers.GpioControl.write")
        Heater.create(name="foo", gpio_num=1)
        heater = Heater.query.get(1)
        assert heater.current_state is False
        assert not GpioControl.write.called
        heater.turn_on()
        assert heater.current_state is True
        assert GpioControl.write.assert_called_once
        heater.turn_off()
        assert heater.current_state is False
        assert GpioControl.write.assert_called

    def test_repr(self):
        """Test for the repr method."""
        heater = Heater.create(name="foo", gpio_num=1)
        assert repr(heater) == "<Heater(foo: 1, False)>"
