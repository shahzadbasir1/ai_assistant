import json
import os
import requests
from datetime import datetime


# =========================
# TOOL FUNCTIONS
# =========================

def calculate(expression):
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return str(e)


def web_search(query):
    api_key = os.getenv("SERPAPI_KEY")

    url = "https://serpapi.com/search.json"
    params = {
        "q": query,
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    try:
        return data["organic_results"][0]["snippet"]
    except:
        return "No results found"


def analyze_data(data_string, operation):
    try:
        data = json.loads(data_string)

        if isinstance(data, list):
            values = [float(x) for x in data]
        elif isinstance(data, dict):
            values = [float(v) for v in data.values()]
        else:
            return "Invalid data"

        if operation == "sum":
            return str(sum(values))
        elif operation == "average":
            return str(sum(values) / len(values))
        elif operation == "max":
            return str(max(values))
        elif operation == "min":
            return str(min(values))
        else:
            return "Unknown operation"

    except Exception as e:
        return str(e)


def write_email(purpose, recipient, tone, research_topic=None):
    research = ""
    if research_topic:
        research = web_search(research_topic)

    return f"""
Subject: {purpose}

Dear {recipient},

I hope you are doing well.

{purpose}

{research}

Please let me know if you have any questions.

Best regards,
Your Name
"""


def format_report(report_type, data, period):
    return f"{period} {report_type} Report generated on {datetime.now()}"

def generate_report(report_type, data_string, period):
    try:
        data = json.loads(data_string)

        if isinstance(data, dict):
            values = list(data.values())
            labels = list(data.keys())
        else:
            values = data
            labels = None

        total = sum(values)
        avg = total / len(values)
        max_val = max(values)

        best_label = labels[values.index(max_val)] if labels else "N/A"

        report = f"""
============================================
{period.upper()} {report_type.upper()} REPORT
============================================
Date: {datetime.now().strftime("%B %d, %Y")}

EXECUTIVE SUMMARY
Total performance is {total} with an average of {avg:.2f}.

KEY METRICS
- Total: {total}
- Average: {avg:.2f}
- Best Value: {max_val} ({best_label})

ANALYSIS
The data shows overall performance trends with variation across periods.

RECOMMENDATIONS
1. Focus on high-performing segments
2. Improve underperforming areas
3. Monitor trends closely

============================================
"""
        return report

    except Exception as e:
        return str(e)

def get_weather(city):
    """Mock weather lookup"""

    weather_data = {
        "Islamabad": "Sunny, 34°C",
        "Lahore": "Hot, 39°C",
        "Karachi": "Humid, 32°C",
        "New York": "Cloudy, 20°C",
        "London": "Rainy, 15°C"
    }

    return weather_data.get(city, f"Weather data for {city} not found")

def summarize_meeting(notes, date, attendees=None):

    lines = notes.split(".")
    summary = lines[0].strip()

    action_items = []
    decisions = []

    for line in lines:
        line = line.strip().lower()
        if "will" in line or "to" in line:
            action_items.append(line)
        if "approved" in line or "decided" in line:
            decisions.append(line)

    return f"""
===========================================
MEETING SUMMARY
===========================================
Date: {date}
Attendees: {attendees if attendees else "N/A"}

SUMMARY
{summary}

KEY POINTS
- {notes}

DECISIONS
{chr(10).join([f"{i+1}. {d}" for i, d in enumerate(decisions)])}

ACTION ITEMS
{chr(10).join([f"- {a}" for a in action_items])}

===========================================
"""    
# =========================
# TOOL DEFINITIONS (FOR OPENAI)
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"}
                },
                "required": ["expression"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for business info",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "analyze_data",
            "description": "Analyze business data",
            "parameters": {
                "type": "object",
                "properties": {
                    "data_string": {"type": "string"},
                    "operation": {"type": "string"}
                },
                "required": ["data_string", "operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_email",
            "description": "Write professional business emails",
            "parameters": {
                "type": "object",
                "properties": {
                    "purpose": {"type": "string"},
                    "recipient": {"type": "string"},
                    "tone": {"type": "string"},
                    "research_topic": {"type": "string"}
                },
                "required": ["purpose", "recipient", "tone"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "generate_report",
        "description": "Generate business reports",
        "parameters": {
            "type": "object",
            "properties": {
                "report_type": {"type": "string"},
                "data_string": {"type": "string"},
                "period": {"type": "string"}
            },
            "required": ["report_type", "data_string", "period"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "summarize_meeting",
        "description": "Summarize meeting notes",
        "parameters": {
            "type": "object",
            "properties": {
                "notes": {"type": "string"},
                "date": {"type": "string"},
                "attendees": {"type": "string"}
            },
            "required": ["notes", "date"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get the current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The city name"
                }
            },
            "required": ["city"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "draft_client_communication",
        "description": "Draft client communication",
        "parameters": {
            "type": "object",
            "properties": {
                "comm_type": {"type": "string"},
                "client": {"type": "string"},
                "context": {"type": "string"},
                "tone": {"type": "string"}
            },
            "required": ["comm_type", "client", "context", "tone"]
        }
    }
}    
]


# =========================
# FUNCTION MAP
# =========================

function_map = {
    "calculate": calculate,
    "web_search": web_search,
    "analyze_data": analyze_data,
    "write_email": write_email
}
function_map.update({
    "generate_report": generate_report,
    "summarize_meeting": summarize_meeting
})