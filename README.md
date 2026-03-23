# 📦 Smart Inventory AI

An AI-powered inventory management system that uses **Computer Vision (Gemini 2.0 Flash)** to identify stock items from images and provides intelligent insights, such as recipe generation based on current stock.

## 🚀 Live Demo
* **Frontend:** [INSERT_YOUR_STREAMLIT_URL_HERE]
* **API Backend:** [https://smart-inventory-pwof.onrender.com](https://smart-inventory-pwof.onrender.com)

---

## ✨ Features
* **AI Item Identification:** Upload an image of a product, and Gemini automatically identifies the name, category, and suggests a quantity.
* **Automated Logging:** Identified items are instantly saved to a persistent SQLite database.
* **Inventory Dashboard:** A clean, searchable interface to view and manage (delete/update) stock.
* **AI Chef:** One-click recipe generation that analyzes your current ingredients and suggests creative meals.
* **Decoupled Architecture:** Separate FastAPI backend and Streamlit frontend for scalability.

---

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** FastAPI
* **AI Model:** Google Gemini 2.0 Flash
* **Database:** SQLAlchemy with SQLite
* **Deployment:** Render (Backend) & Streamlit Cloud (Frontend)

---

## ⚙️ Setup & Installation

### 1. Prerequisites
* Python 3.11+
* A Google AI Studio API Key

### 2. Environment Variables
Create a `.env` file in your backend folder:
```bash
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Installation
```bash
# Clone the repository
git clone [https://github.com/your-username/smart-inventory.git](https://github.com/your-username/smart-inventory.git)

# Install dependencies
pip install -r requirements.txt

# Run the Backend
python main.py

# Run the Frontend
streamlit run app.py
```

---

## 📡 API Endpoints
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/inventory` | Fetch all items from the database |
| `POST` | `/identify` | Upload image to identify and save item |
| `DELETE` | `/inventory/{id}` | Remove an item by ID |
| `GET` | `/generate-recipe` | Get AI-generated meal ideas |

---

## 💡 Assignment Highlights
* **CORS Integration:** Configured middleware to allow secure communication between Streamlit and FastAPI.
* **Pydantic Validation:** Used strict typing for API responses to ensure data integrity.
* **Error Handling:** Robust try-except blocks to manage Render's "cold-start" behavior.
```