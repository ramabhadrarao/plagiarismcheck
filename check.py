import streamlit as st
from copydetect import copydetect
from difflib import SequenceMatcher


# function to read uploaded file as text
def read_file(file):
    text = file.read().decode('utf-8')
    return text


# function to check for plagiarism using copydetect library
def check_plagiarism(code):
    # read codes from plagiarism database
    with open('plagiarism_database.py') as f:
        database_codes = f.read().split('\n\n')

    # check for plagiarism using copydetect library
    matching_codes = copydetect(code, database_codes)

    return matching_codes


# function to calculate similarity between two code snippets
def calculate_similarity(code1, code2):
    return SequenceMatcher(None, code1, code2).ratio()


# streamlit app
def main():
    st.title("Code Plagiarism Checker")

    # file uploader
    uploaded_file = st.file_uploader("Upload a Python file")

    # check for plagiarism and generate report
    if uploaded_file:
        # read uploaded file as text
        code = read_file(uploaded_file)

        # check for plagiarism using copydetect library
        matching_codes = check_plagiarism(code)

        # generate report
        if matching_codes:
            report = "The uploaded code is similar to the following code(s):\n\n"
            for matching_code in matching_codes:
                # calculate similarity percentage between uploaded code and matching code snippet
                similarity_uploaded = calculate_similarity(code, matching_code)
                similarity_matching = calculate_similarity(matching_code, code)
                report += "- Uploaded code similarity: {:.2%}\n".format(similarity_uploaded)
                report += "- Matching code similarity: {:.2%}\n\n{}\n\n".format(similarity_matching, matching_code)
        else:
            report = "The uploaded code is not similar to any code in the plagiarism database."

        # display report
        st.write(report)

        # download report as text file
        href = f'<a href="data:text/plain;base64,{base64.b64encode(report.encode()).decode()}" download="plagiarism_report.txt">Download plagiarism report</a>'
        st.markdown(href, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
