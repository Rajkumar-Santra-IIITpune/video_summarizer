import streamlit as st
from phi.assistant import Assistant
from phi.llm.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
import os
import re

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("⚠️ GOOGLE_API_KEY not found in environment variables. Please add it to your .env file.")
    st.stop()

st.set_page_config(page_title="YouTube Transcript Summarizer", page_icon="🎥", layout="wide")
st.title("⚡ YouTube Video Summarizer Agent")
st.header("Powered by Gemini + Phidata")

@st.cache_resource
def initialize_assistant():
    try:
        return Assistant(
            name="YouTube Transcript Summarizer",
            llm=Gemini(model="gemini-2.5-pro"), 
            tools=[DuckDuckGo()],
            markdown=True,
        )
    except Exception as e:
        st.error(f"Failed to initialize assistant: {e}")
        return None

assistant = initialize_assistant()

def extract_video_id(url: str):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        
        try:
            transcript = transcript_list.find_transcript(['en'])
            return transcript.fetch(), "English"
        except:
            pass
        
        try:
            transcript = transcript_list.find_manually_created_transcript()
            return transcript.fetch(), transcript.language
        except:
            pass
        
        try:
            transcript = transcript_list.find_generated_transcript(['en'])
            return transcript.fetch(), "English (auto-generated)"
        except:
            pass
        
        for transcript in transcript_list:
            try:
                return transcript.fetch(), transcript.language
            except:
                continue
        
        return None, None
        
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except NoTranscriptFound:
        raise Exception("No transcripts found for this video")
    except VideoUnavailable:
        raise Exception("Video is unavailable or private")
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}")

col1, col2 = st.columns([2, 1])

with col1:
    yt_link = st.text_input(
        "Enter a YouTube video link:", 
        placeholder="https://www.youtube.com/watch?v=... or https://youtu.be/...",
        help="Paste any YouTube video URL"
    )

with col2:
    st.write("")
    st.write("")
    summary_type = st.selectbox(
        "Summary Type:",
        ["Comprehensive", "Key Points", "Quick Overview", "Detailed Analysis"]
    )

user_query = st.text_area(
    "Additional instructions (optional):", 
    placeholder="E.g., Focus on technical details, Extract action items, Analyze the speaker's tone, etc.",
    height=100
)

if st.button("🔍 Analyze Video", type="primary", use_container_width=True):
    if not yt_link:
        st.warning("⚠️ Please enter a YouTube video link.")
    elif not assistant:
        st.error("❌ Assistant initialization failed. Please check your API key.")
    else:
        try:
            with st.spinner("🔄 Extracting video ID..."):
                video_id = extract_video_id(yt_link)
                if not video_id:
                    st.error("❌ Invalid YouTube link. Please check the URL and try again.")
                    st.stop()
                st.info(f"✓ Video ID: {video_id}")
            
            with st.spinner("🔄 Fetching transcript..."):
                try:
                    transcript_data, language = get_transcript(video_id)
                    if not transcript_data:
                        st.error("❌ No transcript available for this video.")
                        st.stop()
                    
                    text = " ".join([t.text for t in transcript_data])
                    
                    if not text.strip():
                        st.error("❌ Transcript is empty.")
                        st.stop()
                    st.success(f"✅ Transcript fetched! ({len(text.split())} words, Language: {language})")
                    
                except Exception as e:
                    st.error(f"❌ Could not fetch transcript: {str(e)}")
                    st.stop()
                
            st.video(yt_link)
            
            summary_instructions = {
                "Comprehensive": "Provide a detailed, comprehensive summary covering all major topics and subtopics.",
                "Key Points": "Extract and list the key points and main takeaways in bullet format.",
                "Quick Overview": "Provide a brief, concise overview in 3-4 sentences.",
                "Detailed Analysis": "Provide an in-depth analysis including themes, arguments, and insights."
            }
            
            MAX_CHARS = 30000
            if len(text) > MAX_CHARS:
                text = text[:MAX_CHARS]
                st.warning(f"Transcript truncated to {MAX_CHARS} characters for processing.")
            
            prompt = f"""You are an expert video content analyst. 
**Task:** {summary_instructions[summary_type]}
**Additional User Instructions:** {user_query if user_query else "None"}
**Video Transcript (Language: {language}):**
{text}
Please provide a well-structured response with clear sections and formatting."""

            with st.spinner("🤖 Generating analysis with AI..."):
                response_stream = assistant.run(prompt)
            
            st.subheader("📘 Summary & Insights")
            
            st.write_stream(response_stream)
            
            with st.expander("📊 Transcript Statistics"):
                st.write(f"**Language:** {language}")
                st.write(f"**Total Words:** {len(text.split())}")
                st.write(f"**Total Characters:** {len(text)}")
                st.write(f"**Estimated Reading Time:** {len(text.split()) // 200} minutes")
                
            with st.expander("📥 Download Transcript"):
                st.download_button(
                    label="Download as TXT",
                    data=text,
                    file_name=f"transcript_{video_id}.txt",
                    mime="text/plain"
                )

        except Exception as e:
            st.error(f"❌ An unexpected error occurred: {str(e)}")
            with st.expander("🔍 Error Details"):
                st.code(str(e))

with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This app uses AI to analyze and summarize YouTube videos by:
    1. Extracting the video transcript
    2. Processing it with Gemini AI
    3. Generating intelligent summaries
    
    **Requirements:**
    - Video must have captions/subtitles enabled
    - GOOGLE_API_KEY in .env file
    """)
    
    st.header("📝 Test These Working Videos")
    st.markdown("""
    Try videos with confirmed captions:
    - TED Talks
    - Educational channels (Khan Academy, Crash Course)
    - News channels (CNN, BBC)
    - Most professionally produced content
    """)
    
    st.header("🔧 Installation")
    st.code("pip install streamlit phidata phi-llm-google phi-tools-duckduckgo youtube-transcript-api python-dotenv", language="bash")
    
    st.header("💡 Common Issues")
    st.markdown("""
    - **No transcript found**: Video lacks captions
    - **Video unavailable**: Check if video is private/restricted
    - **API Error**: Check your GOOGLE_API_KEY
    """)

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    .stTextArea textarea {
        font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)