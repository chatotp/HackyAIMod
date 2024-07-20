import gdown
from pathlib import Path

def main():
    model_id = "156KQ1_SQ6L1_ZcrVPAXXTVkhLgpTncfO"
    tokenizer_id = "1HBBnuiXj39hQXQ1cizzZZJdioviP1P5U"
    embeddings_id = "1aVtEw7VfiirqaZuUSxhV5ormBTSB4HQQ"

    base_path = "./models/"

    if not Path(base_path).exists():
        Path.mkdir(base_path, parents=True, exist_ok=True)

    gdown.download(id=model_id, output=base_path+"model.pth")
    gdown.download(id=tokenizer_id, output=base_path+"tokenizer.json")
    gdown.download(id=embeddings_id, output=base_path+"embeddings.npy")

if __name__ == "__main__":
    main()