# 📦 Smart Inventory AI
**AI-Powered Inventory Management System**

This project is an automated inventory solution that uses the **Gemini 3 Flash** multimodal model to identify items via image uploads and store them in a structured database.

## 🚀 Features
* **AI Identification:** Automatically extracts item name, category, and quantity from images.
* **Structured Data:** Converts visual input into JSON and saves it to a database.
* **Dual-Service Architecture:** FastAPI backend for logic and Streamlit for the user interface.
* **Persistence:** Full CRUD capabilities with SQLite/SQLAlchemy.

## 🛠️ Tech Stack
* **Frontend:** Streamlit
* **Backend:** FastAPI (Python)
* **AI Model:** Gemini 3 Flash
* **Database:** SQLite with SQLAlchemy ORM
* **Version Control:** Git & GitHub

## 📂 Project Structure
* `main.py`: FastAPI server and AI logic.
* `app.py`: Streamlit frontend application.
* `requirements.txt`: Project dependencies.

## ⚙️ Setup Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/tamzidmiskat/smart-inventory.git](https://github.com/tamzidmiskat/smart-inventory.git)


Install dependencies: pip install -r requirements.txt
Set up your .env file with your Gemini API Key: GEMINI_API_KEY=your_key_here
Run the Backend: python main.py
Run the Frontend: streamlit run app.py