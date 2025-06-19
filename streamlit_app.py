import streamlit as st
import os
import re
import shutil
from youtube_transcript_api import YouTubeTranscriptApi
import google.generativeai as genai
import chromadb
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="YouTube Notes Generator - Fixed", page_icon="📝", layout="wide")

st.title("📝 YouTube Notes Generator - Fixed Version")
# st.write("This version fixes the ChromaDB compatibility issue!")

def extract_video_id(url_or_id):
    if not url_or_id:
        return None
    if len(url_or_id) == 11 and re.match(r'^[a-zA-Z0-9_-]+$', url_or_id):
        return url_or_id
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/embed/([a-zA-Z0-9_-]{11})',
        r'youtube\.com/v/([a-zA-Z0-9_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

@st.cache_data
def get_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'en-US', 'en-GB'])
        formatted_transcript = "\n".join(entry['text'] for entry in transcript)
        return formatted_transcript, None
    except Exception as e:
        return None, str(e)

def initialize_services():
    gemini_api_key = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY")
    
    if not gemini_api_key:
        st.error("❌ GEMINI_API_KEY not found.")
        st.stop()
    
    try:
        genai.configure(api_key=gemini_api_key)
        gemini_model = genai.GenerativeModel('models/gemini-1.5-flash')
        # st.success("✅ Gemini configured")
    except Exception as e:
        return None, None, f"Gemini error: {e}"
    
    # Fix ChromaDB - use new database path
    db_path = './my_vectordb_fixed'
    
    # Backup old database if exists
    if os.path.exists('./my_vectordb') and not os.path.exists('./my_vectordb_backup'):
        try:
            shutil.move('./my_vectordb', './my_vectordb_backup')
            st.info("📁 Backed up incompatible database")
        except:
            pass
    
    try:
        chroma_client = chromadb.PersistentClient(path=db_path)
        chroma_collection = chroma_client.get_or_create_collection(name='yt_notes')
        # st.success("✅ ChromaDB fixed and working")
        return gemini_model, chroma_collection, None
    except Exception as e:
        return None, None, f"ChromaDB error: {e}"

def generate_notes(model, transcript, custom_prompt=""):
    try:
        default_prompt = "Extract the key points from the video transcript and provide a comprehensive summary."
        prompt = custom_prompt if custom_prompt.strip() else default_prompt
        response = model.generate_content(prompt + "\n\nTranscript:\n" + transcript)
        return response.text, None
    except Exception as e:
        return None, str(e)

def save_to_database(collection, video_id, notes):
    try:
        collection.upsert(
            documents=[notes],
            ids=[video_id],
            metadatas=[{"timestamp": datetime.now().isoformat(), "video_id": video_id}]
        )
        return True, None
    except Exception as e:
        return False, str(e)

# Initialize services
with st.spinner("🚀 Initializing services..."):
    gemini_model, chroma_collection, error = initialize_services()

if error:
    st.error(f"❌ Failed: {error}")
    st.stop()

# if os.path.exists('./my_vectordb_backup'):
#    st.info("ℹ️ Your old database is backed up as 'my_vectordb_backup'. Starting with fresh database!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    custom_prompt = st.text_area(
        "Custom prompt (optional):",
        placeholder="E.g., 'Create a detailed outline'",
        height=100
    )
    
    try:
        results = chroma_collection.get()
        total_videos = len(results['ids']) if results['ids'] else 0
        st.metric("Videos Processed", total_videos)
    except:
        st.metric("Videos Processed", "0")

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎥 Video Input")
    
    video_input = st.text_input(
        "Enter YouTube URL or Video ID:",
        placeholder="https://www.youtube.com/watch?v=VIDEO_ID or just VIDEO_ID"
    )
    
    if st.button("🚀 Generate Notes", type="primary") and video_input:
        video_id = extract_video_id(video_input)
        
        if not video_id:
            st.error("❌ Invalid YouTube URL or Video ID")
        else:
            st.info(f"📹 Processing: `{video_id}`")
            
            # Get transcript
            with st.spinner("📥 Fetching transcript..."):
                transcript, transcript_error = get_transcript(video_id)
            
            if transcript_error:
                st.error(f"❌ Transcript error: {transcript_error}")
            else:
                st.success("✅ Transcript fetched!")
                
                # Generate notes
                with st.spinner("🤖 Generating notes..."):
                    notes, notes_error = generate_notes(gemini_model, transcript, custom_prompt)
                
                if notes_error:
                    st.error(f"❌ Generation error: {notes_error}")
                else:
                    st.success("✅ Notes generated!")
                    
                    # Save to database
                    # with st.spinner("💾 Saving..."):
                    #    saved, save_error = save_to_database(chroma_collection, video_id, notes)
                     
                    # if save_error:
                    #    st.warning(f"⚠️ Save error: {save_error}")
                    # else:
                    #    st.success("✅ Saved to database!")
                    
                    # Store in session
                    st.session_state.current_notes = notes
                    st.session_state.current_video_id = video_id
                    st.session_state.current_transcript = transcript

with col2:
    st.subheader("📝 Generated Notes")
    
    if hasattr(st.session_state, 'current_notes') and st.session_state.current_notes:
        st.markdown(f"**Video ID:** {st.session_state.current_video_id}")
        
        with st.expander("📖 View Notes", expanded=True):
            st.markdown(st.session_state.current_notes)
        
        col_txt, col_md = st.columns(2)
        with col_txt:
            st.download_button(
                "📄 Download TXT",
                data=st.session_state.current_notes,
                file_name=f"notes_{st.session_state.current_video_id}.txt",
                mime="text/plain"
            )
        
        with col_md:
            st.download_button(
                "📝 Download MD",
                data=f"# Notes\n\n{st.session_state.current_notes}",
                file_name=f"notes_{st.session_state.current_video_id}.md",
                mime="text/markdown"
            )
    else:
        st.info("Generate notes to see them here!")

# Database browser
# st.markdown("---")
#st.subheader("🗃️ Saved Notes")

# try:
#    results = chroma_collection.get(include=["documents", "metadatas"])
    
#    if results['ids']:
#        df_data = []
#        for i, video_id in enumerate(results['ids']):
#            doc = results['documents'][i] if i < len(results['documents']) else ""
#            metadata = results['metadatas'][i] if i < len(results['metadatas']) else {}
            
#            df_data.append({
#                "Video ID": video_id,
#                "Preview": doc[:100] + "..." if len(doc) > 100 else doc,
#                "Saved": metadata.get('timestamp', 'Unknown')
#            })
        
#        df = pd.DataFrame(df_data)
#        st.dataframe(df, use_container_width=True)
        
        # View full notes
#        selected_video = st.selectbox("Select video to view full notes:", [""] + results['ids'])
#        if selected_video:
#            idx = results['ids'].index(selected_video)
#            full_notes = results['documents'][idx]
            
#        with st.expander(f"📖 Full Notes for {selected_video}", expanded=True):
#            st.markdown(full_notes)
#    else:
#        st.info("No saved notes yet. Generate some!")

#except Exception as e:
#    st.error(f"Error loading notes: {e}") 