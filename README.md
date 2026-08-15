# AI Resume Screening & Job Recommendation System

An AI-powered web app that analyzes a candidate's resume and recommends the most suitable job role based on their skills, education, and experience — built as part of a Generative AI mini-project.

## Features

-  Upload resumes in **PDF** or **DOCX** format
-  Automatic text extraction (handles multi-page PDFs and table-based DOCX layouts)
-  AI-powered analysis using **Google Gemini**, including:
-  Technical & soft skill extraction
-  Candidate profile summary
-  Recommended job role
-  Missing skills for the recommended role
-  Clean, organized dashboard-style results display
-  Error handling for unsupported files, empty uploads, and failed API responses

## Tech Stack

- **Python**
- **Streamlit** — UI/dashboard
- **pdfplumber** — PDF text extraction
- **python-docx** — DOCX text extraction
- **Google Gemini API** (`google-genai`) — resume analysis

## Project Structure

```
resume_ai/
├── app.py              # Streamlit UI and main app flow
├── resume_parser.py     # PDF/DOCX text extraction logic
├── ai_analyzer.py        # Gemini API integration and JSON parsing
├── requirements.txt
├── .env                  # API key (not committed — see setup below)
```

## Setup & Installation

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd resume_ai
```

2. **Create and activate a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate      # macOS/Linux
   venv\Scripts\activate.bat     # Windows
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Add your Gemini API key**

   Create a `.env` file in the project root:
```
   GEMINI_API_KEY=your_api_key_here
```
   Get a free key from [Google AI Studio](https://aistudio.google.com/apikey).

5. **Run the app**
```bash
   streamlit run app.py
```

## How It Works

1. User uploads a resume (PDF/DOCX)
2. Text is extracted using `pdfplumber` (PDF) or `python-docx` (DOCX)
3. Extracted text is sent to Gemini with a structured prompt requesting a fixed JSON schema
4. The response is parsed and validated for required fields
5. Results are rendered in a Streamlit dashboard across organized sections

## Future Improvements

- OCR support for scanned/image-based resumes
- Support for multiple job role suggestions with match scores
- Resume improvement suggestions (formatting, phrasing)
- Export analysis as a PDF report