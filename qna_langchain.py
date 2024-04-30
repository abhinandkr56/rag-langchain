from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
import os


# llm_openai = ChatOpenAI(model_name='gpt-3.5-turbo-0125', temperature=0.9, max_tokens=256)
api_key = os.getenv("OPENAI_API_KEY")

llm_openai = ChatOpenAI(model_name='gpt-3.5-turbo', temperature=0, max_tokens=2048, openai_api_key = api_key)


def create_history_aware_retriever_1(llm, rag_retriever):
    ### Contextualize question ###
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, rag_retriever, contextualize_q_prompt
    )

    return history_aware_retriever

def create_question_answer_chain(llm):
    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    return question_answer_chain

def create_rag_chain(llm, rag_retriever):
    history_aware_retriever = create_history_aware_retriever_1(llm, rag_retriever)
    question_answer_chain = create_question_answer_chain(llm)
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    
    return rag_chain

### Statefully manage chat history ###
store = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def create_conversational_rag_chain(rag_chain):
    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )
    return conversational_rag_chain

from langchain_community.vectorstores.pgvector import PGVector

def get_pgvector_store():
    CONNECTION_STRING = "postgresql+psycopg2://appuser:devpassword@localhost:5433/devdb"
    COLLECTION_NAME = "qmap_backend_repo"
    embeddings = OpenAIEmbeddings(api_key=api_key)

    db = PGVector(connection_string=CONNECTION_STRING, embedding_length=1536, 
                collection_name=COLLECTION_NAME, embedding_function=embeddings,
                use_jsonb=True)
    return db


vector_store = get_pgvector_store()
llm = llm_openai
rag_chain = create_rag_chain(llm, vector_store.as_retriever())
conversational_rag_chain = create_conversational_rag_chain(rag_chain)

def ask_qa(chat_id, input):
    response = conversational_rag_chain.invoke({"input": input}, 
                                               config={"configurable": {"session_id": chat_id}})

    return response

def ask_qa_stream(chat_id, input, callbacks=[]):
    iterator = conversational_rag_chain.stream({"input": input}, 
                                               config={"configurable": {"session_id": chat_id}})

    for s in iterator:
        if "answer" not in s:
            continue
        content = s['answer']
        yield content

