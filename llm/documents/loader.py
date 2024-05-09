from typing import Optional

import nltk
from nltk.corpus import stopwords

from langchain.docstore.document import Document
from langchain.text_splitter import TextSplitter

from langchain_community.document_loaders import UnstructuredPDFLoader


def load_document(file: str, splitter: Optional[TextSplitter] = None):

    loader = UnstructuredPDFLoader(file)
    return loader.load_and_split(splitter)


def preprocess(document: Document):
    """
    Tokenizes and preprocesses the input text, removing stopwords and short
    tokens.

    Parameters:
        document (str): The input document to preprocess.
    Returns:
        list: A list of preprocessed tokens.
    """

    text = document.page_content
    result = ""
    lines = text.split('\n')

    text = []
    for line in lines:
        tokens = nltk.word_tokenize(line)
        stop_words = set(stopwords.words(['english']))
        result = " ".join([token.lower() for token in tokens if (token.isalpha() or token.isnumeric()) and token not in stop_words])
        text.append(result)
    
    text = "\n".join(text)
    return Document(page_content=text, metadata=document.metadata)
