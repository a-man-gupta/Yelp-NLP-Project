import torch
from transformers import DistilBertForSequenceClassification

# Load the models
userful_model = DistilBertForSequenceClassification.from_pretrained("models/useful_model")
funny_model = DistilBertForSequenceClassification.from_pretrained("models/funny_model")
cool_model = DistilBertForSequenceClassification.from_pretrained("models/cool_model")

# Function to compare if two models are identical
def are_models_identical(model1, model2):
    for param1, param2 in zip(model1.parameters(), model2.parameters()):
        if not torch.equal(param1, param2):
            return False
    return True

# Test if the models are identical
if __name__ == "__main__":
    if are_models_identical(userful_model, funny_model):
        print("Useful and Funny models are identical!")
    else:
        print("Useful and Funny models are different!")

    if are_models_identical(userful_model, cool_model):
        print("Useful and Cool models are identical!")
    else:
        print("Useful and Cool models are different!")

    if are_models_identical(funny_model, cool_model):
        print("Funny and Cool models are identical!")
    else:
        print("Funny and Cool models are different!")