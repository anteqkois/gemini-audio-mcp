from mcp.server.fastmcp import FastMCP
import os
import google.generativeai as genai
import time

mcp = FastMCP("Gemini Audio MCP")

def get_api_keys():
    keys_str = os.environ.get("GEMINI_API_KEY")
    if keys_str:
        return [k.strip() for k in keys_str.split(",") if k.strip()]
    return []

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
                    Supported models include:
                    - models/gemini-1.5-flash
                    - models/gemini-1.5-pro
                    - models/gemini-1.5-flash-8b
                    - models/gemini-2.0-flash-exp
    """
    api_keys = get_api_keys()
    if not api_keys:
        return "Error: GEMINI_API_KEY environment variable is not set."
    
    if not os.path.isfile(file_path):
        return f"Error: File not found at path: {file_path}"

    last_error = None
    
    for attempt, api_key in enumerate(api_keys):
        try:
            genai.configure(api_key=api_key)
            sample_file = None
            
            # Upload the file
            sample_file = genai.upload_file(path=file_path)
            
            # Wait for the file to be processed
            while sample_file.state.name == "PROCESSING":
                time.sleep(2)
                sample_file = genai.get_file(sample_file.name)
                
            if sample_file.state.name == "FAILED":
                raise Exception("File processing failed on Gemini servers.")
                
            # Generate content
            model = genai.GenerativeModel(model_name=model_name)
            response = model.generate_content([sample_file, prompt])
            
            # Cleanup and return
            try:
                genai.delete_file(sample_file.name)
            except Exception:
                pass
                
            return response.text
            
        except Exception as e:
            last_error = str(e)
            if 'sample_file' in locals() and sample_file:
                try:
                    genai.delete_file(sample_file.name)
                except Exception:
                    pass
            
            if attempt < len(api_keys) - 1:
                time.sleep(1)
                continue
            else:
                return f"Error processing file after trying {len(api_keys)} key(s). Last error: {last_error}"

def main():
    mcp.run()

if __name__ == "__main__":
    main()
