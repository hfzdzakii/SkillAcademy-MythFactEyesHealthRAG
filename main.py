from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.prompts.chat import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_chroma.vectorstores import Chroma
from langchain_community.document_loaders.text import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.output_parsers.string import StrOutputParser
from dotenv import load_dotenv
from contextlib import asynccontextmanager
import google.generativeai as genai
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
assert GOOGLE_API_KEY, "GOOGLE_API_KEY environment variable must be set"

def load_and_split_documents(file_path):
    loader = TextLoader(file_path)
    document = loader.load()
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 50,
        separators=[
            "\n\n",
            "\n",
            " ",
            ".",
            ",",
            "\u200b",
            "\uff0c",
            "\u3001",
            "\uff0e",
            "\u3002",
            "",
        ],
    )
    return splitter.split_documents(document)

def setup_vector_store(documents):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    
def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    return Chroma(
        embedding_function=embeddings,
        persist_directory="./chroma_db"
    )
    
def create_prompt_template():
    system_template = open("./data/model_policy.txt", "r").read().strip().replace("\n", " ")
    human_tempplate = """"Use the following context to answer the question!
        Context: {context}
        Question: {question}
    """
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(human_tempplate)        
    ])
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def setup_chain(retriever, prompt, llm):
    return (
        RunnableMap({
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        })
        | prompt
        | llm
        | StrOutputParser()
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.DB = load_vector_store()
    app.state.RETRIEVER = app.state.DB.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "lambda_mult": 0.5}
    )
    app.state.LLM = ChatGoogleGenerativeAI(
        model="models/gemini-2.0-flash-lite-001",
        temperature=0.3
    )
    app.state.PROMPT = create_prompt_template()
    app.state.CHAIN = setup_chain(
        retriever=app.state.RETRIEVER,
        prompt=app.state.PROMPT,
        llm=app.state.LLM
    )
    app.state.A = 1
    yield
    del app.state.DB
    del app.state.RETRIEVER
    del app.state.LLM
    del app.state.PROMPT
    del app.state.CHAIN

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["POST"],
)

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/readme")
async def read(request: Request):
    return templates.TemplateResponse("readme.html", {"request": request})

@app.post("/predict")
async def check_number(question: str = Form(...)):
    result = app.state.CHAIN.invoke(question)
    confidence = app.state.DB.similarity_search_with_relevance_scores(question)[0][1] * 100
    return JSONResponse(content={"result": result})

@app.get("/set-data")
async def setup_vector_store_endpoint():
    docs = load_and_split_documents("./data/data.txt")
    app.state.DB = setup_vector_store(docs)
    app.state.RETRIEVER = app.state.DB.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 3, "lambda_mult": 0.5}
    )
    app.state.CHAIN = setup_chain(
        retriever=app.state.RETRIEVER,
        prompt=app.state.PROMPT,
        llm=app.state.LLM
    )
    return RedirectResponse(url='/', status_code=303)

@app.get("/set-policy")
async def setup_policy_endpoint():
    app.state.PROMPT = create_prompt_template()
    app.state.CHAIN = setup_chain(
        retriever=app.state.RETRIEVER,
        prompt=app.state.PROMPT,
        llm=app.state.LLM
    )
    app.state.A += 1
    return RedirectResponse(url='/', status_code=303)

@app.get("/debug-state")
async def debug_state_endpoint():
    return JSONResponse(content={
        "State DB": str(app.state.DB),
        "State RETRIEVER": str(app.state.RETRIEVER),
        "State LLM": str(app.state.LLM),
        "State PROMPT": str(app.state.PROMPT),
        "State CHAIN": str(app.state.CHAIN),
        "State A": app.state.A
    })