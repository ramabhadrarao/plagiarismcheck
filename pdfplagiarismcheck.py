import streamlit as st
import pandas as pd
from elasticsearch import Elasticsearch
from difflib import SequenceMatcher
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
from io import BytesIO
import base64


# function to read pdf file as text
def read_pdf(file):
    with BytesIO(file.read()) as data:
        text = extract_text_to_fp(data, laparams=LAParams(), output_type='text')
    return text


# function to calculate similarity between two texts
def calculate_similarity(text1, text2):
    return SequenceMatcher(None, text1, text2).ratio()


# function to search for matching documents
def search_documents(text):
    # create Elasticsearch client
    es = Elasticsearch()

    # search for documents matching the text
    body = {
        "query": {
            "match": {
                "content": text
            }
        }
    }
    res = es.search(index="documents", body=body)

    # extract matching documents
    docs = []
    for hit in res['hits']['hits']:
        docs.append(hit['_source'])

    return docs


# function to generate plagiarism report
def generate_report(similarity, matching_docs):
    if similarity >= 0.9:
        report = "The documents are highly similar."
    elif similarity >= 0.5:
        report = "The documents are moderately similar."
    else:
        report = "The documents are not very similar."

    report += "\n\nMatching documents:\n\n"
    for doc in matching_docs:
        report += "- {} (score: {})\n".format(doc['title'], doc['score'])

    return report


# streamlit app
def main():
    st.title("Plagiarism Similarity Checker")

    # file uploader
    uploaded_file = st.file_uploader("Upload a PDF document")

    # search for matching documents and generate report
    if uploaded_file:
        # read uploaded file as text
        text = read_pdf(uploaded_file)

        # search for matching documents
        matching_docs = search_documents(text)

        # calculate similarity
        similarity = 0.0
        for doc in matching_docs:
            doc_text = doc['content']
            doc_similarity = calculate_similarity(text, doc_text)
            similarity = max(similarity, doc_similarity)

        # generate report
        report = generate_report(similarity, matching_docs)

        # display report
        st.write("The similarity between the uploaded document and matching documents is:", similarity)
        st.write(report)

        # download report as PDF
        report_data = {'Similarity': similarity, 'Report': report}
        report_df = pd.DataFrame.from_dict(report_data, orient='index', columns=[''])
        pdf = report_df.to_pdf()

        # generate download link
        b64 = base64.b64encode(pdf)
        href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="plagiarism_report.pdf">Download plagiarism report</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
