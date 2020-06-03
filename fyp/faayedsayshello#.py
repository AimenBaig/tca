from sklearn.naive_bayes import GaussianNB
import pandas as pd
train = pd.read_csv('C:/Users/apex/PycharmProjects/tca/trained_data.csv', sep=',', engine='python')
test = pd.read_csv('C:/Users/apex/PycharmProjects/tca/testing_data.csv', sep=',', engine='python')



X_train = train.iloc[:,1:2]
Y_train = train.iloc[:,0:1]
X_test = train.iloc[:,1:2]

bias = GaussianNB()
bias.fit(X_train,Y_train)

y_predict = bias.predict(X_test)

print(y_predict)