"""
Prerequisites:
wkhtmltopdf download

"""

"""
How to run:
Run (streamlit run yy.py) in terminal

"""


import io
import streamlit as st
import pdfkit
from io import BytesIO
import base64
import PyPDF2
st.set_page_config(page_title="My Webpage", page_icon=":tada:")

def down_wtopdf(url):
    config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe")
    pdf_bytes = pdfkit.from_url(url, False, configuration=config)
    return pdf_bytes


def extract_text(outputfile):
    pdf_file = PyPDF2.PdfFileReader(BytesIO(outputfile))
    text = ""
    for page_num in range(pdf_file.getNumPages()):
        page = pdf_file.getPage(page_num)
        text += page.extractText()
    return text


def compress(pdf_file):
    pdf_obj = PyPDF2.PdfFileReader(io.BytesIO(pdf_file))
    output_pdf = PyPDF2.PdfFileWriter()
    for i in range(pdf_obj.getNumPages()):
        page = pdf_obj.getPage(i)
        page.compressContentStreams()
        output_pdf.addPage(page)
    output_stream = io.BytesIO()
    output_pdf.write(output_stream)
    compressed_pdf = output_stream.getvalue()
    return compressed_pdf


def preview(outputfile):
    return """<iframe src="data:application/pdf;base64,{pdf_var}" width="100%" height="800px"></iframe>
    """.format(pdf_var=base64.b64encode(outputfile).decode('utf-8'))




with st.container():
    st.title("Convert Webpage to PDF")
    url=st.text_input("", placeholder="Enter URL")
    
    st.write("##")
    if st.button("Submit"):
        global outputfile
        global text_file
        global doc_form
        global compressed_pdf
        outputfile = down_wtopdf(url)
        text_file=extract_text(down_wtopdf(url))
        compressed_pdf=compress(down_wtopdf(url))
        st.markdown("***")


        tab1, tab2 = st.tabs(["Preview", "Download"])
        with tab1:
            st.write("Preview:")
            st.markdown(preview(outputfile), unsafe_allow_html=True)

        with tab2:
            st.write("##")
            st.download_button(
                label="Download PDF",
                data= outputfile,
                file_name="webpage.pdf",
                mime="application/pdf"
            )
            st.download_button(
                label="Download text file",
                data= text_file,
                file_name="extracted_text.txt",
                mime="text/plain"
            )
            st.download_button(
                label="Download Compressed PDF",
                data= compressed_pdf,
                file_name="compressed.pdf",
                mime="application/pdf"
            )    
        
        

            

        

        
