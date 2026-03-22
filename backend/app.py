import streamlit as st
import requests
import pandas as pd

# URL of your FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

# Set page config
st.set_page_config(page_title="Smart Inventory AI", layout="wide")

# Connection Check
try:
    response = requests.get(f"{BASE_URL}/inventory")
    response.raise_for_status()
    inventory = response.json()
except requests.exceptions.ConnectionError:
    st.error("🔌 Backend is offline. Please start main.py!")
    st.stop() # This stops the app from trying to run the rest and crashing
except Exception as e:
    inventory = []

st.title("📦 Smart Inventory AI")
st.subheader("Identify and Manage your stock with Gemini 2.5")

# --- SIDEBAR: UPLOAD ---
with st.sidebar:
    st.header("Scan New Item")
    uploaded_file = st.file_uploader("Upload an image of the item...", type=["jpg", "jpeg", "png"])
    
    if st.button("🚀 Identify & Save"):
        if uploaded_file is not None:
            with st.spinner("AI is thinking..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(f"{BASE_URL}/identify", files=files)
                
                if response.status_code == 200:
                    st.success("Item Identified & Saved!")
                    st.json(response.json())
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload an image first.")

# --- MAIN AREA: VIEW INVENTORY ---
st.header("📋 Current Inventory")

# Fetch inventory data
response = requests.get(f"{BASE_URL}/inventory")

if response.status_code == 200:
    inventory = response.json()
    
    if not inventory:
        st.info("Inventory is empty. Scan something to get started!")
    else:
        # 1. Display as a clean Dataframe/Table
        df = pd.DataFrame(inventory)
        # Reorder and rename columns for the UI
        df = df[["id", "name", "category", "quantity", "description"]]
        st.dataframe(df, use_container_width=True, hide_index=True, column_config={"id": st.column_config.NumberColumn("ID", format="%d"),"quantity": st.column_config.NumberColumn("Qty", format="%d")})

        # 2. Management Section (Delete/Update)
        st.divider()
        st.subheader("🛠️ Manage Items")
        
        # Create a dropdown to select an item to delete or view
        item_names = {f"{i['name']} (ID: {i['id']})": i['id'] for i in inventory}
        selected_item_label = st.selectbox("Select an item to manage:", options=list(item_names.keys()))
        selected_id = item_names[selected_item_label]

        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🗑️ Delete Selected", type="primary"):
                del_res = requests.delete(f"{BASE_URL}/inventory/{selected_id}")
                if del_res.status_code == 200:
                    st.success("Deleted!")
                    st.rerun()
        with col2:
            st.caption("Warning: Deleting an item is permanent.")

else:
    st.error("Could not connect to the backend server.")