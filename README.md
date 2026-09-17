# Campus Vehicle Rental (OOP demo)

A small Python program for the Siam University vehicle-rental desk, built to
practise classes/objects, encapsulation, and inheritance/polymorphism.

## Files

- `rental.py` — all classes: `Vehicle`, `Renter`, `ElectricCar`, `Motorbike`
- `main.py` — demo script, run with `python main.py`
- `test_rental.py` — pytest suite, run with `pytest`

## Design

- **`Vehicle`** holds `make`, `model`, `plate`, `is_rented`, with `rent()` /
  `return_vehicle()` methods and a one-line `__str__`.
- **`Renter`** holds `name` and `license_no` behind `@property` setters, so
  an empty name or a non-positive licence number always raises `ValueError`
  — whether set at creation or changed later. `rented` starts as an empty
  list.
- **`ElectricCar`** and **`Motorbike`** each inherit from `Vehicle`, call
  `super().__init__(...)`, add one extra attribute (`battery_kwh` /
  `engine_cc`), and override `__str__` with their own format. Because they
  inherit from `Vehicle`, `isinstance(x, Vehicle)` is `True` for both, and
  they can still `rent()` / `return_vehicle()` like any vehicle.

## Run it

```bash
python main.py
pytest
```
