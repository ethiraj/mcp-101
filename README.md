# 🌦️ Open Meteo MCP Weather Tool

Give your LLM or agent real-time weather capabilities using the [Open Meteo API](https://open-meteo.com) and [FastMCP](https://gofastmcp.com) — a Pythonic framework for creating tools that follow the Model Context Protocol (MCP).

---

## 🚀 What It Does
This project exposes a tool called `get_current_weather(location: str)` that:
- Geocodes the location to latitude and longitude
- Fetches current weather data
- Returns a structured response in Pydantic format

Perfect for Claude, GPT, or any agent framework that understands structured tools.

---

## 🛠️ Tech Stack
- **FastMCP**: Defines the MCP server and exposes the tool
- **Python**: Core language
- **httpx**: Async API calls
- **Pydantic**: Typed schema validation for structured responses
- **Open Meteo API**: Real-time weather + geocoding

---

## 📦 Folder Structure
```
.
├── open_meteo_mcp.py        # FastMCP server exposing the weather tool
├── mcp_client_test.py       # Simple FastMCP client that simulates an LLM call
├── architecture_diagram.png # System diagram showing data flow
```

---

## 📄 How to Run

### 1. Install dependencies
```bash
pip install fastmcp httpx
```

### 2. Run the server
```bash
python open_meteo_mcp.py
```

### 3. Call the tool via client
```bash
python mcp_client_test.py
```

---

## ✅ Sample Output
```
{
  "location": "Houston",
  "latitude": 29.76328,
  "longitude": -95.36327,
  "current_temperature": 77.1,
  "temperature_unit": "°F",
  "weather_description": "Overcast",
  "current_wind_speed": 10.9,
  "wind_speed_unit": "mp/h",
  "error": null
}

```

---

## 🔗 How It Works

1. LLM or agent triggers `get_current_weather(location)`
2. FastMCP server geocodes the location
3. Calls Open Meteo to fetch real-time weather
4. Maps the response to a `WeatherResponse` Pydantic model
5. Returns structured output

![Architecture Diagram](Screenshot%20from%202025-04-20%2020-58-49.png)

---

## 💬 Why Use MCP?
MCP (Model Context Protocol) is a way to expose structured tools to LLMs — like OpenAI function calling, but portable.

- 🚀 Schema-aware for safety
- 🧩 Easy to plug into Claude, LangChain, CrewAI, etc.
- ⛓️ Modular and chainable with other tools

---

## 🤖 Next Step
Stay tuned for **Part 2**: Integrating this with an actual LLM (Claude, OpenAI, or LangChain Agent).

Or drop your idea for what **real-time tool** I should build next!

---

## 📬 Connect
Made by Ethiraj Krishnamanaidu.
Let’s talk GenAI, agents, and real-time tools → [LinkedIn](https://www.linkedin.com/in/ethiraj-krishnamanaidu/)

