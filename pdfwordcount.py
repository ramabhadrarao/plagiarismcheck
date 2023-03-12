import streamlit as st
from PyPDF4 import PdfFileReader

def get_word_count(page_content):
    # Remove special symbols and numbers from page content
    special_symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '-', '=', '{', '}', '[', ']', '|', '\\', ';', ':', '\'', '\"', ',', '.', '<', '>', '/', '?']
    page_content_without_special = ''.join(char for char in page_content if char not in special_symbols and not char.isdigit())

    # Count total words in page content
    words = page_content.split()
    total_words = len(words)

    # Count words in page content without special symbols and numbers
    words_without_special = page_content_without_special.split()
    total_words_without_special = len(words_without_special)

    # Count number of special symbols in page content
    total_special_symbols = sum([1 for char in page_content if char in special_symbols])

    return total_words, total_words_without_special, total_special_symbols

def main():
    st.title("PDF Word Count")
    st.write("Developed by Rama Bhadra Rao Maddu")
    st.write("if any support mail to : maddu.ramabhadrarao@gmail.com")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_reader = PdfFileReader(uploaded_file)

        total_words = 0
        total_words_without_special = 0
        total_special_symbols = 0

        for page_num in range(pdf_reader.getNumPages()):
            page_content = pdf_reader.getPage(page_num).extractText()
            words, words_without_special, special_symbols = get_word_count(page_content)
            total_words += words
            total_words_without_special += words_without_special
            total_special_symbols += special_symbols

        st.write(f"Total word count: {total_words}")
        st.write(f"Total word count without special symbols and numbers: {total_words_without_special}")
        st.write(f"Total number of special symbols and numbers: {total_special_symbols}")

if __name__ == "__main__":
    main()
