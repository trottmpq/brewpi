# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest

from brewpi.devices.models import Kettle, Heater, Pump


@pytest.mark.usefixtures("db")
class TestKettle:
    """Kettle tests."""

    def test_get_by_id(self):
        """Get kettle by ID."""
        kettle = Kettle("foo")
        kettle.save()
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_create_direct(self):
        """Create a kettle."""
        kettle = Kettle(name="foo")
        kettle.save()
        assert kettle.name == Kettle.get_by_id(kettle.id).name
        assert kettle.name == "foo"
        assert kettle.heater is Kettle.get_by_id(kettle.id).heater
        assert kettle.heater is None
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_create_method(self):
        """Create a kettle."""
        kettle = Kettle.create(name="foo")

        assert "foo" == kettle.name
        assert kettle.state is False
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_create_method_kwargs(self):
        """Create a kettle."""
        data = {"name": "foo"}
        kettle = Kettle.create(**data)

        assert "foo" == kettle.name
        assert kettle.state is False
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_update_method(self):
        """Update a kettle."""
        kettle = Kettle.create(name="foo")
        heater = Heater.create(name="Heater", gpio_num=1)
        assert kettle.heater is None
        kettle.update(heater=heater)
        assert Kettle.get_by_id(kettle.id).heater is heater

    def test_heater_turn_on_turn_off(self):
        """Test heater turns on then off from kettle control."""
        heater = Heater.create(name="Heater", gpio_num=1)
        kettle = Kettle.create(name="foo", heater=heater)
        assert Kettle.get_by_id(kettle.id).heater.current_state is False
        assert Heater.get_by_id(heater.id).current_state is False
        kettle.heater_enable(True)
        assert Kettle.get_by_id(kettle.id).heater.current_state is True
        assert Heater.get_by_id(heater.id).current_state is True
        kettle.heater_enable(False)
        assert Kettle.get_by_id(kettle.id).heater.current_state is False
        assert Heater.get_by_id(heater.id).current_state is False

    def test_pump_turn_on_turn_off(self):
        """Test pump turns on then off from kettle control."""
        pump = Pump.create(name="Pump", gpio_num=1)
        kettle = Kettle.create(name="foo", pump=pump)
        assert Kettle.get_by_id(kettle.id).pump.current_state is False
        assert Pump.get_by_id(pump.id).current_state is False
        kettle.pump_enable(True)
        assert Kettle.get_by_id(kettle.id).pump.current_state is True
        assert Pump.get_by_id(pump.id).current_state is True
        kettle.pump_enable(False)
        assert Kettle.get_by_id(kettle.id).pump.current_state is False
        assert Pump.get_by_id(pump.id).current_state is False
