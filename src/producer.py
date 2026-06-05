from kafka import KafkaProducer
import pandas as pd
import json
import time
import random 

producer =  KafkaProducer(
    bootstrap_servers=['localhost:19092'],
    value_serializer= lambda v: json.dumps(v).encode('utf-8')
)

df = pd.read_csv('../data/creditcard.csv')

print("streaming transction to Redpanda..")

while True:
    row = df.sample(1).iloc[0]
    transaction = row.drop('Class').to_dict()

    producer.send('transactions', transaction)
    print(f"send transaction - Amount: ${row['Amount']:.2f}")

    time.sleep(1)

