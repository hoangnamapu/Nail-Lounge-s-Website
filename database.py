#import streamlit as st
from supabase import Client, Client
from datetime import datetime
import toml

#@st.cache_resource
def init_connection():
    path = ".streamlit/secrets.toml"
    with open(path, "r") as f:
        data = toml.load(f)
    url = data["SUPABASE_URL"]
    key = data["SUPABASE_KEY"]
    Check_in(url,key)
    return Check_in(url,key)

supabase = init_connection()

def get_client(phone):
    conn = init_connection()
    try:
        data, _ = conn.table("Client").select("*").eq("Phone_Number", phone).single().execute()
        return data[1]
    except:
        return None

def get_point(phone):
    conn = init_connection()
    curr_point = conn.table("Client").select("Point").eq("Phone_Number", phone).single().execute()
    return curr_point

def update_point(phone):
    conn = init_connection()
    data = get_point(phone)
    data = data.data['Point']
    new_data = data+1
    updated_data, _ = conn.table("Client").update({"Point": new_data}).eq("Phone_Number", phone).execute()
    return updated_data[1]

def checkin(phone, services):
    point = 0
    conn = init_connection()
    check = get_client(phone)
    date = datetime.today()
    if check:
        data, _ = conn.table("Check_in").insert({"Phone_Number": phone, "Service": services, "Date": date}).execute()
        update_point(phone)
        return data[1]
    else:
        return "Please sign up"

def signup(fname, lname, dob, phone):
    conn = init_connection()
    check = get_client(phone)
    if check:
        return "You have already sign up"
    else:
        data, _ = conn.table("Client").insert({"First_Name": fname, "Last_Name": lname, "DOB": dob, "Phone_Number": phone, "Point": 0}).execute()
        return data[1]

def main():
    phone = "6027238354"
    services = "Full_set"
    client = checkin(phone, services)
    print(client)
if __name__ == "__main__":
    main()
