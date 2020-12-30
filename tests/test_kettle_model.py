# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest

from brewpi.devices.drivers import GpioControl
from brewpi.devices.models import Heater, Kettle, Pump, TempSensor


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

        assert kettle.name == "foo"
        assert kettle.target_temp == 0.0
        assert kettle.is_running is False
        assert kettle.hyst_window == 5.0
        assert kettle.control_type == Kettle.ControlType.HYSTERESIS
        assert kettle.task_id is None
        assert kettle.heater_id is None
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_create_method_kwargs(self):
        """Create a kettle."""
        data = {"name": "foo"}
        kettle = Kettle.create(**data)

        assert "foo" == kettle.name
        assert kettle.target_temp == 0.0
        assert kettle.is_running is False
        assert kettle.hyst_window == 5.0
        assert kettle.control_type == Kettle.ControlType.HYSTERESIS
        assert kettle.task_id is None
        assert kettle.heater_id is None
        assert Kettle.get_by_id(kettle.id) is kettle

    def test_update_method(self):
        """Update a kettle."""
        kettle = Kettle.create(name="foo")
        heater = Heater.create(name="Heater", gpio_num=1)
        assert kettle.heater is None
        kettle.update(heater=heater)
        assert Kettle.get_by_id(kettle.id).heater is heater

    def test_current_temp(self, mocker):
        """Test current temp returns correctly when linked/unlinked."""
        mocker.patch(
            "brewpi.devices.drivers.TempSensorDriver.get_temp_c", return_value=50.0
        )
        kettle = Kettle.create(name="foo")
        assert kettle.current_temp == 0.0

        TempSensor.create(name="foo", gpio_num=1, kettle_id=1)
        assert kettle.current_temp == 50.0

    def test_heater_turn_on_turn_off(self, mocker):
        """Test heater turns on then off from kettle control."""
        mocker.patch("brewpi.devices.drivers.GpioControl.write")
        kettle = Kettle.create(name="foo")
        kettle.heater_enable(True)
        assert not GpioControl.write.called
        kettle.heater_enable(False)
        assert not GpioControl.write.called

        heater = Heater.create(name="Heater", gpio_num=1)
        kettle.update(heater_id=heater.id)
        assert kettle.heater == heater
        assert kettle.heater.current_state is False
        assert heater.current_state is False
        assert not GpioControl.write.called

        kettle.heater_enable(True)
        assert kettle.heater.current_state is True
        assert heater.current_state is True
        assert GpioControl.write.assert_called_once

        kettle.heater_enable(False)
        assert kettle.heater.current_state is False
        assert heater.current_state is False
        assert GpioControl.write.assert_called_once

    def test_pump_turn_on_turn_off(self, mocker):
        """Test pump turns on then off from kettle control."""
        mocker.patch("brewpi.devices.drivers.GpioControl.write")
        kettle = Kettle.create(name="foo")
        kettle.pump_enable(True)
        assert not GpioControl.write.called
        kettle.pump_enable(False)
        assert not GpioControl.write.called

        pump = Pump.create(name="Pump", gpio_num=1, kettle_id=1)
        assert kettle.pump.current_state is False
        assert pump.current_state is False
        assert not GpioControl.write.called

        kettle.pump_enable(True)
        assert kettle.pump.current_state is True
        assert pump.current_state is True
        assert GpioControl.write.assert_called_once

        kettle.pump_enable(False)
        assert kettle.pump.current_state is False
        assert pump.current_state is False
        assert GpioControl.write.assert_called_once

    def test_current_target_temp(self):
        """Test current target temp property."""
        kettle = Kettle.create(name="foo")
        assert kettle.current_target_temperature == 0.0
        kettle.current_target_temperature = 26.5
        assert kettle.current_target_temperature == 26.5

    def test_is_loop_running(self):
        """Test current target temp property."""
        kettle = Kettle.create(name="foo")
        assert kettle.is_loop_running is False
        kettle.is_loop_running = True
        assert kettle.is_loop_running is True

    def test_repr(self):
        """Test for the repr method."""
        kettle = Kettle.create(name="foo")
        assert repr(kettle) == "<Kettle(foo)>"
