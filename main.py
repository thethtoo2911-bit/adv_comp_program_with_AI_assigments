"""
main.py

Short demo program for the campus vehicle-rental desk.
Run with:  python main.py
"""

from rental import Vehicle, Renter, ElectricCar, Motorbike


def main():
    print("=== 1. Create vehicles and a renter ===")
    car = Vehicle("Toyota", "Yaris", "1AB234")
    ecar = ElectricCar("Tesla", "Model 3", "2EV567", battery_kwh=75)
    bike = Motorbike("Honda", "Wave", "3MB890", engine_cc=125)
    renter = Renter("Somchai", 998877)

    print(car)
    print(ecar)
    print(bike)
    print(renter)

    print("\n=== 2. Rent and return a vehicle ===")
    print("Before renting:", car)
    car.rent()
    renter.rented.append(car)
    print("After renting: ", car)
    car.return_vehicle()
    print("After return:  ", car)

    print("\n=== 3. Invalid renter data raises ValueError ===")
    try:
        bad_renter = Renter("", 12345)
    except ValueError as e:
        print("Caught expected error (empty name):", e)

    try:
        bad_renter = Renter("Nok", -5)
    except ValueError as e:
        print("Caught expected error (bad licence):", e)

    print("\n=== 4. Mixed list of vehicles - polymorphism ===")
    fleet = [
        Vehicle("Mazda", "2", "4CD111"),
        ElectricCar("Nissan", "Leaf", "5EV222", battery_kwh=40),
        Motorbike("Yamaha", "Fino", "6MB333", engine_cc=115),
    ]
    for v in fleet:
        print(v)
        print("  isinstance of Vehicle:", isinstance(v, Vehicle))


if __name__ == "__main__":
    main()
