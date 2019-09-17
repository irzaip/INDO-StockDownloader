from flask import Flask, jsonify, Response
import pandas as pd
import glob


app = Flask(__name__)

fl = glob.glob('./list/*.csv')
df = pd.DataFrame()
for i in fl:
    df = df.append(pd.read_csv(i))

df = df.reset_index()
df = df[['Kode','Nama']]
stockList = df.to_json(orient='index')

@app.route('/')
def jsonstock():
    return (Response(stockList,content_type='application/json'))

if __name__ == '__main__':
    app.run()