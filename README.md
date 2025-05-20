# Skill Academy Final Project - Myth Fact Eyes Health

- Created by : Muhammad Hafizh Dzaki
- Last Edited On : May 2025

This project was created to fulfill the completion of **Artificial Intelligence** course in **Skill Academy Pro** Bootcamp by **Ruangguru**. The Eye Health Facts & Myths website is an AI-based platform designed to check everything related to eye health. This is Langchain-based project using RAG (Retrieval-Augmented Generation) technique. However, there are some **important disclaimers** you should be aware of!

## Disclaimer

1. Non-Medical Background – The creator has an IT background, not a medical or healthcare degree

2. No Expert Verification – There is no certified eye health specialist validating the accuracy of the information provided for AI model

3. AI-Generated Dataset – The data is sourced from a privately created dataset, generated using popular AI tools like OpenAI ChatGPT and Google Gemini

4. AI-Based Validation – Information is only included if both AI tools agree on the conclusion

As a result, the AI may sometimes provide **irrelevant** or **inaccurate answers**. Please use this tool wisely and at your own discretion. For any vision-related concerns, we strongly recommend consulting a **qualified eye doctor directly**.

## How to Run

### Run From Repository

**Prerequisite** : Python Environment Management (Conda or Miniconda preferable)

```
$ conda create --name MyEnv "python<3.13"
$ coda activate MyEnv
```

After that follow these steps below :

```
$ git clone https://github.com/hfzdzakii/SkillAcademy-MythFactEyesHealthRAG.git
$ cd SkillAcademy-MythFactEyesHealthRAG
$ pip install -r requirements.txt
```

Copy `.env.example` file , rename into `.env`. Then, Fill in the GOOGLE_API_KEY field with your API key, which you can create [here](https://console.cloud.google.com/apis/credentials). To generate a new key, click **Create Credentials > API Key**.

To run the project, enter command :

```
$ uvicorn main:app --reload
```

### Run Using Docker

**Prerequisite** : Docker CLI or Docker Desktop and GOOGLE_API_KEY field with your API key, which you can create [here](https://console.cloud.google.com/apis/credentials). To generate a new key, click **Create Credentials > API Key**.

```
$ docker pull hfzdzakii/myth-fact-eyes-health:latest
$ docker run -d -p 8000:8000 -e GOOGLE_API_KEY="<your api key>" --name rag hfzdzakii/myth-fact-eyes-health:latest
```

Open your web browser and go to url :

```
localhost:8000
```

## Understanding Folder 

1. assets : An asset for front-end website
2. chroma_db : Vector store to store embedded text data from document
3. data : Consist of `data.txt` to provide context for LLM model and `model_policy.txt` to strict LLM model for following specified rules
4. static : A javascript file so the website can hit API
5. templates : A couple HTML files for frond-end view

## Understanding Files

1. create.ipynb : An ipynb file preserves as a note for creating RAG
2. main.py : A Python file containing a FastAPI script serves as an API endpoint