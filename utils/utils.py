from tensorflow.keras.preprocessing.sequence import pad_sequences
import torch

def clean_special_chars(text, punct):
    for p in punct:
        text = text.replace(p, ' ')
    return text

def preprocess_input(text, tokenizer, max_len=220, device='cpu'):
    punct = "/-'?!.,#$%\'()*+-/:;<=>@[\\]^_`{|}~`" + '""“”’' + '∞θ÷α•à−β∅³π‘₹´°£€\×™√²—–&'
    text = clean_special_chars(text, punct)
    sequences = tokenizer.texts_to_sequences([text])
    padded_sequences = pad_sequences(sequences, maxlen=max_len)
    return torch.tensor(padded_sequences, dtype=torch.long).to(device)

def predict(text, model, tokenizer, device='cpu'):
    x_input = preprocess_input(text, tokenizer, device=device)
    model.to(device)
    model.eval()
    with torch.no_grad():
        output = model(x_input).cpu().numpy()
    return output