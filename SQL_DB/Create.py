import pandas as pd
import json
import sqlite3
# Open JSON data

def Load():

  with open("datasets.json") as f:
      data = json.load(f)

  # Create A DataFrame From the JSON Data
  df = pd.DataFrame(data)

  conn=sqlite3.connet("data.bd")
  c=conn.cursor()

  df.to_sql("data",conn)

