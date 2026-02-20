import requests
import pandas as pd
from datetime import datetime
from database import insert_crypto_data

def fetch_and_transform_data():
    print("Data is being retrieved from the API.")

    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    try:
        response=requests.get(url)
        response.raise_for_status()
        raw_data=response.json()
        print("Data retrieved successfully!")

    except Exception as e:
        print(f"An error occurred while retrieving data:{e}")
        return None
    
    current_time=datetime.now()

    transform_data=[
        {
            'coin_name':'bitcoin',
            'price_usd':raw_data['bitcoin']['usd'],
            'fetched_at':current_time
        },
        {
            'coin_name':'ethereum',
            'price_usd':raw_data['ethereum']['usd'],
            'fetched_at':current_time
        }
    ]

    df=pd.DataFrame(transform_data)
    return df

if __name__=="__main__":
    
    df_result=fetch_and_transform_data()

    if df_result is not None:
        print("\nProcessed Data Table (DataFrame):")
        print(df_result)

        print("\nUploading to the cloud...")
        insert_crypto_data(df_result)