

#   这一部分代码主要是向量话的处理，并再加载在本地的向量库中
import os
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS

with open("sale_course.txt",encoding="utf-8") as f:
    real_estate_sales = f.read()

# 检查并创建目标文件夹
output_dir = r"E:\sales_chatbot\real_estate_sales_course"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)  # 如果不存在，创建文件夹

text_splitter = CharacterTextSplitter(
    separator = r'\d+\.',
    chunk_size = 100,
    chunk_overlap  = 0,
    length_function = len,
    is_separator_regex = True,
)

docs = text_splitter.create_documents([real_estate_sales])

faiss_index  = FAISS.from_documents(docs, OpenAIEmbeddings())

faiss_index.save_local(output_dir)