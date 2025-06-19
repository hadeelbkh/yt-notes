# YouTube Notes Generator - Streamlit UI Setup

This guide will help you set up the Streamlit web interface for your YouTube Notes Generator.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

You have two options for setting up your Gemini API key:

#### Option A: Using Streamlit Secrets (Recommended)
1. Copy the template secrets file:
   ```bash
   cp .streamlit/secrets.toml .streamlit/secrets_local.toml
   ```
2. Edit `.streamlit/secrets_local.toml` and add your actual API key:
   ```toml
   GEMINI_API_KEY = "your_actual_api_key_here"
   CHROMA_GOOGLE_GENAI_API_KEY = "your_actual_api_key_here"
   ```

#### Option B: Using Environment Variables
```bash
export GEMINI_API_KEY="your_actual_api_key_here"
export CHROMA_GOOGLE_GENAI_API_KEY="your_actual_api_key_here"
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎯 Features

- **Simple Input**: Just paste any YouTube URL or video ID
- **Custom Prompts**: Customize how notes are generated
- **Download Options**: Export notes as TXT or Markdown
- **Database Browser**: View and manage all saved notes
- **Real-time Processing**: See progress as the app works
- **Responsive Design**: Works well on desktop and mobile

## 🔧 Configuration

The app uses your existing ChromaDB database in the `my_vectordb` folder, so all your previous notes from the Jupyter notebook will be available.

## 🌐 Deployment Options

### Deploy to Streamlit Cloud (Free)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add your API keys in the Streamlit Cloud secrets section

### Deploy to Heroku
1. Create a `Procfile`:
   ```
   web: sh setup.sh && streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Create `setup.sh`:
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   headless = true\n\
   port = $PORT\n\
   enableCORS = false\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

### Deploy Locally with Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

## 📁 File Structure

```
yt-notes/
├── streamlit_app.py         # Main Streamlit application
├── requirements.txt         # Python dependencies
├── .streamlit/
│   └── secrets.toml        # API key configuration
├── my_vectordb/            # ChromaDB database (existing)
├── get_video_notes.ipynb   # Original notebook (existing)
└── STREAMLIT_SETUP.md      # This setup guide
```

## 🛠️ Troubleshooting

### Common Issues:

1. **API Key Error**: Make sure your Gemini API key is correctly set in secrets or environment variables
2. **ChromaDB Error**: Ensure the `my_vectordb` folder has proper permissions
3. **Transcript Error**: Some videos don't have transcripts available - try a different video
4. **Port Already in Use**: Use `streamlit run streamlit_app.py --server.port 8502` to use a different port

### Getting Help:
- Check the Streamlit logs in your terminal
- Verify your API key is valid at [Google AI Studio](https://makersuite.google.com/)
- Make sure the video has English captions available

## 🎨 Customization

You can easily customize the app by:
- Modifying the CSS in the `st.markdown()` section
- Adding new prompt templates
- Enhancing the UI with additional Streamlit components
- Adding search functionality to the database browser

Enjoy your new YouTube Notes Generator UI! 🎉 