import json
import sys
import csv
import os

DATA_FILE = 'data.csv'
data_pair = []


teta0 = 0.0
teta1 = 0.0
if not os.path.exists(DATA_FILE):
    print(f"Error: '{DATA_FILE}' not found.")
    sys.exit(1)

try:
    with open(DATA_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        reader = list(reader)
        reader = reader[1:]
        for line in reader:
            try:
                data_pair.append((float(line[0]), float(line[1])))
            except (ValueError, IndexError):
                continue
except PermissionError:
    print(f"Error: No permission to read '{DATA_FILE}'.")
    sys.exit(1)
except OSError as e:
    print(f"Error opening '{DATA_FILE}': {e}")
    sys.exit(1)

if len(data_pair) < 2:
	print("Error: Not enough valid data in 'data.csv'.")
	sys.exit(1)

def estimate_price(x):
	global teta0, teta1
	est_price = teta0 + (teta1 * x)
	return est_price

def	training_loop():
	global teta0, teta1
	learning_rate = 0.01
	for i in range(1000):
		err = 0.0
		error = 0.0
		error_m = 0.0

		for mile, price in normalized_data_pair:
			est_price = estimate_price(mile)
			err = (est_price - price)
			error += err
			error_m += err * mile

		
		tempteta0 = learning_rate * ((1/len(normalized_data_pair)) *  error)
		tempteta1 = learning_rate * ((1/len(normalized_data_pair)) *  error_m)
		
		teta0 -= tempteta0
		teta1 -= tempteta1

def mean(values):
    return sum(values) / len(values)

def standard_deviation(values):
    mu = mean(values)
    variance = sum((x - mu) ** 2 for x in values) / len(values)
    return variance ** 0.5

def normalize_data(data_pair):
	data = []
	global mile_mean, price_mean, mile_std, price_std	
	for mile, price in data_pair:
		normalized_mile = (mile - mile_mean) / mile_std
		normalized_price = (price - price_mean) / price_std
		
		data.append((normalized_mile, normalized_price))
	return data
	
mile_mean = mean([x[0] for x in data_pair])
price_mean = mean([x[1] for x in data_pair])
mile_std = standard_deviation([x[0] for x in data_pair])
price_std = standard_deviation([x[1] for x in data_pair])
normalized_data_pair = normalize_data(data_pair)
training_loop()

data={
	"teta0":teta0,
	"teta1":teta1,
	"mile_mean":mile_mean,
	"price_mean":price_mean,
	"mile_std":mile_std,
	"price_std":price_std
}

with open("data.json", "w") as f:
        json.dump(data, f)