# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest

from brewpi.heater.models import Heater
from brewpi.user.models import Role, User

from .factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User("foo", "foo@bar.com")
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    def test_check_password(self):
        """Check password."""
        user = User.create(username="foo", email="foo@bar.com", password="foobarbaz123")
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles


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
        print(Heater.query.get(heater.id))

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

    def test_turn_on_off(self):
        """Test null password."""
        heater = Heater.create(name="foo", gpio_num=1)
        assert heater.current_state is False
        heater.turn_on()
        assert heater.current_state is True
        heater.turn_off()
        assert heater.current_state is False

    # def test_factory(self, db):
    #     """Test user factory."""
    #     user = UserFactory(password="myprecious")
    #     db.session.commit()
    #     assert bool(user.username)
    #     assert bool(user.email)
    #     assert bool(user.created_at)
    #     assert user.is_admin is False
    #     assert user.active is True
    #     assert user.check_password("myprecious")

    # def test_check_password(self):
    #     """Check password."""
    #     user = User.create(username="foo", email="foo@bar.com", password="foobarbaz123")
    #     assert user.check_password("foobarbaz123") is True
    #     assert user.check_password("barfoobaz") is False

    # def test_full_name(self):
    #     """User full name."""
    #     user = UserFactory(first_name="Foo", last_name="Bar")
    #     assert user.full_name == "Foo Bar"

    # def test_roles(self):
    #     """Add a role to a user."""
    #     role = Role(name="admin")
    #     role.save()
    #     user = UserFactory()
    #     user.roles.append(role)
    #     user.save()
    #     assert role in user.roles
