# Agentes de IA para Vertex AI Agent Engine

## SKILLS required

- google-adk-python: `npx skills add https://github.com/cnemri/google-genai-skills --skill google-adk-python`
-

## MCP servers required
- antigravity:
```json
{
  "mcpServers": {
    "google-developer-knowledge": {
      "serverUrl": "https://developerknowledge.googleapis.com/mcp",
      "headers": {
        "X-Goog-Api-Key": "AIza..."
      }
    }
  }
}
```
- claude ai
```bash
claude mcp add --transport http google-developer-knowledge https://developerknowledge.googleapis.com/mcp --header "X-Goog-Api-Key: AIza..."
claude mcp list
claude mcp get google-developer-knowledge

claude mcp remove google-developer-knowledge
```
