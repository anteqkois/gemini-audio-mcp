# Gemini Audio MCP

A dedicated [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server that provides high-quality audio and video transcription, summarization, and reasoning using Google's native multimodal Gemini models (`gemini-1.5-flash`).

## Why this exists?

Most AI assistants (like Claude Code, Cursor, or local agents) rely on text inputs. If you want them to transcribe or process audio, you usually have to run local STT (Speech-to-Text) models like Whisper, which can be inaccurate, slow, or resource-heavy. 

This MCP server connects your AI assistant directly to **Google's Gemini 1.5 Flash multimodal API**. Instead of just transcribing text, the file is processed natively by Gemini, allowing you to ask complex queries about the audio or video content (e.g., "Transcribe this", "Extract the action items", "Translate this Polish audio to an English summary").

## Features
- **Native Multimodal Support**: Uses `gemini-1.5-flash` to process the audio/video file directly.
- **Fast and Cheap**: `gemini-1.5-flash` provides exceptional transcription quality without burning through API limits or hallucinating wildly.
- **Custom Prompts**: Don't just transcribe – tell the model exactly what to extract from the audio.

## Installation & Usage

You can use this MCP server with any compatible client (Claude Code, Cursor, Windsurf, etc.) using `uvx`.

### 1. Claude Code
Run the following command to add the server to Claude Code globally:
```bash
claude mcp add gemini-audio uvx gemini-audio-mcp
```

### 2. Cursor / Windsurf / Generic MCP Client
Add the following configuration to your client's MCP settings file (usually `settings.json` or `claude.json`):

```json
{
  "mcpServers": {
    "gemini-audio": {
      "command": "uvx",
      "args": ["gemini-audio-mcp"],
      "env": {
        "GEMINI_API_KEY": "your_gemini_api_key_here"
      }
    }
  }
}
```

## Environment Variables

The server requires a Google Gemini API key to function. 
Set the `GEMINI_API_KEY` environment variable in your terminal before launching your agent, or define it in your MCP configuration file.

## Provided Tools

### `process_audio`
Processes an audio or video file using Google's Gemini models.

**Parameters:**
- `file_path` (string, required): The absolute path to the local audio or video file.
- `prompt` (string, optional): Instructions for the model. Default is *"Please transcribe this audio exactly as spoken."*
- `model_name` (string, optional): The Gemini model to use. Default is `"models/gemini-1.5-flash"`.

## License
Open Source (MIT)
