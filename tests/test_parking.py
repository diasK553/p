import pytest
from parking_system import Car, Truck, Motorcycle, ParkingLot


def make_lot():
    lot = ParkingLot("Тест", capacity=3)
    lot.register_vehicle(Car("AAA 001", "Тест Пользователь"))
    lot.register_vehicle(Truck("BBB 002", "Компания"))
    lot.register_vehicle(Motorcycle("CCC 003", "Мотоциклист"))
    return lot


def test_register():
    lot = ParkingLot("Тест", 2)
    car = Car("TST 001", "Тестер")
    lot.register_vehicle(car)
    assert lot.get_registry()[0]["plate"] == "TST 001"


def test_double_register():
    lot = ParkingLot("Тест", 2)
    lot.register_vehicle(Car("TST 001", "Тестер"))
    with pytest.raises(ValueError):
        lot.register_vehicle(Car("TST 001", "Другой"))


def test_enter_exit():
    lot = make_lot()
    spot = lot.enter("AAA 001")
    assert spot >= 1
    record = lot.exit_vehicle("AAA 001")
    assert record.vehicle.plate == "AAA 001"
    assert record.cost > 0


def test_enter_unregistered():
    lot = ParkingLot("Тест", 2)
    with pytest.raises(ValueError):
        lot.enter("ZZZ 999")


def test_parking_full():
    lot = ParkingLot("Тест", 1)
    lot.register_vehicle(Car("A 001", "Один"))
    lot.register_vehicle(Car("B 002", "Два"))
    lot.enter("A 001")
    with pytest.raises(ValueError):
        lot.enter("B 002")


def test_rates():
    assert Car("X", "X").rate == 500.0
    assert Truck("X", "X").rate == 1200.0
    assert Motorcycle("X", "X").rate == 250.0


def test_search():
    lot = make_lot()
    lot.enter("AAA 001")
    result = lot.search("AAA 001")
    assert result["status"] == "on_parking"
    result2 = lot.search("BBB 002")
    assert result2["status"] == "registered"
    result3 = lot.search("ZZZ 999")
    assert result3["status"] == "not_found"
