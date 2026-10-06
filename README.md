OKF Knowledge Assistant
An AI-powered knowledge assistant that converts source PDF documents into structured Open Knowledge Format (OKF) knowledge files and uses that structured knowledge to answer user questions with Google Gemini.
Live Demo
🌐 OKF Knowledge Assistant
Overview
The project is designed around a simple knowledge workflow:
Source PDFs
    ↓
PyPDFLoader
    ↓
Extract structured information
    ↓
OKF Markdown + YAML frontmatter
    ↓
Knowledge Catalog
    ↓
Concept Retrieval
    ↓
Selected OKF knowledge
    ↓
Google Gemini
    ↓
Final Answer
The PDF is treated as the original source document. The generated .md files are the structured knowledge consumed by the application.
Why OKF?
A PDF is useful as a source document, but it is not an ideal format for a knowledge system to inspect, organize, connect, and version at the concept level.
The OKF layer separates:
- Metadata — type, title, description, tags, status, version, source
- Knowledge content — the actual Markdown body
- Relationships — links between related concepts
This makes the knowledge easier to read, update, search, version-control, and use by other applications.
OKF specification:
https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
Project Structure
OKF-Knowledge-Assistant/
│
├── source_pdfs/
│   ├── leave_policy_v1.pdf
│   ├── leave_policy_v2.pdf
│   ├── work_from_home_policy.pdf
│   ├── travel_reimbursement_policy.pdf
│   ├── attendance_policy.pdf
│   └── learning_development_policy.pdf
│
├── okf/
│   ├── index.md
│   ├── attendance_policy.md
│   ├── learning_development_policy.md
│   ├── leave_policy_v1.md
│   ├── leave_policy_v2.md
│   ├── travel_reimbursement_policy.md
│   └── work_from_home_policy.md
│
├── app.py
├── catalog.py
├── convert_to_okf.py
├── generator.py
├── retrieve.py
├── config.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
Main Components
convert_to_okf.py
Reads the source PDFs using LangChain's PyPDFLoader, extracts the structured fields, and creates OKF-style Markdown files with YAML frontmatter.
Example:
PDF
 ↓
PyPDFLoader
 ↓
TYPE / TITLE / DEPARTMENT / VERSION / TAGS / STATUS
 ↓
Markdown + YAML
catalog.py
Reads only the YAML frontmatter from the OKF files and creates a small catalog containing information such as:
title
type
description
tags
status
resource
file path
The catalog helps the application decide which knowledge concept is relevant without loading every full document.
retrieve.py
Takes the user's question and compares its important words with the concept title, description, and tags.
It then selects the best matching OKF concept and loads the full Markdown file.
generator.py
Sends the selected OKF knowledge and the user's question to Google Gemini and generates the final response.
app.py
Provides the Streamlit interface, chat history, example questions, answer display, and a Knowledge used section showing the selected concept's metadata.
Example
User question:
How many days can I work from home?

The system identifies:
Title: Work From Home Policy
Type: Policy
Status: stable
Tags: WFH, remote work, attendance, HR
It then loads the corresponding OKF Markdown file and sends that knowledge to Gemini for the final answer.
Features
- PDF to structured OKF conversion
- YAML frontmatter for knowledge metadata
- Markdown-based knowledge representation
- Simple catalog generation
- Metadata-based concept retrieval
- Support for document versions and lifecycle status
- Related concept links
- Google Gemini answer generation
- Streamlit web interface
- Local .env support
- Streamlit Cloud Secrets support
Run Locally
1. Clone the repository
git clone <your-repository-url>
cd OKF-Knowledge-Assistant
2. Install dependencies
pip install -r requirements.txt
3. Create .env
Create a .env file in the project root:
GEMINI_API_KEY=your_gemini_api_key
Do not commit .env to GitHub.
4. Convert PDFs to OKF
python convert_to_okf.py
This creates the Markdown knowledge files inside the okf/ directory.
5. Build and check the catalog
python catalog.py
6. Run the application
streamlit run app.py
Deployment
The application is deployed using Streamlit Community Cloud.
For deployment, the Gemini API key should be added through Streamlit Secrets instead of committing it to the repository.
Example secret:
GEMINI_API_KEY = "your_gemini_api_key"
Security
- API keys are stored outside the repository.
- .env is excluded through .gitignore.
- .env.example contains only the variable name and no secret value.
Current Scope and Limitations
This version intentionally keeps retrieval simple and explainable.
Current limitations include:
- The PDF converter assumes the source documents contain clearly structured fields.
- Complex PDF tables, scanned documents, and image-heavy documents may require a stronger document-processing pipeline.
- Concept retrieval currently uses metadata and keyword matching.
- The current application does not use a vector database or FAISS.
- The LLM is used for final answer generation after concept retrieval.
Future Improvements
Possible next improvements include:
- Better PDF table and image extraction
- OCR for scanned documents
- More advanced concept retrieval for larger knowledge bases
- Better relationship traversal between concepts
- Automated knowledge validation
- Source-level citations in answers
- Version-aware concept selection
- Enterprise authentication and access control
Technologies Used
- Python
- Streamlit
- LangChain PyPDFLoader
- Open Knowledge Format (OKF)
- Google Gemini API
- PyYAML
- python-dotenv
Author
Deepak Verma
Built as a practical Generative AI / knowledge-management project.