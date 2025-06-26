import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import pickle
house_price = pd.read_csv('Housing.csv')
print(house_price.head())

print(house_price.tail())

print('Rows and columns of the Dataset : ', house_price.shape)
print(house_price.info())
print(house_price.columns)
print(house_price.isnull().sum())

print(house_price.head())

categorical_col = ['mainroad', 'guestroom', 'basement', 'hotwaterheating', 'airconditioning', 'prefarea']

print(house_price[categorical_col])


def binary_map(x):

    return x.map({'yes': 1, 'no': 0})

house_price[categorical_col] = house_price[categorical_col].apply(binary_map)
print(house_price[categorical_col])

print(house_price.head())

dummy_col = pd.get_dummies(house_price['furnishingstatus'])
print(dummy_col.head())

dummy_col = pd.get_dummies(house_price['furnishingstatus'], drop_first = True)
print(dummy_col.head())


house_price = pd.concat([house_price, dummy_col], axis = 1)
print(house_price.head())


house_price.drop(['furnishingstatus'], axis = 1, inplace = True)
print(house_price.head())


print(house_price.columns)

np.random.seed(0)
hp_train, hp_test = train_test_split(house_price, train_size = 0.7, test_size = 0.3, random_state = 100)

print(hp_train.head())
print(hp_train.shape)
print(hp_test.shape)

scaler = MinMaxScaler()


col_scale = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking', 'price']
hp_train[col_scale] = scaler.fit_transform(hp_train[col_scale])

y_train = hp_train.pop('price')
x_train = hp_train

regression = RandomForestRegressor()

regression.fit(x_train, y_train)

score = regression.score(x_train, y_train)
print("Regression score is ", score)

col_scale = ['area', 'bedrooms', 'bathrooms', 'stories', 'parking', 'price']

hp_test[col_scale] = scaler.fit_transform(hp_test[col_scale])

y_test = hp_test.pop('price')
x_test = hp_test

prediction = regression.predict(x_test)

r2 = r2_score(y_test, prediction)

print(" R2 score is", r2)

filename = 'prediction-rfc-model.pkl'
pickle.dump(regression, open(filename, 'wb'))

y_test.shape
y_test_metrics = y_test.values.reshape(-1,1)

data_fram = pd.DataFrame({'actual ':y_test_metrics.flatten(), 'predicted ': prediction.flatten()})
print(data_fram.head(10))

# Creating a new figure
fig = plt.figure()

# Scatter plot of actual verses predicted values
plt.scatter(y_test, prediction, c="green", s=50, marker="*")

# Set the title and labels for the plot
plt.title('Actual vs Prediction')
plt.xlabel('Actual ', fontsize = 10)
plt.ylabel('Predicted ', fontsize = 10)
plt.show()

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(y_test, prediction)
print(" Mean Squared Error : ", mse)