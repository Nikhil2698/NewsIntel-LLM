from flask import Flask, request, jsonify
import os
import pickle
from langchain import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader, SeleniumURLLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

app = Flask(__name__)
llm = OpenAI(temperature=0.9, max_tokens=500)
embeddings = OpenAIEmbeddings()

def load_data_from_urls(urls):
    loader = SeleniumURLLoader(urls=urls)
    return loader.load()

def split_text(data):
    text_splitter = RecursiveCharacterTextSplitter(
        separators=['\n\n', '\n', '.', ','],
        chunk_size=1000
    )
    return text_splitter.split_documents(data)

def create_vector_store(docs):
    vectorstore = FAISS.from_documents(docs, embeddings)
    vectorstore.save_local('vector_index')
    return vectorstore

@app.route('/process_urls', methods=['POST'])
def process_urls():
    try:
        urls = request.json['urls']
        data = load_data_from_urls(urls)
        docs = split_text(data)
        vector_store = create_vector_store(docs)
        return jsonify([{"url": url, "data": "Processed data for " + url} for url in urls])
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route('/answer_question', methods=['POST'])
def answer_question():
    question = request.json['question']
    new_db = FAISS.load_local("vector_index", embeddings, allow_dangerous_deserialization=True)
    chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=new_db.as_retriever())

    # Process the question and return outputs along with sources
    result = chain({"question": question}, return_only_outputs=False)  # Adjust this to False to include metadata
    answer = result.get("answer", "No answer found.")

    # Retrieve sources from the result
    sources = result.get("sources", [])
    sources_list = [source.get("url", "") for source in sources]  # Assuming sources are dicts with URLs

    # Return both answer and sources
    return jsonify({"question": question, "answer": answer, "sources": sources_list})


if __name__ == '__main__':
    app.run(debug=True)
