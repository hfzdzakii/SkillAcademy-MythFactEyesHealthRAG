from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import google.generativeai as genai
import os

def classify_input_with_similarity(input_text, fact_store, myth_store, qa_fakta, qa_mitos, threshold=0.45):
    input_text = input_text.lower()
    
    fakta_score = fact_store.similarity_search_with_relevance_scores(input_text, k=1)[0][1]
    mitos_score = myth_store.similarity_search_with_relevance_scores(input_text, k=1)[0][1]

    if max(fakta_score, mitos_score) < threshold:
        return {"kalimat" : f"Out of Topic", 
                "konfiden" : f"-"}

    if fakta_score > mitos_score:
        ans_fakta = qa_fakta.run(input_text)
        return {"kalimat" : f"{ans_fakta}", 
                "konfiden" : f"{fakta_score*100:.2f}"}
    else:
        ans_mitos = qa_mitos.run(input_text)
        return {"kalimat" : f"{ans_mitos}",
                "konfiden" : f"{mitos_score*100:.2f}"}

def chain_prompt(kalimat, llm, prompt):
    chain = LLMChain(llm=llm, prompt=prompt)
    hasil = chain.run(kalimat)
    return hasil

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

splitter = CharacterTextSplitter(separator = '\n', chunk_size = 250, chunk_overlap = 25)

fakta_loader = TextLoader("./data/fakta.txt")
mitos_loader = TextLoader("./data/mitos.txt")

fakta_docs = fakta_loader.load()
fakta_docs[0].page_content = fakta_docs[0].page_content.lower()

mitos_docs = mitos_loader.load()
mitos_docs[0].page_content = mitos_docs[0].page_content.lower()

fakta = splitter.split_documents(fakta_docs)
mitos = splitter.split_documents(mitos_docs)

embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
db_fakta = FAISS.from_documents(fakta, embeddings)
db_mitos = FAISS.from_documents(mitos, embeddings)

llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

prompt_template = ChatPromptTemplate.from_template(
    """Kamu adalah seorang ahli dalam bidang kesehatan mata. Jika kamu tidak mengetahui jawaban dari pertanyaan atau jika teks yang tersedia tidak memberikan informasi yang cukup, cukup jawablah dengan kalimat yang menyatakan ketidaktahuan mu. Jangan pernah membuat informasi sendiri yang tidak ada dalam teks. Jangan pernah menyebut kata teks untuk merujuk pada dokumen yang diberi kepada kamu.
    Berikut kalimatnya: {question}
    Konteks: {context}
    Jawaban:
    """
)

qa_fakta = RetrievalQA.from_llm(llm=llm, retriever=db_fakta.as_retriever(), prompt=prompt_template)
qa_mitos = RetrievalQA.from_llm(llm=llm, retriever=db_mitos.as_retriever(), prompt=prompt_template)

@app.get("/")
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/readme")
async def read(request: Request):
    return templates.TemplateResponse("readme.html", {"request": request})

@app.post("/check_faktos")
async def check_number(kalimat: str = Form(...)):
    hasil = classify_input_with_similarity(kalimat, db_fakta, db_mitos, qa_fakta, qa_mitos)
    # kalimat_akhir = chain_prompt(hasil['kalimat'], llm, prompt_template)
    kalimat_akhir = hasil['kalimat']
    konfiden = hasil['konfiden']
    return JSONResponse(content={"kalimat": kalimat_akhir, "konfiden": konfiden})