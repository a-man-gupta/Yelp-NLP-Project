from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer, GPT2LMHeadModel, GPT2Tokenizer
import torch
import numpy as np
from pydantic import BaseModel
import random

app = FastAPI()

userful_model = DistilBertForSequenceClassification.from_pretrained("models/useful_model")
userful_tokenizer = DistilBertTokenizer.from_pretrained("models/useful_model")

funny_model = DistilBertForSequenceClassification.from_pretrained("models/funny_model")
funny_tokenizer = DistilBertTokenizer.from_pretrained("models/funny_model")

cool_model = DistilBertForSequenceClassification.from_pretrained("models/cool_model")
cool_tokenizer = DistilBertTokenizer.from_pretrained("models/cool_model")


generation_model = GPT2LMHeadModel.from_pretrained("models/fine_tuned_gpt2")
generation_tokenizer = GPT2Tokenizer.from_pretrained("models/fine_tuned_gpt2")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Enable CORS to allow requests from the frontend (React app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define input data models
class RatingRequest(BaseModel):
    business_id: str
    user_id: str
    review_text: str

class ReviewRequest(BaseModel):
    business_id: str
    user_id: str
    helpful_text: str

# First API: Predict Ratings (funny, useful, cool)
@app.post("/predict-ratings")
async def predict_ratings(request: RatingRequest):
    try:
        # Dummy implementation: Return random ratings between 0 and 5
        funny = random.randint(0, 5)
        useful = random.randint(0, 5)
        cool = random.randint(0, 5)

        userful_inputs = userful_tokenizer(request.review_text, return_tensors="pt", truncation=True, max_length=512)
        funny_inputs = funny_tokenizer(request.review_text, return_tensors="pt", truncation=True, max_length=512)
        cool_inputs = cool_tokenizer(request.review_text, return_tensors="pt", truncation=True, max_length=512) 

        with torch.no_grad():
            userful_outputs = userful_model(**userful_inputs)
            userful_predictions = userful_outputs.logits
            useful_probs = np.argmax(userful_predictions, axis=1)
            if abs(userful_predictions[0][0]) > abs(userful_predictions[0][1]):
                useful_probs = [0]
            else:
                useful_probs = [1]
            useful_score = useful_probs[0]  # Assuming the second class is "useful"

        with torch.no_grad():
            funny_outputs = funny_model(**funny_inputs)
            funny_predictions = funny_outputs.logits
            funny_probs = np.argmax(funny_predictions, axis=1)
            if abs(funny_predictions[0][0]) > abs(funny_predictions[0][1]):
                funny_probs = [0]
            else:
                funny_probs = [1]
            funny_score = funny_probs[0]  # Assuming the second class is "funny"

        with torch.no_grad():
            cool_outputs = cool_model(**cool_inputs)
            cool_predictions = cool_outputs.logits
            cool_probs = np.argmax(cool_predictions, axis=1)
            if abs(cool_predictions[0][0]) > abs(cool_predictions[0][1]):
                cool_probs = [0]
            else:
                cool_probs = [1]
            cool_score = cool_probs[0]  # Assuming the second class is "cool"

        print(userful_predictions)
        print(f"Useful Score: {useful_score}, Funny Score: {funny_score}, Cool Score: {cool_score}")

        return {
            "business_id": request.business_id,
            "user_id": request.user_id,
            "ratings": {
            "funny": 5 if int(funny_score) == 1 else 0,
            "useful": 5 if int(useful_score) == 1 else 0,
            "cool": 5 if int(cool_score) == 1 else 0
            # "funny": funny,
            # "useful": useful,
            # "cool": cool
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting ratings: {str(e)}")

# Second API: Generate Review
@app.post("/generate-review")
async def generate_review(request: ReviewRequest):
    try:

        return {
            "business_id": request.business_id,
            "user_id": request.user_id,
            "generated_review": generate_review(generation_model, generation_tokenizer, request.helpful_text, device)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating review: {str(e)}")


def generate_review(model, tokenizer, prompt, device, max_len=100):
    model.eval()  # Set the model to evaluation mode

    # Tokenize the prompt
    encoding = tokenizer(prompt, return_tensors='pt', padding=True, truncation=True, max_length=max_len)

    # Move the input to the device (GPU or CPU)
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)

    # Generate text
    generated_ids = model.generate(
        input_ids=input_ids, 
        attention_mask=attention_mask, 
        max_length=max_len,
        num_return_sequences=1,  # Number of sequences to return
        no_repeat_ngram_size=2,  # Prevent repetition
        top_p=0.92,  # Nucleus sampling
        top_k=50,  # Top-k sampling
        temperature=0.7,  # Control randomness
    )

    # Decode the generated text
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

    if generated_text.startswith(prompt):
        generated_text = generated_text[len(prompt):].strip()
    
    return generated_text

# Run the server with: uvicorn predict_api:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#  uvicorn predict_api:app --host 0.0.0.0 --port 8000