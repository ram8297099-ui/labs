Incident Search & Answer Generation

A Python-based project for uploading incident documents, generating embeddings, performing vector search, and generating answers from retrieved information.

📌 Overview

This project provides a workflow for:

Uploading incident documents
Processing and embedding documents
Storing incident information for vector search
Searching for relevant incidents using semantic similarity
Generating answers based on retrieved information
📂 Project Structure
File	Description
create_index.py	Creates the initial search/vector index
create_index_v2.py	Updated version of the index creation process
generate_answer.py	Generates answers using retrieved information
search_vector.py	Performs vector-based searches
search_vector_v2.py	Updated vector search implementation
test_embedding.py	Tests embedding generation
upload_incident.py	Uploads and processes incident data
upload_second_incident.py	Uploads an additional incident
upload_v2.py	Updated upload implementation
upload_v2_documents.py	Handles document uploads in the updated workflow
🔄 Workflow
Incident Documents
        ↓
Upload / Process
        ↓
Embeddings
        ↓
Vector Index
        ↓
Semantic Search
        ↓
Relevant Information
        ↓
Answer Generation

🚀 Getting Started
1. Clone the repository
git clone <repository-url>
cd <repository-folder>

2. Create a virtual environment
python -m venv venv

3. Activate the virtual environment

Windows

venv\Scripts\activate


macOS / Linux

source venv/bin/activate

4. Install dependencies

If the repository contains a requirements.txt file:

pip install -r requirements.txt


Otherwise, install the dependencies required by the Python scripts.

▶️ Running the Project
Create the index
python create_index_v2.py

Upload documents
python upload_v2_documents.py

Search the vector index
python search_vector_v2.py

Generate an answer
python generate_answer.py


The exact order may depend on your project configuration and data.

⚙️ Configuration

If the project uses external APIs or services, store credentials in environment variables.

Example:

API_KEY=your_api_key


Never commit API keys, passwords, tokens, or other secrets to GitHub.

🧪 Testing

To test embedding generation:

python test_embedding.py

🛠️ Technologies
Python
Embedding models
Vector search
Semantic search
Generative AI / LLMs
📈 Future Improvements
Add automated tests
Add better error handling and logging
Add a requirements.txt
Add environment-based configuration
Add a REST API
Add a web interface
Support larger incident datasets
👤 Author

ram8297099-ui
