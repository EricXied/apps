import random
import json
import torch
from .model import NeuralNet
from .nltk_utils import bag_of_words, tokenize
import os

# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device("cpu")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "\chatbot\intents.json")

with open(file_path, "r") as f:
    intents = json.load(f)

FILE = os.path.join(BASE_DIR, "chatbot\data.pth")
data = torch.load(FILE)
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data["all_words"]
tags = data["tags"]
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"
# print("Let's chat! type 'quit' to exit")


def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]

    if prob.item() > 0.75:
        for intent in intents["intents"]:
            if tag == intent["tag"]:
                return random.choice(intent["responses"])

    else:
        return "I do not understand..."


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        msg = input("You: ")
        get_response(msg)
        if msg == "quit":
            break
        resp = get_response(msg)
        print(resp)
