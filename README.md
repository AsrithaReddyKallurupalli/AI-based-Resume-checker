# AI Resume Screening System

An AI-based resume-job matching system that uses semantic vector embeddings to match resumes with job descriptions and identify skill gaps.

## Features
- **Semantic Matching**: Uses Sentence Transformers to understand context, not just keywords.
- **Skill Gap Analysis**: Identifies missing skills required for the job.
- **Resume Parsing**: Supports PDF and DOCX formats.
- **Interactive UI**: Built with Streamlit for easy usage.

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
try this if the above one doesnt work
   ```bash
   pip install sentence-transformers scikit-learn streamlit pdfplumber python-docx
   ```
2. Run the application:
   ```bash
   streamlit run ui/streamlit_app.py
   ```

## Structure
- `resume_parser.py`: Extracts text from files.
- `preprocess.py`: Cleans raw text.
- `embeddings.py`: Generates vector embeddings.
- `similarity.py`: Computes match scores.
- `skills.py`: Extracts and compares skills.
- `app.py`: Main pipeline logic.
- `ui/streamlit_app.py`: User interface.

