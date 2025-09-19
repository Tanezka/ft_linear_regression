import json
import sys

data_file = "data.txt"

# Only protect file handling
try:
    with open("data.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    print("Model is not trained yet. Please train the model first.")
    sys.exit(1)
except PermissionError:
    print("No permission to open the data file.")
    sys.exit(1)
except OSError as e:
    print(f"OS error: {e}")
    sys.exit(1)

# Safe: we have data now
teta0 = data["teta0"]
teta1 = data["teta1"]
mile_mean = data["mile_mean"]
price_mean = data["price_mean"]
mile_std = data["mile_std"]
price_std = data["price_std"]

if teta0 == 0.0 and teta1 == 0.0:
    print("Model is not trained yet. Please train the model first.")
    sys.exit(1)

def estimate_price(x):
    return teta0 + (teta1 * x)

try:
	mile_given = float(input("Give me a mile so I can predict the price:\n"))
except ValueError:
    print("Error: Mile must be a numbe, dummy")
    sys.exit(0)

if (mile_given < 0):
    print("Error: Mile cannot be negative. What are you, a time traveler?")
    sys.exit(0)
normal_mile = (mile_given - mile_mean) / mile_std
predicted_price = (estimate_price(normal_mile) * price_std) + price_mean

if predicted_price <= 0:
    print("That’s a junkie, do not buy it")
else:
    print(f"Predicted price: {predicted_price}")
