# -*- coding: utf-8 -*-
"""Model unit tests."""

import pytest


@pytest.mark.usefixtures("db")
class TestHeater:
    """Heater tests."""

    def test_is_empty(self, testapp):
        """Get empty heater list."""
        response = testapp.get("/devices/Heater/")
        assert response.status_int == 200
        assert response.content_type == "application/json"
        assert response.json == []

    def test_create(self, testapp):
        """Create a heater."""
        response = testapp.post_json("/devices/Heater/", dict(name="Heater1", gpio_num=1))
        assert response.status_int == 200
        assert response.content_type == "application/json"
        assert response.json == {
            "active_low": False,
            "gpio_num": 1,
            "id": 1,
            "kettle_id": None,
            "name": "Heater1",
            "state": False,
        }

    def test_get_list(self, testapp):
        """Test heater list view."""
        testapp.post_json("/devices/Heater/", dict(name="Heater1", gpio_num=1))
        testapp.post_json("/devices/Heater/", dict(name="Heater2", gpio_num=2))
        response = testapp.get("/devices/Heater/")
        assert response.status_int == 200
        assert response.content_type == "application/json"
        assert response.json == [
            {
                "active_low": False,
                "gpio_num": 1,
                "id": 1,
                "kettle_id": None,
                "name": "Heater1",
                "state": False,
            },
            {
                "active_low": False,
                "gpio_num": 2,
                "id": 2,
                "kettle_id": None,
                "name": "Heater2",
                "state": False,
            },
        ]

    # def test_create_method(self):
    #     """Create a heater."""
    #     heater = Heater.create(name="foo", gpio_num=1)

    #     assert "foo" == heater.name
    #     assert 1 == heater.gpio_num
    #     assert heater.state is False
    #     assert Heater.query.get(heater.id) is heater

    # def test_create_method_kwargs(self):
    #     """Create a heater."""
    #     data = {"name": "foo", "gpio_num": 1}
    #     heater = Heater.create(**data)

    #     assert "foo" == heater.name
    #     assert 1 == heater.gpio_num
    #     assert heater.state is False
    #     assert Heater.query.get(heater.id) is heater

    # def test_update_method(self):
    #     """Update a heater."""
    #     heater = Heater.create(name="foo", gpio_num=1)
    #     assert 1 == heater.gpio_num
    #     heater.update(gpio_num=2)
    #     assert 2 == heater.gpio_num

    # def test_turn_on_turn_off(self):
    #     """Test turns on then off."""
    #     heater = Heater.create(name="foo", gpio_num=1)
    #     assert Heater.query.get(heater.id).current_state is False
    #     heater.turn_on()
    #     assert Heater.query.get(heater.id).current_state is True
    #     heater.turn_off()
    #     assert Heater.query.get(heater.id).current_state is False
