import numpy as np
import pandas as pd
import pandas_datareader.data as web
import datetime
import math
from sklearn import preprocessing
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split


def predict(stock, start, end, forecast_out=7):
    try:
        df = web.DataReader(stock, 'yahoo', start=start, end=end)
    except:
        print("Some error, try another date or stock.")
        exit

    dfreg = df.loc[:,['Adj Close','Volume']]
    dfreg['HL_PCT'] = (df['High'] - df['Low']) / df['Close'] * 100.0
    dfreg['PCT_change'] = (df['Close'] - df['Open']) / df['Open'] * 100.0

    dfreg = dfreg.dropna()

    dfreg['label'] = dfreg['Adj Close'].shift(-forecast_out)
    X = np.array(dfreg.drop(['label'],1))
    X = preprocessing.scale(X)

    X_lately = X[-forecast_out:]
    X = X[:-forecast_out]

    y = np.array(dfreg['label'])
    y = y[:-forecast_out]

    X_train = X
    y_train = y

    #X_train, X_test, y_train, y_test = train_test_split(X_train,y_train, test_size = 0.2, random_state = 43)

    clfreg = LinearRegression()
    clfreg.fit(X_train, y_train)

    # Quadratic Regression 2
    clfpoly2 = make_pipeline(PolynomialFeatures(2), Ridge())
    clfpoly2.fit(X_train, y_train)

    # Quadratic Regression 3
    clfpoly3 = make_pipeline(PolynomialFeatures(3), Ridge())
    clfpoly3.fit(X_train, y_train)

    clfknn = KNeighborsRegressor(n_neighbors=1)
    clfknn.fit(X_train,y_train)

    f_reg = clfreg.predict(X_lately)
    f_poly2 = clfpoly2.predict(X_lately)
    f_poly3 = clfpoly3.predict(X_lately)
    f_knn = clfknn.predict(X_lately)

    dfreg['F_reg'] = np.nan
    dfreg['F_poly2'] = np.nan
    dfreg['F_poly3'] = np.nan
    dfreg['F_knn'] = np.nan

    last_date = dfreg.iloc[-1].name

    for i, k in enumerate(f_reg):
        next_date = last_date + datetime.timedelta(days=i+1)
        data = {'F_reg': k, 'F_poly2': f_poly2[i], 'F_poly3': f_poly3[i], 'F_knn': f_knn[i]}
        dfreg = dfreg.append(pd.DataFrame(data, index=[next_date]))

    return (dfreg, f_reg, f_poly2, f_poly3, f_knn)

if __name__ == '__main__':
    a = predict('BBCA.JK', datetime.datetime(2018,1,1), datetime.datetime.now())
    print(a)


