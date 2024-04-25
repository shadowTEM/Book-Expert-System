import streamlit as st
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceInstructEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
import os



def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def embed_index(doc_list, embed_fn, index_store):
    """Function takes in existing vector_store,
    new doc_list and embedding function that is
    initialized on appropriate model. Local or online.
    New embedding is merged with the existing index. If no
    index given a new one is created"""
    #check whether the doc_list is documents, or text
    try:
        faiss_db = FAISS.from_documents(doc_list,
                                embed_fn)
    except Exception as e:
        faiss_db = FAISS.from_texts(doc_list,
                                embed_fn)

    if os.path.exists(index_store):
        local_db = FAISS.load_local(index_store,embed_fn,allow_dangerous_deserialization=True)
        #merging the new embedding with the existing index store
        local_db.merge_from(faiss_db)
        print("Merge completed")
        local_db.save_local(index_store)
        print("Updated index saved")
    else:
        faiss_db.save_local(folder_path=index_store)
        print("New store created...")

def load_vectorstore(Num):
    e = HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    if Num==0:
        index = FAISS.load_local(folder_path='new_index', 
                                    embeddings=e
                                    )
    elif Num==1:
        index = FAISS.load_local(folder_path='48_laws', 
                                    embeddings=e
                                    )
    # elif Num==2:
    #     index = FAISS.load_local(folder_path='Human_Nature', 
    #                                 embeddings=HuggingFaceEmbeddings(model_name="hkunlp/instructor-xl")
    #                                 ,allow_dangerous_deserialization=True)
    return index

def get_conversation_chain(vectorstore):
    # llm = ChatOpenAI()
    llm = HuggingFaceHub(repo_id = "mistralai/Mistral-7B-Instruct-v0.2", model_kwargs={"temperature":0.4, "max_length":1024})

    memory = ConversationBufferMemory(
        memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain


def handle_userinput(user_question):
    print(user_question)
    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content[message.content.rfind("Helpful Answer"):]), unsafe_allow_html=True)

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                    page_icon=":books:")
    st.write(css, unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")
    if user_question:
        handle_userinput(user_question)

    with st.sidebar:
        st.subheader("Choose your book")
        if st.button("Rich Dad"):
            with st.spinner("Processing"):
                # create vector store
                vectorstore = load_vectorstore(0)
                st.session_state.conversation = get_conversation_chain(
                    vectorstore)
                

        if st.button("48 laws"):
            with st.spinner("Processing"):
                # create vector store
                vectorstore = load_vectorstore(1)
                st.session_state.conversation = get_conversation_chain(vectorstore)

        # if st.button("Human Nature"):
        #     with st.spinner("Processing"):
        #         # create vector store
        #         vectorstore = load_vectorstore(1)

if __name__ == '__main__':
    main()