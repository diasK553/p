"""
Система управления парковкой (Parking Management System)
=========================================================
Демонстрирует: инкапсуляцию, наследование, полиморфизм, абстракцию
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class ParkingEntity(ABC):
    @abstractmethod
    def get_info(self) -> str:
        pass

    @abstractmethod
    def get_type(self) -> str:
        pass


class Vehicle(ParkingEntity):
    _BASE_RATE: float = 500.0

    def __init__(self, plate: str, owner: str):
        self.__plate = plate.upper().strip()
        self.__owner = owner.strip()
        self._rate = self._BASE_RATE

    @property
    def plate(self) -> str:
        return self.__plate

    @property
    def owner(self) -> str:
        return self.__owner

    @owner.setter
    def owner(self, value: str):
        if not value.strip():
            raise ValueError("Имя владельца не может быть пустым.")
        self.__owner = value.strip()

    @property
    def rate(self) -> float:
        return self._rate

    def get_info(self) -> str:
        return f"{self.get_type()} | Номер: {self.__plate} | Владелец: {self.__owner} | Тариф: {self._rate:.0f} ₸/ч"

    def get_type(self) -> str:
        return "Транспортное средство"

    def to_dict(self) -> dict:
        return {
            "plate": self.plate,
            "owner": self.owner,
            "type": self.get_type(),
            "rate": self.rate,
        }

    def __repr__(self):
        return f"<{self.get_type()} {self.__plate}>"


class Car(Vehicle):
    _BASE_RATE = 500.0

    def __init__(self, plate: str, owner: str):
        super().__init__(plate, owner)
        self._rate = Car._BASE_RATE

    def get_type(self) -> str:
        return "Легковой автомобиль"


class Truck(Vehicle):
    _BASE_RATE = 1200.0

    def __init__(self, plate: str, owner: str):
        super().__init__(plate, owner)
        self._rate = Truck._BASE_RATE

    def get_type(self) -> str:
        return "Грузовой автомобиль"


class Motorcycle(Vehicle):
    _BASE_RATE = 250.0

    def __init__(self, plate: str, owner: str):
        super().__init__(plate, owner)
        self._rate = Motorcycle._BASE_RATE

    def get_type(self) -> str:
        return "Мотоцикл"


class ParkingSpot:
    def __init__(self, spot_id: int):
        self.__spot_id = spot_id
        self.__vehicle: Optional[Vehicle] = None
        self.__entry_time: Optional[datetime] = None

    @property
    def spot_id(self) -> int:
        return self.__spot_id

    @property
    def is_occupied(self) -> bool:
        return self.__vehicle is not None

    @property
    def vehicle(self) -> Optional[Vehicle]:
        return self.__vehicle

    @property
    def entry_time(self) -> Optional[datetime]:
        return self.__entry_time

    def park(self, vehicle: Vehicle) -> None:
        if self.is_occupied:
            raise ValueError(f"Место #{self.__spot_id} уже занято.")
        self.__vehicle = vehicle
        self.__entry_time = datetime.now()

    def release(self):
        if not self.is_occupied:
            raise ValueError(f"Место #{self.__spot_id} уже свободно.")
        v, t = self.__vehicle, self.__entry_time
        self.__vehicle = None
        self.__entry_time = None
        return v, t

    def to_dict(self) -> dict:
        d = {"spot_id": self.__spot_id, "is_occupied": self.is_occupied}
        if self.is_occupied:
            elapsed = (datetime.now() - self.__entry_time).total_seconds() / 60
            d["vehicle"] = self.__vehicle.to_dict()
            d["entry_time"] = self.__entry_time.strftime("%H:%M:%S")
            d["elapsed_min"] = round(elapsed, 1)
        return d


class ParkingRecord:
    def __init__(self, vehicle: Vehicle, spot_id: int, entry: datetime, exit_: datetime):
        self.vehicle = vehicle
        self.spot_id = spot_id
        self.entry = entry
        self.exit = exit_
        self.duration_hours = (exit_ - entry).total_seconds() / 3600
        self.cost = max(self.duration_hours, 1 / 60) * vehicle.rate

    def to_dict(self) -> dict:
        return {
            "plate": self.vehicle.plate,
            "owner": self.vehicle.owner,
            "type": self.vehicle.get_type(),
            "spot_id": self.spot_id,
            "entry": self.entry.strftime("%H:%M:%S"),
            "exit": self.exit.strftime("%H:%M:%S"),
            "duration_min": round(self.duration_hours * 60, 1),
            "cost": round(self.cost, 2),
        }


class ParkingLot:
    def __init__(self, name: str, capacity: int):
        self.__name = name
        self.__spots: dict[int, ParkingSpot] = {
            i: ParkingSpot(i) for i in range(1, capacity + 1)
        }
        self.__registry: dict[str, Vehicle] = {}
        self.__history: list[ParkingRecord] = []

    @property
    def name(self) -> str:
        return self.__name

    def register_vehicle(self, vehicle: Vehicle) -> None:
        if vehicle.plate in self.__registry:
            raise ValueError(f"Автомобиль {vehicle.plate} уже зарегистрирован.")
        self.__registry[vehicle.plate] = vehicle

    def enter(self, plate: str) -> int:
        plate = plate.upper().strip()
        if plate not in self.__registry:
            raise ValueError(f"Автомобиль {plate} не зарегистрирован.")
        for spot in self.__spots.values():
            if spot.is_occupied and spot.vehicle.plate == plate:
                raise ValueError(f"Автомобиль {plate} уже на парковке (место #{spot.spot_id}).")
        spot = self.__find_free_spot()
        spot.park(self.__registry[plate])
        return spot.spot_id

    def exit_vehicle(self, plate: str) -> ParkingRecord:
        plate = plate.upper().strip()
        spot = self.__find_spot_by_plate(plate)
        vehicle, entry_time = spot.release()
        record = ParkingRecord(vehicle, spot.spot_id, entry_time, datetime.now())
        self.__history.append(record)
        return record

    def search(self, plate: str) -> dict:
        plate = plate.upper().strip()
        for spot in self.__spots.values():
            if spot.is_occupied and spot.vehicle.plate == plate:
                elapsed = (datetime.now() - spot.entry_time).total_seconds() / 60
                return {"status": "on_parking", "spot_id": spot.spot_id, "elapsed_min": round(elapsed, 1)}
        if plate in self.__registry:
            return {"status": "registered"}
        return {"status": "not_found"}

    def get_status(self) -> dict:
        spots = [s.to_dict() for s in self.__spots.values()]
        occupied = [s for s in spots if s["is_occupied"]]
        free = [s for s in spots if not s["is_occupied"]]
        return {
            "name": self.__name,
            "total": len(self.__spots),
            "occupied_count": len(occupied),
            "free_count": len(free),
            "spots": spots,
        }

    def get_history(self) -> list:
        return [r.to_dict() for r in self.__history]

    def get_registry(self) -> list:
        return [v.to_dict() for v in self.__registry.values()]

    def __find_free_spot(self) -> ParkingSpot:
        for spot in self.__spots.values():
            if not spot.is_occupied:
                return spot
        raise ValueError("Нет свободных мест на парковке!")

    def __find_spot_by_plate(self, plate: str) -> ParkingSpot:
        for spot in self.__spots.values():
            if spot.is_occupied and spot.vehicle.plate == plate:
                return spot
        raise ValueError(f"Автомобиль {plate} не найден на парковке.")


VEHICLE_TYPES = {"car": Car, "truck": Truck, "motorcycle": Motorcycle}

# Глобальный экземпляр парковки
lot = ParkingLot("Центральная", capacity=10)
