# import package
from fastapi import FastAPI, HTTPException, Header
import pandas as pd

password = "secret123"
# create FastAPI object
app = FastAPI()

# endpoint -> alamat tertentu yang bisa diakses oleh client
# create endpoint untuk mendapatkan data di halaman awal/utam

@app.get("/home")
def getData(): # function handle -> untuk menghandle request dari endpoint
    return{
        "message": "hello world !?" 
    }

# endpoint untuk ngambil data dari csv
@app.get("/data")
def getCsv():
   # 1. baca data dari csv
   df = pd.read_csv('data.csv')

   # 2. tampilkan response berupa data csv menjadi json.
   # untuk mengubah dataframe menjadi json menggunakan to_dict() ubah menjadi dictionary
   return df.to_dict(orient="records")

@app.get("/data/{name}")
def getDataByName(name: str):
    # 1. baca data dari csv
    df = pd.read_csv('data.csv')
    
    # 2. filter data by name
    result = df[df['name'] == name]

    # check apakah hasil filter > 0 (ada)
    if len(result) > 0:
        # 3. tampilkan response berupa data csv menjadi json
        return result.to_dict(orient="records")
    else:
        # tampilkan pesan error
        # menggunakan raise yang memanggil object HTTPException

        # tampilkan pesan error
        raise HTTPException(status_code = 404, detail = "data " + name + " tidak ditemukan")

# @app.post("/addData")
# def addData(added_item: dict):
#     # 1. baca data dari csv
#         # 1. baca data dari csv
#         df = pd.read_csv('data.csv')

#     # 2. delete nama by filter
#         result = df.loc[len(df)] = added_item

#     # 3. replace csv existing -> data yang difilter akan hilang
#         result.to_csv('data.csv',index=False)

#         return result.to_dict(orient="records")




@app.delete("/data/{name}")
def deleteDataByName(name: str, api_key: str = Header(None)):
    # check auth
    if api_key != None and api_key == password:
    # 1. baca data dari csv
        df = pd.read_csv('data.csv')

    # 2. delete nama by filter
        result = df[~(df['name'] == name)]

    # 3. replace csv existing -> data yang difilter akan hilang
        result.to_csv('data.csv',index=False)

        return result.to_dict(orient="records")
    else:
        raise HTTPException(status_code = 403, detail= "Password salah")
    