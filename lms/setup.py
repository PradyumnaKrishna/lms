import os


def _setup(base_dir):
    if "NLTK_DATA" not in os.environ:
        nltk_data = os.path.join(base_dir, ".cache", "nltk_data")
        os.environ["NLTK_DATA"] = nltk_data

        import nltk

        nltk.download("stopwords", quiet=True, download_dir=nltk_data)
        nltk.download("punkt", quiet=True, download_dir=nltk_data)

    if "HF_HOME" not in os.environ:
        hf_home = os.path.join(base_dir, ".cache", "huggingface")
        os.environ["HF_HOME"] = hf_home
