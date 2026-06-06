from mcp.server.fastmcp import FastMCP
import os
import google.generativeai as genai
import time

mcp = FastMCP("Gemini Audio MCP")

@mcp.tool()
def process_audio(
    file_path: str,
    prompt: str = "Please transcribe this audio exactly as spoken.",
    model_name: str = "models/gemini-1.5-flash"
) -> str:
    """
    Processes an audio or video file using Google's Gemini multimodal models.
    Useful for high-quality transcription, summarization, or reasoning over audio/video files.
    
    Args:
        file_path: The absolute path to the local audio/video file.
        prompt: Instructions for the model (e.g., 'Transcribe this', 'Summarize this in Polish').
        model_name: The Gemini model to use (default: models/gemini-1.5-flash).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return "Error: GEMINI_API_KEY environment variable is not set."
    
    if not os.path.isfile(file_path):
        return f"Error: File not found at path: {file_path}"

    genai.configure(api_key=api_key)
    
    sample_file = None
    try:
        # Upload the file
        sample_file = genai.upload_file(path=file_path)
        
        # Wait for the file to be processed
        while sample_file.state.name == "PROCESSING":
            time.sleep(2)
            sample_file = genai.get_file(sample_file.name)
            
        if sample_file.state.name == "FAILED":
            return "Error: File processing failed on Gemini servers."
            
        # Generate content
        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content([sample_file, prompt])
        
        return response.text
        
    except Exception as e:
        return f"Error processing file: {str(e)}"
    finally:
        # Always cleanup the uploaded file
        if sample_file:
            try:
                genai.delete_file(sample_file.name)
            except Exception:
                pass

def main():
    mcp.run()

if __name__ == "__main__":
    main()
