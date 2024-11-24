import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
import numpy as np
from sklearn.neighbors import KNeighborsRegressor


df = pd.read_csv('data.csv')

df.drop('name', inplace=True, axis=1)

df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

df.dropna(subset=['rating'], inplace=True)

df = df.replace(0, None).dropna()

df.drop_duplicates(inplace=True)

label_encoder = LabelEncoder()
df['gender'] = label_encoder.fit_transform(df['gender'])
df['country'] = label_encoder.fit_transform(df['country'])

X = df.drop(columns=['rating'])
y = df['rating']

xTrain, xTest, yTrain, yTest = train_test_split(X, y, test_size=0.3)

model =  KNeighborsRegressor(n_neighbors=4) 

model.fit(xTrain, yTrain)

predictions = model.predict(xTest)

country_code = label_encoder.transform(['LBN'])[0]
new_sample = np.array([[30, 1, country_code]])

print(model.predict(new_sample))

mse = mean_squared_error(yTest, predictions)
r2 = r2_score(yTest, predictions)

print("Mean Squared Error:", mse)
print("R^2 Score:", r2)

plt.plot(yTest, predictions, 'o')
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.title('True vs Predicted Values')
plt.show()
