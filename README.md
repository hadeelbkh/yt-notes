# YouTube Notes Generator with Gemini & ChromaDB

This project automatically extracts transcripts from YouTube videos, summarizes them using Google's Gemini 1.5 Flash model, and stores the results in a persistent Chroma vector database for later retrieval and querying.

## Features

- Download and parse YouTube video transcripts
- Summarize transcripts using Gemini 1.5 Flash
- Store notes in a Chroma vector database with vector embeddings
- Easily search or expand later using vector search

## Technologies Used

- [Google Generative AI](https://ai.google.dev/)
- [ChromaDB](https://www.trychroma.com/)
- [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/)
- Python 3, Google Colab
- SQLite3, `.bin` index files
- Google Drive integration

## How It Works

1. The user provides a YouTube video ID.
2. The transcript is fetched using `youtube-transcript-api`.
3. Gemini generates a summary based on the transcript and a customizable prompt.
4. The result is saved as `.txt` and stored in a Chroma vector collection with an embedding function.

## Folder Structure

```
yt-notes/
├── get_video_notes.ipynb  # Main Colab notebook
├── chroma.sqlite3         # Metadata for vector DB
├── index/                 # Binary index files (auto-generated)
├── temp_notes.txt         # Summarized notes (temporary)
└── temp_transcript.txt    # Transcript from YouTube video (temporary)
```

## Environment Variables

Secrets must be added securely. For Colab, use the **Secrets tab** or `userdata.get()`:

- `GEMINI_API_KEY` - your Google AI API key
- `CHROMA_GOOGLE_GENAI_API_KEY` - used for embedding functions

```python
from google.colab import userdata
GEMINI_API_KEY = userdata.get("GEMINI_API_KEY")
```

## Setup (Colab)

1. Mount your Google Drive
2. Install dependencies (via `!pip install`)
3. Add your Secrets using the Colab sidebar
4. Run the notebook `get_video_notes.ipynb`

## Contributions

PRs and ideas are welcome! Just open an issue or fork the repo.


*Built by Hadeel❤️*