import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

url:str=os.environ.get("SUPABASE_URL")
key:str=os.environ.get("SUPABASE_KEY")

supabase: Client=create_client(url,key)

def clean_old_records():
    
    threshold_date=datetime.now()-timedelta(days=2)

    try:
        supabase.table("crypto_logs").delete().lt("fetched_at",threshold_date.isoformat()).execute
        print(f"Old data deleted successfully (prior to: {threshold_date.strftime('%Y-%m-%d %H:%M')}).")
    
    except Exception as e:
        print(f"Cleanup process failed. Error: {e}")

def insert_crypto_data(df):

    df['fetched_at'] = df['fetched_at'].astype(str)
    records=df.to_dict(orient="records")

    try:
        supabase.table("crypto_logs").insert(records).execute()
        print("Data successfully saved to Supabase.")

        clean_old_records()
        return True
    
    except Exception as e:
        print(f"Database save operation failed. Error: {e}")
        return False