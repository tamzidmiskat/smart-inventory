import streamlit as st
import requests
import pandas as pd

# 1. MUST BE THE FIRST STREAMLIT COMMAND
st.set_page_config(page_title="Smart Inventory AI", layout="wide")

# 2. DEFINING THE URL (Make sure this matches everywhere!)
BASE_URL = "https://smart-inventory-pwof.onrender.com"

# --- CONNECTION CHECK BUTTON ---
with st.expander("🛠️ Debug: Check Backend Connection"):
    if st.button("Ping Backend"):
        try:
            response = requests.get(f"{BASE_URL}/") 
            if response.status_code == 200:
                st.success(f"Connected! Backend says: {response.text}")
            else:
                st.error(f"Connected but got error: {response.status_code}")
        except Exception as e:
            st.error(f"Could not connect to backend: {e}")

# 3. GLOBAL CONNECTION CHECK (Stops the app if Render is asleep)
try:
    # Use a small timeout so the user doesn't wait forever if Render is down
    response = requests.get(f"{BASE_URL}/inventory", timeout=5)
    response.raise_for_status()
    inventory = response.json()
except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError):
    st.error("🔌 Backend is offline. Please wait 60 seconds for Render to 'wake up' and refresh the page.")
    st.info("Note: Render Free Tier goes to sleep after 15 mins of inactivity.")
    st.stop() 
except Exception as e:
    inventory = []

# --- UI HEADER ---
st.title("📦 Smart Inventory AI")
st.subheader("Identify and Manage your stock with Gemini 2.5 Flash")

# --- SIDEBAR: UPLOAD ---
with st.sidebar:
    st.header("Scan New Item")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    
    if st.button("🚀 Identify & Save"):
        if uploaded_file is not None:
            with st.spinner("AI is thinking..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                # FIXED: Changed BACKEND_URL to BASE_URL
                response = requests.post(f"{BASE_URL}/identify", files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ Item Successfully Scanned!")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Item Name", data['name'])
                        st.metric("Category", data['category'])
                    with col2:
                        st.metric("Quantity", data['quantity'])
                        st.write(f"**Description:** {data['description']}")
                else:
                    st.error(f"Error: {response.text}")
        else:
            st.warning("Please upload an image first.")

# --- MAIN AREA: VIEW INVENTORY ---
st.header("📋 Current Inventory")

# We already fetched 'inventory' in the connection check above
if inventory is not None:
    if not inventory:
        st.info("Inventory is empty. Scan something to get started!")
    else:
        df = pd.DataFrame(inventory)
        if not df.empty:
            df = df[["id", "name", "category", "quantity", "description"]]
            st.dataframe(df, use_container_width=True, hide_index=True, 
                         column_config={
                             "id": st.column_config.NumberColumn("ID", format="%d"),
                             "quantity": st.column_config.NumberColumn("Qty", format="%d")
                         })

            st.divider()
            st.subheader("🛠️ Manage Items")
            
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

# --- RECIPE GENERATION SECTION ---
st.divider()
st.header("🍳 AI Chef Recommendations")
if st.button("🪄 Generate Recipe", type="secondary"):
    with st.spinner("Gordon Ramsay is thinking..."):
        recipe_res = requests.get(f"{BASE_URL}/generate-recipe")
        if recipe_res.status_code == 200:
            recipe_data = recipe_res.json()
            st.success("✨ AI Chef Recommendation")
            st.info(recipe_data['recipe'])
        else:
            st.error("Could not generate recipe. Check your backend.")