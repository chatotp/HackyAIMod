import json
import numpy as np
import tkinter as tk

from tkinter import ttk, messagebox
from keras.preprocessing.text import tokenizer_from_json
from pathlib import Path

import torch

from utils import *

MAX_LEN = 220
MAX_FEATURES = 327009
NUM_AUX = 6

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths - Make sure content is in models folder
colab_path = "/content/"
kaggle_path = "/kaggle/working/"

prepend_path = "./models/"
if Path(colab_path).exists():
    prepend_path = colab_path
elif Path(kaggle_path).exists():
    prepend_path = kaggle_path

model_path = prepend_path + "model.pth"
embedding_matrix_path = prepend_path + "embeddings.npy"
tokenizer_path = prepend_path + "tokenizer.json"

# Load model and params
embedding_matrix = np.load(embedding_matrix_path)

with open(tokenizer_path) as tknzr:
    tokenizer_json = json.load(tknzr)
    tokenizer = tokenizer_from_json(tokenizer_json)

model = NeuralNet(embedding_matrix, num_aux_targets=NUM_AUX, max_features=MAX_FEATURES)
model.load_state_dict(torch.load(model_path, map_location=device)['model_state_dict'])

def on_submit():
    text = text_entry.get()
    if text.strip() == "":
        messagebox.showwarning("Warning", "Please enter some text.")
        return

    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"You: {text}\n")
    chat_display.config(state=tk.DISABLED)
    text_entry.delete(0, tk.END)

    prediction = predict(text, model, tokenizer)
    result = "violates policy" if prediction[0][0] > 0.5 else "does not violate policy"
    
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, f"System: Your message {result}.\n")
    chat_display.config(state=tk.DISABLED)

# Create the Tkinter window
root = tk.Tk()
root.title("Content Moderation Chat")

mainframe = ttk.Frame(root, padding="10 10 10 10")
mainframe.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

chat_display = tk.Text(mainframe, height=20, width=70, state=tk.DISABLED)
chat_display.grid(column=1, row=1, columnspan=3, sticky=(tk.W, tk.E))

ttk.Label(mainframe, text="Enter text:").grid(column=1, row=2, sticky=tk.W)
text_entry = ttk.Entry(mainframe, width=50)
text_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))

ttk.Button(mainframe, text="Submit", command=on_submit).grid(column=3, row=2, sticky=tk.W)

root.mainloop()