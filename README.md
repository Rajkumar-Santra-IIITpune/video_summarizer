# YouTube Video Summarizer

A Streamlit application that uses AI to analyze and summarize YouTube videos by extracting their transcripts and generating intelligent summaries using Google's Gemini 2.5 Pro model.

## Features

- **AI-Powered Summarization**: Leverages Gemini 2.5 Pro for high-quality video analysis
- **Multiple Summary Types**: Choose from Comprehensive, Key Points, Quick Overview, or Detailed Analysis
- **Custom Instructions**: Add personalized instructions for tailored summaries
- **Transcript Extraction**: Automatically fetches YouTube video transcripts (supports multiple languages)
- **Transcript Download**: Download full transcripts as TXT files
- **Statistics Display**: View transcript statistics including word count, language, and reading time
- **Error Handling**: Robust handling of videos without transcripts, private videos, and API errors
- **Web Search Integration**: Uses DuckDuckGo for additional context when needed

## Prerequisites

- Python 3.8+
- Google Generative AI API key (Gemini)
- YouTube videos with captions/subtitles enabled

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/video-summarizer.git
   cd video-summarizer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. Run the Streamlit app:

   ```bash
   streamlit run app.py
   ```

2. Open your browser to the provided URL (usually `http://localhost:8501`).

3. Enter a YouTube video URL in the input field.

4. Select your preferred summary type from the dropdown.

5. (Optional) Add custom instructions in the text area.

6. Click "🔍 Analyze Video" to generate the summary.

## Example Videos to Test

Try these types of videos that typically have good caption support:

- TED Talks
- Educational content (Khan Academy, Crash Course)
- News channels (CNN, BBC, Reuters)
- Tech conference talks
- Professional tutorials

## Project Structure

```
video_summarizer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not committed)
└── README.md             # This file
```

## Dependencies

- streamlit: Web app framework
- phidata: AI assistant framework
- phi-llm-google: Google Gemini integration
- phi-tools-duckduckgo: Web search tool
- youtube-transcript-api: YouTube transcript extraction
- python-dotenv: Environment variable management

## Configuration

The application requires the following environment variable:

- `GOOGLE_API_KEY`: Your Google Generative AI API key for Gemini model access

## How It Works

1. **URL Processing**: Extracts video ID from YouTube URL
2. **Transcript Fetching**: Retrieves available transcripts (English preferred, falls back to other languages)
3. **AI Analysis**: Sends transcript to Gemini 2.5 Pro with user-specified summary type and instructions
4. **Response Generation**: AI generates structured summary based on the content
5. **Display**: Shows summary, statistics, and download options

## Common Issues

- **No transcript found**: Video lacks captions/subtitles
- **Video unavailable**: Video is private, deleted, or region-restricted
- **API Error**: Check your GOOGLE_API_KEY is valid and has quota
- **Long videos**: Transcripts are truncated to 30,000 characters for processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
