import os
import io
import requests
import psycopg2 as pg
import pandas as pd
from tools import JsonObject
from sqlalchemy import create_engine


engine = create_engine(os.environ['DB_URL_MENTOR'])

print("Starting...")
sql = "select identity_number from metadata_borrower where length(identity_number) = 16;"
df = pd.read_sql(sql, engine)
print("Success to get Mekar borrowers!")
identities = df["identity_number"].tolist()

counter = 0
result = pd.DataFrame()
for identity in identities:
    print(f"Getting credit history for borrower with identity {identity}...")

    response = requests.get(
        f"{os.environ['FDC_API_URL']}?id={identity}&reason=2",
        auth=(os.environ['FDC_USER'], os.environ['FDC_PASS'])
    )
    if response.ok:
        response = JsonObject(response.text)
        if len(response.pinjaman) > 0:
            print(f"Founded {len(response.pinjaman)} credit history, running next step...")
            df = pd.DataFrame(response.pinjaman)
            result = result.append(df)
            counter += 1
    else:
        print(f"Error {response.status_code}: {response.reason}, on identity: {identity}.")
        continue

if len(result) > 0:
    result.reset_index()
    result.to_sql("borrowers_history", engine, if_exists="replace", index=False)
    print(f"Success to get {counter} borrower's credit history.")
else:
    print("No borrower's credit history generated.")
