
from datetime import datetime, timedelta
from math import ceil

# Pricing constants
HOURLY_RATE = 5
DAILY_RATE  = 20
WEEKLY_RATE = 60


class CarRental:
    """Manage car stock and rental operations."""

    def __init__(self, stock: int = 0) -> None:
        self.stock = int(stock)

    def now(self) -> datetime:
        """Return current timestamp (used for rentals and billing)."""
        return datetime.now()

    def display_stock(self) -> int:
        """Show and return the number of available cars."""
        if self.stock > 0:
            print(f"Available cars: {self.stock}")
        else:
            print("Sorry, no cars available at the moment.")
        return self.stock

    # ---------- Rental methods ----------
    def _validate_and_reserve(self, n: int) -> bool:
        """Validate request and reserve stock if valid."""
        # More strict: disallow booleans (since True/False are subclasses of int)
        if type(n) is not int:
            print("Please enter an integer number of cars.")
            return False
        if n <= 0:
            print("Number of cars should be at least 1.")
            return False
        if n > self.stock:
            print(f"Only {self.stock} car(s) available right now.")
            return False
        # Passed validation → reduce stock
        self.stock -= n
        return True

    def rent_hourly(self, n: int):
        """Rent cars on an hourly basis. Return rental info dict or None."""
        if not self._validate_and_reserve(n):
            return None
        rental_info = {"rental_time": self.now(), "basis": "hourly", "num_cars": n}
        print(f"You rented {n} car(s) on an hourly basis.")
        return rental_info

    def rent_daily(self, n: int):
        """Rent cars on a daily basis. Return rental info dict or None."""
        if not self._validate_and_reserve(n):
            return None
        rental_info = {"rental_time": self.now(), "basis": "daily", "num_cars": n}
        print(f"You rented {n} car(s) on a daily basis.")
        return rental_info

    def rent_weekly(self, n: int):
        """Rent cars on a weekly basis. Return rental info dict or None."""
        if not self._validate_and_reserve(n):
            return None
        rental_info = {"rental_time": self.now(), "basis": "weekly", "num_cars": n}
        print(f"You rented {n} car(s) on a weekly basis.")
        return rental_info

    # ---------- Return cars ----------
    def return_cars(self, rental_info=None, *, rental_time=None, basis=None, num_cars=None) -> float:
        """
        Return cars and generate a bill.

        You can pass either:
          - rental_info dict (with keys: rental_time, basis, num_cars), OR
          - separate keyword args: rental_time=..., basis=..., num_cars=...
        """
        # ---- Parse inputs ----
        if rental_info is not None:
            rental_time = rental_info.get("rental_time")
            basis = rental_info.get("basis")
            num_cars = rental_info.get("num_cars")

        if not rental_time or not basis or not num_cars:
            print("Invalid rental info.")
            return 0.0

        # ---- Compute elapsed time ----
        end_time = self.now()
        delta = end_time - rental_time  # datetime.timedelta

        # ---- Billable units (ceil) & rate ----
        if basis == "hourly":
            billable_units = max(1, ceil(delta.total_seconds() / 3600))
            rate = HOURLY_RATE
        elif basis == "daily":
            billable_units = max(1, ceil(delta.total_seconds() / 86400))
            rate = DAILY_RATE
        elif basis == "weekly":
            billable_units = max(1, ceil(delta.total_seconds() / (7 * 86400)))
            rate = WEEKLY_RATE
        else:
            print("Unknown rental basis.")
            return 0.0

        # ---- Compute bill & restock ----
        bill = billable_units * rate * num_cars
        self.stock += num_cars

        print(f"Bill for {num_cars} car(s) on a {basis} basis ({billable_units} unit(s)): ${bill}")
        return bill


class Customer:
    """Customer entity to interact with the CarRental shop."""

    def __init__(self) -> None:
        self.rental_info = None

    def request_car(self, rental_type: str, num_cars: int, shop: CarRental):
        """Request cars from the rental shop."""
        if rental_type == "hourly":
            self.rental_info = shop.rent_hourly(num_cars)
        elif rental_type == "daily":
            self.rental_info = shop.rent_daily(num_cars)
        elif rental_type == "weekly":
            self.rental_info = shop.rent_weekly(num_cars)
        else:
            print("Invalid rental type. Choose hourly/daily/weekly.")

    def return_car(self, shop: CarRental):
        """Return cars to the rental shop."""
        if self.rental_info is None:
            print("No cars to return.")
            return 0.0
        bill = shop.return_cars(self.rental_info)
        self.rental_info = None
        return bill
