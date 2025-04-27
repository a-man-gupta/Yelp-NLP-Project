from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

app = FastAPI()

# Dummy model loading – replace with real ones
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased').to(device)
tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')

# Define request schemas
class ReviewRequest(BaseModel):
    user_id: str
    business_id: str
    review_text: str

class GenerateRequest(BaseModel):
    user_id: str
    business_id: str
    experience_description: str

@app.post("/predict")
def predict_scores(data: ReviewRequest):
    # Tokenize and move input to device
    inputs = tokenizer(data.review_text, return_tensors="pt", truncation=True, padding=True).to(device)
    
    # Dummy output – replace with inference from your 3 trained models
    # Here we simulate the output as probabilities from 0 to 1
    dummy_output = torch.tensor([[0.8, 0.6, 0.9]])  # [funny, cool, useful]

    # Scale to 0–5 and convert to JSON
    scaled = (dummy_output * 5).squeeze().tolist()
    return {
        "funny": round(scaled[0], 2),
        "cool": round(scaled[1], 2),
        "useful": round(scaled[2], 2)
    }

@app.post("/generate")
def generate_review(data: GenerateRequest):
    # Dummy generation – replace with your generative model's output
    fake_review = f"{data.experience_description} It was a truly memorable visit at {data.business_id}!"

    return {"generated_review": fake_review}
