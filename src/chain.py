from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.memory import ConversationBufferMemory

from .helper import load_db, load_embeddings, load_llm
from .prompt import condense_prompt, qa_prompt

llm = load_llm()
embeddings = load_embeddings()
vector_db = load_db(embeddings=embeddings)

retriever = vector_db.as_retriever(search_kwargs={"k": 3})

history_aware_chain = create_history_aware_retriever(
    llm, retriever, prompt=condense_prompt
)

qa_chain = create_stuff_documents_chain(llm, qa_prompt)

rag_chain = create_retrieval_chain(history_aware_chain, qa_chain)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)


def ask_bot(query: str):
    response = rag_chain.invoke(
        {
            "input": query,
            "chat_history": memory.load_memory_variables({})["chat_history"],
        }
    )
    memory.save_context({"input": query}, {"output": response["answer"]})
    return response["answer"]
