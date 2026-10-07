# OKF Knowledge Assistant

An AI-powered knowledge assistant that converts PDF documents into structured OKF knowledge and uses semantic search with FAISS to find relevant information before generating an answer with Google Gemini.

## Live Demo

https://okf-knowledge-assistant.streamlit.app/

## How It Works

```text
12 Source PDFs
      ↓
PyPDFLoader
      ↓
Extract metadata and content
      ↓
OKF Markdown files
      ↓
Knowledge Catalog
      ↓
Sentence Transformer Embeddings
      ↓
FAISS Index
      ↓
User Question
      ↓
Question Embedding
      ↓
FAISS Search
      ↓
Relevant OKF Knowledge
      ↓
Google Gemini
      ↓
Final Answer

Project Overview
The source of knowledge in this project is a set of company-policy PDF documents.
The PDFs are converted into structured Markdown files using an OKF-style format.
Each OKF file contains:
- Metadata such as title, department, version, tags, and status
- The actual policy content
- The source PDF reference
The application creates embeddings from the knowledge metadata and stores them in a FAISS index.
When a user asks a question, the question is also converted into an embedding. FAISS finds the most relevant knowledge concept.
The complete OKF file is then given to Google Gemini to generate the final answer.
Why OKF?
PDFs are useful as source documents, but they are not the most convenient format for representing structured knowledge.
The OKF files separate metadata from the actual knowledge content.
For example:
---
type: Policy
title: Employee Leave Policy
department: Human Resources
version: 2.0
tags:
  - leave
  - annual leave
  - sick leave
status: stable
source: /source_pdfs/leave_policy.pdf
---

The content of the policy is stored below the metadata.
This makes the knowledge easier to organize, retrieve, update, and use in an application.
Knowledge Base
The current knowledge base contains 12 policy documents:
1. Employee Leave Policy
2. Work From Home Policy
3. Employee Attendance Policy
4. Business Travel Policy
5. Travel Reimbursement Policy
6. Learning and Development Policy
7. Performance Review Policy
8. Employee Benefits Policy
9. Employee Code of Conduct
10. Remote Work Security Policy
11. Employee Expense Policy
12. IT Asset Policy

The documents are stored in:
source_pdfs/

and converted OKF files are stored in:
okf/

Project Structure
OKF-Knowledge-Assistant/
│
├── source_pdfs/
│   └── 12 PDF knowledge files
│
├── okf/
│   └── 12 OKF Markdown files
│
├── index/
│   ├── faiss.index
│   └── catalog.pkl
│
├── app.py
├── catalog.py
├── config.py
├── convert_to_okf.py
├── embedder.py
├── generator.py
├── retrieve.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
└── .gitignore

Main Files
convert_to_okf.py
Reads the PDF files using LangChain's PyPDFLoader.
It extracts the metadata and content from each PDF and creates an OKF Markdown file.
PDF
 ↓
PyPDFLoader
 ↓
Metadata + Content
 ↓
OKF Markdown

catalog.py
Reads the YAML metadata from the OKF files and creates a knowledge catalog.
The catalog contains information such as:
- Title
- Department
- Version
- Tags
- Status
- Source
- File path
embedder.py
Uses the Sentence Transformers model:
all-MiniLM-L6-v2

to convert text into numerical embeddings.
The same embedding model is used for both the knowledge and the user question.
retrieve.py
Handles semantic retrieval using FAISS.
The metadata of every knowledge concept is converted into an embedding and stored in the FAISS index.
When the user asks a question:
Question
   ↓
Question Embedding
   ↓
FAISS Search
   ↓
Best Matching Knowledge

The complete OKF file is then loaded using the selected concept.
generator.py
Sends the retrieved OKF knowledge and the user's question to Google Gemini.
Gemini generates the final answer using the retrieved knowledge as the main source.
app.py
Provides the Streamlit interface.
It handles:
- Chat interface
- Chat history
- Question input
- Knowledge retrieval
- Gemini response generation
- Display of the selected knowledge source
Example
Question
What are the normal working hours?

Retrieval
FAISS selects:
Employee Attendance Policy

Knowledge
The application loads the complete attendance_policy.md file.
Answer
Standard working hours are 9:00 AM to 6:00 PM from Monday to Friday,
including a one-hour lunch break.

Example of Semantic Retrieval
A question does not always have to use the exact words from a document.
For example:
Can I get money back for a hotel during a work trip?

can retrieve:
Travel Reimbursement Policy

because the embedding-based search compares the semantic meaning of the question with the knowledge metadata.
FAISS
FAISS is used to perform vector similarity search.
The project uses:
faiss.IndexFlatL2

The embeddings are stored in:
index/faiss.index

The catalog used to map FAISS results back to the original knowledge files is stored in:
index/catalog.pkl

The current knowledge base is small, so a simple FAISS index is sufficient.
Running Locally
1. Install dependencies
pip install -r requirements.txt

2. Create .env
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key

Do not commit this file to GitHub.
3. Convert PDFs to OKF
python convert_to_okf.py

4. Run the application
streamlit run app.py

The application will open in the browser.
Technologies
- Python
- Streamlit
- LangChain PyPDFLoader
- Open Knowledge Format style Markdown
- Sentence Transformers
- FAISS
- Google Gemini API
- PyYAML
- python-dotenv
Environment Variables
The project uses:
GEMINI_API_KEY

For local development it is stored in .env.
For Streamlit Cloud it can be stored in Streamlit Secrets.
The actual API key is not included in the repository.
Current Limitations
- The PDF converter currently works best with text-based PDFs.
- Scanned PDFs and complex image-based documents would need additional processing.
- The current FAISS index retrieves the best matching knowledge concept.
- The application currently uses a single best knowledge result for answer generation.
- The project does not use a separate vector database because the current knowledge base is small.
Future Improvements
- Retrieve multiple relevant concepts
- Add concept relationships
- Add source citations in answers
- Improve PDF extraction for complex documents
- Add OCR support for scanned PDFs
- Add authentication and access control
- Use a vector database for a much larger knowledge base
Author
Deepak Verma
A practical Generative AI and knowledge-management project using Python, OKF-style structured knowledge, embeddings, FAISS, and Google Gemini.