# OKF Knowledge Assistant

An AI-powered knowledge assistant that converts PDF documents into structured Open Knowledge Format (OKF) knowledge and uses Google Gemini to answer questions from that knowledge.

## Live Demo

🌐 [OKF Knowledge Assistant](https://okf-knowledge-assistant.streamlit.app/)

## How It Works

```text
Source PDF
    ↓
PyPDFLoader
    ↓
Extract text and metadata
    ↓
Convert to OKF Markdown
    ↓
Build Knowledge Catalog
    ↓
Retrieve relevant OKF concept
    ↓
Load full knowledge
    ↓
Google Gemini
    ↓
Answer

The PDF is the original source document.
The .md files inside the okf folder are the structured knowledge used by the application.
Why OKF?
PDF is useful as a source document, but it is not designed to represent knowledge in a simple machine-readable structure.
OKF separates:
- Metadata such as type, title, description, tags, version, status, and source
- Knowledge content in Markdown
- Relationships between related concepts
This makes the knowledge easier to organize, read, update, and consume by applications.
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
Reads the source PDF files using LangChain's PyPDFLoader and converts their structured information into Markdown files with YAML frontmatter.
Example:
PDF
 ↓
PyPDFLoader
 ↓
Metadata + Content
 ↓
OKF Markdown

catalog.py
Reads the YAML frontmatter from the OKF files and creates a small knowledge catalog.
The catalog contains information such as:
- Title
- Type
- Description
- Tags
- Status
- Source
- File path
retrieve.py
Takes the user's question and compares it with the titles, descriptions, and tags in the catalog.
It selects the most relevant OKF concept and loads the complete Markdown file.
generator.py
Sends the selected OKF knowledge and the user's question to Google Gemini and generates the final answer.
app.py
Provides the Streamlit interface, chat history, example questions, answers, and the "Knowledge used" section.
Example
User Question
How many days can I work from home?

Retrieved Knowledge
Title: Work From Home Policy
Type: Policy
Status: stable
Tags: WFH, remote-work, attendance, HR

The application then loads the complete work_from_home_policy.md file and sends that knowledge to Gemini.
Answer
Eligible employees may work from home for up to 2 days per week,
subject to manager approval.

Features
- PDF to OKF conversion
- YAML frontmatter
- Markdown-based knowledge
- Knowledge catalog
- Metadata-based retrieval
- Document version information
- Knowledge relationships
- Google Gemini integration
- Streamlit interface
- Source information display
- Streamlit Cloud deployment
Running Locally
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

5. Build the catalog
python catalog.py

6. Start the application
streamlit run app.py

Deployment
The application is deployed on Streamlit Community Cloud.
The Gemini API key is stored using Streamlit Secrets and is not included in the GitHub repository.
Security
The API key is stored outside the Git repository.
.env is included in .gitignore.
.env.example contains only:
GEMINI_API_KEY=

Current Limitations
This version keeps the retrieval system simple and explainable.
- The PDF converter expects structured information in the source documents.
- Complex tables, scanned PDFs, and image-heavy PDFs need a more advanced document-processing pipeline.
- Retrieval currently uses metadata and keyword matching.
- The application does not currently use FAISS or a vector database.
- Gemini is responsible for generating the final natural-language answer.
Future Improvements
- Better extraction of tables and images from PDFs
- OCR for scanned documents
- More advanced semantic retrieval for large knowledge bases
- Better concept relationship traversal
- Source citations in answers
- Automated knowledge validation
- Enterprise authentication and access control
Technologies
- Python
- Streamlit
- LangChain PyPDFLoader
- Open Knowledge Format (OKF)
- Google Gemini API
- PyYAML
- python-dotenv
Author
Deepak Verma
Built as a practical Generative AI and knowledge-management project.