import streamlit as st
import requests

# Set page config
st.set_page_config(page_title="Smart Inventory AI", layout="wide")

st.title("📦 Smart Inventory AI")
st.subheader("Identify and Manage your stock with Gemini 2.5")

# URL of your FastAPI backend
BASE_URL = "http://127.0.0.1:8000"

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

if st.button("🔄 Refresh Inventory"):
    response = requests.get(f"{BASE_URL}/inventory")
    if response.status_code == 200:
        inventory = response.json()
        if not inventory:
            st.info("Inventory is empty. Scan something!")
        else:
            # Display items in a nice table
            for item in inventory:
                with st.expander(f"{item['name']} (Qty: {item['quantity']})"):
                    st.write(f"**Category:** {item['category']}")
                    st.write(f"**Description:** {item['description']}")
                    if st.button(f"🗑️ Delete {item['name']}", key=f"del_{item['id']}"):
                        requests.delete(f"{BASE_URL}/inventory/{item['id']}")
                        st.rerun()
    else:
        st.error("Could not fetch inventory.")