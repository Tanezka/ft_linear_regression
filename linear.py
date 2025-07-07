import csv
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
	learning_rate = 0.0000000000001
	for i in range(100000):
		err = 0.0
		error = 0.0
		error_m = 0.0

		for mile, price in data_pair:
			est_price = estimate_price(mile)
			err = (est_price - price)
			error += err
			error_m += err * mile

		
		tempteta0 = learning_rate * ((1/len(data_pair)) *  error)
		tempteta1 = learning_rate * ((1/len(data_pair)) *  error_m)
		
		teta0 -= tempteta0
		teta1 -= tempteta1
		print(f"Iteration {i+1}: teta0 = {teta0}, teta1 = {teta1}, error = {error/len(data_pair)}")

training_loop()
mileGiven = float(input("Give me a mile so i can predit the price:\n"))
while mileGiven >= 0:
	print(f"Predicted price: {estimate_price(mileGiven)}\n")
	mileGiven = float(input("Give me a mile so i can predit the price:"))