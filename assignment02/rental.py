"""
rental.py

Classes for the Siam University campus vehicle-rental desk.

Contains:
    Vehicle      - base class for anything that can be rented out
    Renter       - a member who rents vehicles (data is validated)
    ElectricCar  - a Vehicle with a battery size (inherits Vehicle)
    Motorbike    - a Vehicle with an engine size (inherits Vehicle)
"""


class Vehicle:
    """A generic rentable vehicle (car, bike, etc.)."""

    def __init__(self, make, model, plate):
        self.make = make
        self.model = model
        self.plate = plate
        self.is_rented = False

    def rent(self):
        """Mark this vehicle as rented out."""
        self.is_rented = True

    def return_vehicle(self):
        """Mark this vehicle as returned / available again."""
        self.is_rented = False

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return f"{self.make} {self.model} ({self.plate}) [{status}]"


class Renter:
    """
    A person who rents vehicles.

    name must not be empty, and license_no must be a positive number.
    Both are enforced through properties, so the check runs every time
    the value is set - including when the object is first created.
    """

    def __init__(self, name, license_no):
        self.name = name
        self.license_no = license_no
        self.rented = []

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if value is None or not str(value).strip():
            raise ValueError("Renter name must not be empty.")
        self._name = value

    @property
    def license_no(self):
        return self._license_no

    @license_no.setter
    def license_no(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Renter license_no must be a positive number.")
        self._license_no = value

    def __str__(self):
        return f"{self.name} (licence #{self.license_no})"


class ElectricCar(Vehicle):
    """An electric car - a Vehicle plus a battery size in kWh."""

    def __init__(self, make, model, plate, battery_kwh):
        super().__init__(make, model, plate)
        self.battery_kwh = battery_kwh

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return (
            f"Electric car: {self.make} {self.model} ({self.plate}) "
            f"- {self.battery_kwh} kWh battery [{status}]"
        )


class Motorbike(Vehicle):
    """A motorbike - a Vehicle plus an engine size in cc."""

    def __init__(self, make, model, plate, engine_cc):
        super().__init__(make, model, plate)
        self.engine_cc = engine_cc

    def __str__(self):
        status = "rented" if self.is_rented else "available"
        return (
            f"Motorbike: {self.make} {self.model} ({self.plate}) "
            f"- {self.engine_cc}cc engine [{status}]"
        )
