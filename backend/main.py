import os
import io
import PIL.Image
from typing import List
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from google import genai
from google.genai import types
from pydantic import BaseModel
from dotenv import load_dotenv
# Database Imports
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
Base = declarative_base()


# --- DATABASE SETUP ---
DATABASE_URL = "sqlite:///./inventory.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class DBItem(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category = Column(String)
    quantity = Column(Integer)
    description = Column(Text)

# Create the database file
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- GEMINI & FASTAPI SETUP ---
load_dotenv()
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(api_version='v1beta')
)

class InventoryItem(BaseModel):
    name: str
    category: str
    quantity: int
    description: str

app = FastAPI(title="Smart Inventory AI")

# --- ROUTES ---

@app.get("/")
def home():
    return {"message": "Inventory API is running"}

@app.get("/inventory")
def get_all_items(db: Session = Depends(get_db)):
    return db.query(DBItem).all()

@app.post("/identify", response_model=InventoryItem)
async def identify_item(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Validation check (moved inside the function)
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    try:
        image_bytes = await file.read()
        img = PIL.Image.open(io.BytesIO(image_bytes))

        prompt = "Identify this inventory item specifically (e.g., brand and model). Provide name, category, quantity, and a brief description."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[prompt, img],
            config=types.GenerateContentConfig(
                response_mime_type='application/json',
                response_schema=InventoryItem,
            )
        )

        ai_data = response.parsed 

        # 2. SAVE TO DATABASE
        new_item = DBItem(
            name=ai_data.name,
            category=ai_data.category,
            quantity=ai_data.quantity,
            description=ai_data.description
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        return ai_data

    except Exception as e:
        print(f"Error: {e}") 
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/inventory/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": f"Item {item_id} deleted successfully"}

@app.patch("/inventory/{item_id}")
def update_item(item_id: int, updates: InventoryItem, db: Session = Depends(get_db)):
    item = db.query(DBItem).filter(DBItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.name = updates.name
    item.category = updates.category
    item.quantity = updates.quantity
    item.description = updates.description
    
    db.commit()
    return item

@app.get("/generate-recipe")
def generate_recipe(db: Session = Depends(get_db)):
    # 1. Fetch all items from the database
    items = db.query(DBItem).all()
    if not items:
        return {"recipe": "Your inventory is empty! Scan some ingredients first."}
    
    # 2. Create a list of ingredient names
    ingredient_list = [item.name for item in items]
    ingredients_str = ", ".join(ingredient_list)
    
    # 3. Ask Gemini to be a Chef
    try:
        prompt = f"I have the following ingredients: {ingredients_str}. Suggest a creative recipe I can make. Include a title, ingredients list, and brief steps. Keep it concise."
        
        response = client.models.generate_content(
            model='gemini-2.5-flash', # Use the model you have configured
            contents=prompt
        )
        
        return {"recipe": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)