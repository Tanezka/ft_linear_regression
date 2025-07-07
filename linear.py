import csv
import matplotlib.pyplot as plt
import os

DATA_FILE = 'data.csv'
data_pair = []


teta0 = 0.0
teta1 = 0.0

with open(DATA_FILE, 'r') as file:
	reader = csv.reader(file)
	reader = list(reader)
	reader = reader[1:]  # Skip header if present
	for line in reader:
		data_pair.append((float(line[0]), float(line[1])))
print(len(data_pair))

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
		# print(f"Iteration {i+1}: teta0 = {teta0}, teta1 = {teta1}, error = {error/len(normalized_data_pair)}")

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
# Prepare data for graphing
km_values = [x[0] for x in data_pair]
actual_prices = [x[1] for x in data_pair]

# Generate predictions from the model
predicted_prices = []
for km in km_values:
    norm_km = (km - mile_mean) / mile_std
    norm_pred = estimate_price(norm_km)
    denorm_pred = norm_pred * price_std + price_mean
    predicted_prices.append(denorm_pred)

# Plot
plt.figure(figsize=(10, 6))
plt.scatter(km_values, actual_prices, color='blue', label='Actual Prices')
plt.plot(km_values, predicted_prices, color='red', label='Predicted Prices (Linear Regression)')
plt.xlabel('Kilometers (km)')
plt.ylabel('Price (TL)')
plt.title('Car Price Prediction')
plt.legend()
plt.grid(True)
plt.show()
mileGiven = float(input("Give me a mile so i can predit the price:\n"))
normal_mileGiven = (mileGiven - mile_mean) / mile_std
while mileGiven >= 0:
	print(f"Predicted price: {(estimate_price(normal_mileGiven) * price_std) + price_mean}\n")
	mileGiven = float(input("Give me a mile so i can predit the price:"))
	normal_mileGiven = (mileGiven - mile_mean) / mile_std
