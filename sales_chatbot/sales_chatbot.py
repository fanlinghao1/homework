import gradio as gr

from langchain_openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS


#这部分是房产销售
def initialize_sales_bot(vector_store_dir: str = r"real_estate_sales_data"):
    db = FAISS.load_local(vector_store_dir, OpenAIEmbeddings(),
                          allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    global SALES_BOT
    SALES_BOT = RetrievalQA.from_chain_type(llm,
            retriever=db.as_retriever(search_type="similarity_score_threshold",
                                    search_kwargs={"score_threshold": 0.8}))
    # 返回向量数据库的检索结果
    SALES_BOT.return_source_documents = True

    return SALES_BOT


def sales_chat(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    # TODO: 从命令行参数中获取
    enable_chat = True

    ans = SALES_BOT({"query": message})
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return "这个问题我要问问领导"

#这部分是教育销售
def initialize_sales_bot_course(vector_store_dir: str = r"real_estate_sales_course"):
    db = FAISS.load_local(vector_store_dir, OpenAIEmbeddings(),
                          allow_dangerous_deserialization=True)
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    global SALES_BOT_COURSE
    SALES_BOT_COURSE = RetrievalQA.from_chain_type(llm,
            retriever=db.as_retriever(search_type="similarity_score_threshold",
                                    search_kwargs={"score_threshold": 0.8}))
    # 返回向量数据库的检索结果
    SALES_BOT_COURSE.return_source_documents = True

    return SALES_BOT_COURSE


def sales_course_chat(message, history):
    print(f"[message]{message}")
    print(f"[history]{history}")
    # TODO: 从命令行参数中获取
    enable_chat = True

    ans = SALES_BOT_COURSE({"query": message})
    # 如果检索出结果，或者开了大模型聊天模式
    # 返回 RetrievalQA combine_documents_chain 整合的结果
    if ans["source_documents"] or enable_chat:
        print(f"[result]{ans['result']}")
        print(f"[source_documents]{ans['source_documents']}")
        return ans["result"]
    # 否则输出套路话术
    else:
        return "这个问题我要问问领导"

"""
def launch_gradio():
    demo = gr.ChatInterface(
        fn=sales_chat,
        title="房产销售",
        # retry_btn=None,
        # undo_btn=None,
        chatbot=gr.Chatbot(height=600),
    )
"""


with gr.Blocks() as demo:
    gr.Markdown("## 选项卡选择")
    with gr.Tabs() as tabs:
        with gr.TabItem("房产销售"):
            input1 = gr.Textbox(label="输入1")
            output1 = gr.Textbox(label="输出1")
            gr.Button("发送").click(sales_chat, inputs=input1, outputs=output1)
        with gr.TabItem("教育销售"):
            input1 = gr.Textbox(label="输入1")
            output1 = gr.Textbox(label="输出1")
            gr.Button("发送").click(sales_course_chat, inputs=input1, outputs=output1)

#demo.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    # 初始化房产销售机器人
    SALES_BOT = initialize_sales_bot()
    SALES_BOT_COURSE = initialize_sales_bot_course()
    # 启动 Gradio 服务
    demo.launch(share=True, server_name="0.0.0.0")