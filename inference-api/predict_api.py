from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

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

        # In the future, replace with model inference, e.g.:
        # model = joblib.load("path/to/ratings_model.pkl")
        # features = preprocess_review_text(request.review_text)  # Tokenize, embed, etc.
        # prediction = model.predict(features)
        # funny, useful, cool = prediction[0]

        return {
            "business_id": request.business_id,
            "user_id": request.user_id,
            "ratings": {
                "funny": funny,
                "useful": useful,
                "cool": cool
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error predicting ratings: {str(e)}")

# Second API: Generate Review
@app.post("/generate-review")
async def generate_review(request: ReviewRequest):
    try:
        # Dummy implementation: Return a template-based review
        review_text = (
            f"Based on my experience at the business (ID: {request.business_id}), "
            f"I found it to be {request.helpful_text.lower()}. "
            "The service was great, and I would recommend it to others!"
        )

        # In the future, replace with generative AI, e.g.:
        # from transformers import pipeline
        # generator = pipeline("text-generation", model="gpt2")
        # prompt = f"Generate a review for business {request.business_id} by user {request.user_id}: {request.helpful_text}"
        # review_text = generator(prompt, max_length=100)[0]["generated_text"]

        return {
            "business_id": request.business_id,
            "user_id": request.user_id,
            "generated_review": review_text
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating review: {str(e)}")

# Run the server with: uvicorn predict_api:app --host 0.0.0.0 --port 8000
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

#  uvicorn predict_api:app --host 0.0.0.0 --port 8000