# Gemini Audio MCP

[![PyPI version](https://img.shields.io/pypi/v/gemini-audio-mcp.svg)](https://pypi.org/project/gemini-audio-mcp/)
[![Downloads](https://img.shields.io/pypi/dm/gemini-audio-mcp.svg)](https://pypi.org/project/gemini-audio-mcp/)
[![Python Versions](https://img.shields.io/pypi/pyversions/gemini-audio-mcp.svg)](https://pypi.org/project/gemini-audio-mcp/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

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

**Multi-Key Fallback:** 
You can provide a single key or a **comma-separated list of keys**. If one key encounters a rate limit or quota issue (e.g., 429 Resource Exhausted), the server will automatically retry the request using the next key in the list.

```json
{
  "env": {
    "GEMINI_API_KEY": "key1,key2,key3"
  }
}
```
## Provided Tools

### `process_audio`
Processes an audio or video file using Google's Gemini models.

**Parameters:**
- `file_path` (string, required): The absolute path to the local audio or video file.
- `prompt` (string, optional): Instructions for the model. Default is *"Please transcribe this audio exactly as spoken."*
- `model_name` (string, optional): The Gemini model to use. Default is `"models/gemini-1.5-flash"`.

## Supported File Formats

Gemini 1.5 Flash natively supports a wide range of audio and video formats via the File API.

**Audio formats:**
- WAV (`audio/wav`)
- MP3 (`audio/mp3`)
- AIFF (`audio/aiff`)
- AAC (`audio/aac`)
- OGG Vorbis (`audio/ogg`)
- FLAC (`audio/flac`)

**Video formats:**
- MP4 (`video/mp4`)
- MPEG (`video/mpeg`)
- MOV (`video/quicktime`)
- AVI (`video/x-msvideo`)
- FLV (`video/x-flv`)
- MPG (`video/mpeg`)
- WEBM (`video/webm`)
- WMV (`video/x-ms-wmv`)
- 3GPP (`video/3gpp`)

> For more details, refer to the official Google Gemini API documentation for [Audio understanding](https://ai.google.dev/gemini-api/docs/audio) and [Video understanding](https://ai.google.dev/gemini-api/docs/vision).

## Release Notes

### v0.1.3
- **Documentation:** Added a comprehensive list of supported audio and video formats.

### v0.1.2
- **Initial Release:** Core processing via `gemini-1.5-flash`.
- **Automatic Fallback:** Added support for multiple API keys in `GEMINI_API_KEY` (comma-separated) to prevent interruptions during rate limits.
- **Native execution:** Works securely out-of-the-box via `uvx`.

## License
Open Source (MIT)
