import datetime
import json
import random
import streamlit as st

# ==========================================
# 1. PAGE CONFIGURATION & DYNAMIC THEME CSS
# ==========================================
st.set_page_config(
    page_title="SPORTSLE",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

if "sport" not in st.session_state:
    st.session_state.sport = "Cricket"

# Theme colors per sport
if st.session_state.sport == "F1":
    accent_color = "#e10600"
    accent_hover = "#b30500"
elif st.session_state.sport == "Football":
    accent_color = "#10b981"
    accent_hover = "#059669"
else:
    accent_color = "#3b82f6"
    accent_hover = "#2563eb"

# 4. INITIALIZE THEME IN SESSION STATE (Fixes the AttributeError!)
if "theme" not in st.session_state:
    st.session_state.theme = {
        "bg": "#0e1117",          # Main app background
        "text": "#ffffff",        # Text color
        "card_bg": "#1e2638",     # Grid card background
        "card_border": "#2e3b52", # Grid card border
        "accent": accent_color,   # Dynamic sport accent color
        "accent_hover": accent_hover
    }
else:
    # Update accent color if sport changed during session
    st.session_state.theme["accent"] = accent_color
    st.session_state.theme["accent_hover"] = accent_hover


# 5. RENDER ALL CSS (Mobile Responsive + Dynamic Theme)
st.markdown(
    f"""
    <style>
    /* ==========================================
       1. CORE THEME & LAYOUT STYLES
       ========================================== */
    header[data-testid="stHeader"] {{
        background: transparent !important;
    }}

    .stApp {{
        background-color: {st.session_state.theme['bg']} !important;
        color: {st.session_state.theme['text']} !important;
    }}

    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-bottom: 5px;
    }}

    .main-title {{
        font-family: 'Aptos', 'Trebuchet MS', sans-serif;
        font-size: 2.5rem;
        font-weight: 900;
        letter-spacing: 2px;
        color: {st.session_state.theme['text']} !important;
        margin: 0;
        line-height: 1;
    }}

    .logo-icon {{
        font-size: 2.5rem;
        line-height: 1;
    }}

    /* Buttons */
    div.stButton > button {{
        background-color: {st.session_state.theme['accent']} !important;
        color: white !important;
        border: none !important;
        width: 100% !important;
        transition: all 0.2s ease-in-out !important;
    }}

    div.stButton > button:hover {{
        background-color: {st.session_state.theme['accent_hover']} !important;
    }}

    /* ==========================================
       2. SCROLLABLE GRID CONTAINER
       ========================================== */
    .grid-wrapper {{
        width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        padding-bottom: 10px;
    }}

    .grid-content {{
        min-width: 650px; /* Ensures grid stays readable on mobile */
    }}

    /* Grid Cards & Headers */
    .grid-header {{
        background-color: {st.session_state.theme['card_bg']};
        color: {st.session_state.theme['text']};
        padding: 10px 4px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        font-size: 0.8rem;
        border: 1px solid {st.session_state.theme['card_border']};
        margin-bottom: 6px;
        text-transform: uppercase;
    }}

    .grid-card-neutral {{
        background-color: {st.session_state.theme['card_bg']};
        color: {st.session_state.theme['text']};
        padding: 10px 4px;
        border-radius: 6px;
        text-align: center;
        font-weight: 600;
        font-size: 0.85rem;
        border: 1px solid {st.session_state.theme['card_border']};
        margin-bottom: 6px;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .grid-card-correct {{
        background-color: #2e7d32 !important;
        color: #ffffff !important;
        padding: 10px 4px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 6px;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .grid-card-wrong {{
        background-color: #c62828 !important;
        color: #ffffff !important;
        padding: 10px 4px;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        font-size: 0.85rem;
        margin-bottom: 6px;
        min-height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    /* ==========================================
       3. MOBILE RESPONSIVE TWEAKS
       ========================================== */
    .stAppViewContainer {{
        overflow-x: hidden !important;
    }}

    @media screen and (max-width: 768px) {{
        .block-container {{
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
        }}

        .main-title {{
            font-size: 1.6rem !important;
        }}

        .logo-icon {{
            font-size: 1.6rem !important;
        }}

        div.stButton > button {{
            height: 44px !important;
            font-size: 1rem !important;
        }}
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================
# 2. DATABASES
# ==========================================
CRICKET_PLAYERS = [
    {
        "name": "Sachin Tendulkar",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 53,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "MS Dhoni",
        "Country": "India",
        "status": "Active",
        "Role": "WK",
        "Batting Hand": "Right",
        "Age": 45,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Virat Kohli",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 37,
        "Franchise": "Royal Challengers Bengaluru",
    },
    {
        "name": "Rohit Sharma",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 39,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "Kapil Dev",
        "Country": "India",
        "status": "Retired",
        "Role": "ALL",
        "Batting Hand": "Right",
        "Age": 67,
        "Franchise": "Haryana",
    },
    {
        "name": "Rahul Dravid",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 53,
        "Franchise": "Rajasthan Royals",
    },
    {
        "name": "Sourav Ganguly",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 54,
        "Franchise": "Kolkata Knight Riders",
    },
    {
        "name": "Sunil Gavaskar",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 77,
        "Franchise": "Mumbai",
    },
    {
        "name": "Anil Kumble",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 55,
        "Franchise": "Royal Challengers Bengaluru",
    },
    {
        "name": "Jasprit Bumrah",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 32,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "Ravichandran Ashwin",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Right",
        "Age": 39,
        "Franchise": "Rajasthan Royals",
    },
    {
        "name": "Ravindra Jadeja",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Left",
        "Age": 37,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Yuvraj Singh",
        "Country": "India",
        "status": "Retired",
        "Role": "ALL",
        "Batting Hand": "Left",
        "Age": 44,
        "Franchise": "Sunrisers Hyderabad",
    },
    {
        "name": "Virender Sehwag",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 47,
        "Franchise": "Delhi Capitals",
    },
    {
        "name": "Zaheer Khan",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 47,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "VVS Laxman",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 51,
        "Franchise": "Deccan Chargers",
    },
    {
        "name": "Harbhajan Singh",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 46,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "Shikhar Dhawan",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 40,
        "Franchise": "Punjab Kings",
    },
    {
        "name": "Rishabh Pant",
        "Country": "India",
        "status": "Active",
        "Role": "WK",
        "Batting Hand": "Left",
        "Age": 28,
        "Franchise": "Delhi Capitals",
    },
    {
        "name": "Hardik Pandya",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Right",
        "Age": 32,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "KL Rahul",
        "Country": "India",
        "status": "Active",
        "Role": "WK",
        "Batting Hand": "Right",
        "Age": 34,
        "Franchise": "Lucknow Super Giants",
    },
    {
        "name": "Shubman Gill",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 26,
        "Franchise": "Gujarat Titans",
    },
    {
        "name": "Suryakumar Yadav",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 35,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "Mohammed Shami",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 35,
        "Franchise": "Gujarat Titans",
    },
    {
        "name": "Mohammed Siraj",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 32,
        "Franchise": "Royal Challengers Bengaluru",
    },
    {
        "name": "Gautam Gambhir",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 44,
        "Franchise": "Kolkata Knight Riders",
    },
    {
        "name": "Suresh Raina",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 39,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Javagal Srinath",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 56,
        "Franchise": "Karnataka",
    },
    {
        "name": "Mohammad Azharuddin",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 63,
        "Franchise": "Hyderabad",
    },
    {
        "name": "Dilip Vengsarkar",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 70,
        "Franchise": "Mumbai",
    },
    {
        "name": "Cheteshwar Pujara",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 38,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Ajinkya Rahane",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 38,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Ishant Sharma",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 37,
        "Franchise": "Delhi Capitals",
    },
    {
        "name": "Bhuvneshwar Kumar",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 36,
        "Franchise": "Sunrisers Hyderabad",
    },
    {
        "name": "Kuldeep Yadav",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Left",
        "Age": 31,
        "Franchise": "Delhi Capitals",
    },
    {
        "name": "Yuzvendra Chahal",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 36,
        "Franchise": "Rajasthan Royals",
    },
    {
        "name": "Shreyas Iyer",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 31,
        "Franchise": "Kolkata Knight Riders",
    },
    {
        "name": "Yashasvi Jaiswal",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 24,
        "Franchise": "Rajasthan Royals",
    },
    {
        "name": "Axar Patel",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Left",
        "Age": 32,
        "Franchise": "Delhi Capitals",
    },
    {
        "name": "Irfan Pathan",
        "Country": "India",
        "status": "Retired",
        "Role": "ALL",
        "Batting Hand": "Left",
        "Age": 41,
        "Franchise": "Sunrisers Hyderabad",
    },
    {
        "name": "Ashish Nehra",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 47,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Dinesh Karthik",
        "Country": "India",
        "status": "Retired",
        "Role": "WK",
        "Batting Hand": "Right",
        "Age": 41,
        "Franchise": "Royal Challengers Bengaluru",
    },
    {
        "name": "Parthiv Patel",
        "Country": "India",
        "status": "Retired",
        "Role": "WK",
        "Batting Hand": "Left",
        "Age": 41,
        "Franchise": "Mumbai Indians",
    },
    {
        "name": "RP Singh",
        "Country": "India",
        "status": "Retired",
        "Role": "BOWL",
        "Batting Hand": "Right",
        "Age": 40,
        "Franchise": "Deccan Chargers",
    },
    {
        "name": "Robin Uthappa",
        "Country": "India",
        "status": "Retired",
        "Role": "BAT",
        "Batting Hand": "Right",
        "Age": 40,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Kedar Jadhav",
        "Country": "India",
        "status": "Retired",
        "Role": "ALL",
        "Batting Hand": "Right",
        "Age": 41,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Washington Sundar",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Left",
        "Age": 26,
        "Franchise": "Sunrisers Hyderabad",
    },
    {
        "name": "Shardul Thakur",
        "Country": "India",
        "status": "Active",
        "Role": "ALL",
        "Batting Hand": "Right",
        "Age": 34,
        "Franchise": "Chennai Super Kings",
    },
    {
        "name": "Arshdeep Singh",
        "Country": "India",
        "status": "Active",
        "Role": "BOWL",
        "Batting Hand": "Left",
        "Age": 27,
        "Franchise": "Punjab Kings",
    },
    {
        "name": "Rinku Singh",
        "Country": "India",
        "status": "Active",
        "Role": "BAT",
        "Batting Hand": "Left",
        "Age": 28,
        "Franchise": "Kolkata Knight Riders",
    },

    # Australia
    {"name": "Sir Donald Bradman", "Country": "Australia", "status": "Deceased", "Role": "BAT", "Batting Hand": "Right", "Age": "N/A", "Franchise": "New South Wales / South Australia"},
    {"name": "Shane Warne", "Country": "Australia", "status": "Deceased", "Role": "BOWL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Rajasthan Royals"},
    {"name": "Ricky Ponting", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 51, "Franchise": "Mumbai Indians"},
    {"name": "Steve Waugh", "Country": "Australia", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 61, "Franchise": "New South Wales"},
    {"name": "Glenn McGrath", "Country": "Australia", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 56, "Franchise": "Delhi Capitals"},
    {"name": "Adam Gilchrist", "Country": "Australia", "status": "Retired", "Role": "WK", "Batting Hand": "Left", "Age": 54, "Franchise": "Deccan Chargers / Punjab Kings"},
    {"name": "Allan Border", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 70, "Franchise": "Queensland"},
    {"name": "Steve Smith", "Country": "Australia", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 37, "Franchise": "Sydney Sixers / Rajasthan Royals"},
    {"name": "David Warner", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 39, "Franchise": "Sunrisers Hyderabad / Delhi Capitals"},
    {"name": "Pat Cummins", "Country": "Australia", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 33, "Franchise": "Sunrisers Hyderabad"},
    {"name": "Mitchell Starc", "Country": "Australia", "status": "Active", "Role": "BOWL", "Batting Hand": "Left", "Age": 36, "Franchise": "Kolkata Knight Riders"},
    {"name": "Dennis Lillee", "Country": "Australia", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 77, "Franchise": "Western Australia"},
    {"name": "Greg Chappell", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 77, "Franchise": "South Australia / Queensland"},
    {"name": "Matthew Hayden", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 54, "Franchise": "Chennai Super Kings"},
    {"name": "Michael Clarke", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 45, "Franchise": "Pune Warriors India"},
    {"name": "Brett Lee", "Country": "Australia", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 49, "Franchise": "Kolkata Knight Riders / Punjab Kings"},
    {"name": "Mitchell Johnson", "Country": "Australia", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 44, "Franchise": "Mumbai Indians / Perth Scorchers"},
    {"name": "Shane Watson", "Country": "Australia", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 45, "Franchise": "Rajasthan Royals / Chennai Super Kings"},
    {"name": "Nathan Lyon", "Country": "Australia", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 38, "Franchise": "Melbourne Renegades"},
    {"name": "Travis Head", "Country": "Australia", "status": "Active", "Role": "BAT", "Batting Hand": "Left", "Age": 32, "Franchise": "Sunrisers Hyderabad / Adelaide Strikers"},
    {"name": "Josh Hazlewood", "Country": "Australia", "status": "Active", "Role": "BOWL", "Batting Hand": "Left", "Age": 35, "Franchise": "Royal Challengers Bengaluru"},
    {"name": "Mark Waugh", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 61, "Franchise": "New South Wales"},
    {"name": "Justin Langer", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 55, "Franchise": "Western Australia"},
    {"name": "Ian Chappell", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 82, "Franchise": "South Australia"},
    {"name": "Neil Harvey", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 97, "Franchise": "Victoria / New South Wales"},
    {"name": "Keith Miller", "Country": "Australia", "status": "Deceased", "Role": "ALL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Victoria / New South Wales"},
    {"name": "Michael Hussey", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 51, "Franchise": "Chennai Super Kings / Mumbai Indians"},
    {"name": "Aaron Finch", "Country": "Australia", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 39, "Franchise": "Melbourne Renegades / KKR"},
    {"name": "Usman Khawaja", "Country": "Australia", "status": "Active", "Role": "BAT", "Batting Hand": "Left", "Age": 39, "Franchise": "Brisbane Heat"},
    {"name": "Glenn Maxwell", "Country": "Australia", "status": "Active", "Role": "ALL", "Batting Hand": "Right", "Age": 37, "Franchise": "Royal Challengers Bengaluru / Melbourne Stars"},

    # England
    {"name": "Sir Alastair Cook", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 41, "Franchise": "Essex"},
    {"name": "Joe Root", "Country": "England", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 35, "Franchise": "Rajasthan Royals / Yorkshire"},
    {"name": "James Anderson", "Country": "England", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 43, "Franchise": "Lancashire"},
    {"name": "Stuart Broad", "Country": "England", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 40, "Franchise": "Kings XI Punjab / Nottinghamshire"},
    {"name": "Ben Stokes", "Country": "England", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 35, "Franchise": "Chennai Super Kings / Durham"},
    {"name": "Sir Ian Botham", "Country": "England", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 70, "Franchise": "Somerset / Worcestershire"},
    {"name": "Kevin Pietersen", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 46, "Franchise": "Royal Challengers Bengaluru / Delhi Capitals"},
    {"name": "Jos Buttler", "Country": "England", "status": "Active", "Role": "WK", "Batting Hand": "Right", "Age": 35, "Franchise": "Rajasthan Royals / Lancashire"},
    {"name": "Sir Geoffrey Boycott", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 85, "Franchise": "Yorkshire"},
    {"name": "Sir Len Hutton", "Country": "England", "status": "Deceased", "Role": "BAT", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Yorkshire"},
    {"name": "W. G. Grace", "Country": "England", "status": "Deceased", "Role": "ALL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Gloucestershire"},
    {"name": "Andrew Flintoff", "Country": "England", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 48, "Franchise": "Chennai Super Kings / Lancashire"},
    {"name": "Graham Gooch", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 73, "Franchise": "Essex"},
    {"name": "David Gower", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 69, "Franchise": "Leicestershire / Hampshire"},
    {"name": "Bob Willis", "Country": "England", "status": "Deceased", "Role": "BOWL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Warwickshire"},
    {"name": "Fred Trueman", "Country": "England", "status": "Deceased", "Role": "BOWL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Yorkshire"},
    {"name": "Sydney Barnes", "Country": "England", "status": "Deceased", "Role": "BOWL", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Lancashire / Staffordshire"},
    {"name": "Eoin Morgan", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 39, "Franchise": "Kolkata Knight Riders / Middlesex"},
    {"name": "Jonny Bairstow", "Country": "England", "status": "Active", "Role": "WK", "Batting Hand": "Right", "Age": 36, "Franchise": "Punjab Kings / Sunrisers Hyderabad"},
    {"name": "Jofra Archer", "Country": "England", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 31, "Franchise": "Mumbai Indians / Rajasthan Royals"},
    {"name": "Harry Brook", "Country": "England", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 27, "Franchise": "Sunrisers Hyderabad / Yorkshire"},
    {"name": "Graeme Swann", "Country": "England", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 47, "Franchise": "Nottinghamshire"},
    {"name": "Paul Collingwood", "Country": "England", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 50, "Franchise": "Delhi Capitals / Durham"},
    {"name": "Alec Stewart", "Country": "England", "status": "Retired", "Role": "WK", "Batting Hand": "Right", "Age": 63, "Franchise": "Surrey"},
    {"name": "Marcus Trescothick", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 50, "Franchise": "Somerset / Royal Challengers Bengaluru"},
    {"name": "Michael Vaughan", "Country": "England", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 51, "Franchise": "Yorkshire"},
    {"name": "Adil Rashid", "Country": "England", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 38, "Franchise": "Sunrisers Hyderabad / Yorkshire"},
    {"name": "Liam Livingstone", "Country": "England", "status": "Active", "Role": "ALL", "Batting Hand": "Right", "Age": 33, "Franchise": "Punjab Kings / Lancashire"},
    {"name": "Moeen Ali", "Country": "England", "status": "Active", "Role": "ALL", "Batting Hand": "Left", "Age": 39, "Franchise": "Chennai Super Kings / Royal Challengers Bengaluru"},
    {"name": "Mark Wood", "Country": "England", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 36, "Franchise": "Lucknow Super Giants / Durham"},

    # New Zealand

{"name": "Sir Richard Hadlee", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 75, "Franchise": "Nottinghamshire / Canterbury"},
    {"name": "Kane Williamson", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 35, "Franchise": "Sunrisers Hyderabad / Gujarat Titans"},
    {"name": "Brendon McCullum", "Country": "New Zealand", "status": "Retired", "Role": "WK", "Batting Hand": "Right", "Age": 44, "Franchise": "Kolkata Knight Riders / Otago"},
    {"name": "Stephen Fleming", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 53, "Franchise": "Chennai Super Kings / Wellington"},
    {"name": "Ross Taylor", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 42, "Franchise": "Royal Challengers Bengaluru / Central Districts"},
    {"name": "Daniel Vettori", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 47, "Franchise": "Royal Challengers Bengaluru / Northern Districts"},
    {"name": "Trent Boult", "Country": "New Zealand", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 37, "Franchise": "Rajasthan Royals / Mumbai Indians"},
    {"name": "Tim Southee", "Country": "New Zealand", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 37, "Franchise": "Kolkata Knight Riders / Northern Districts"},
    {"name": "Martin Crowe", "Country": "New Zealand", "status": "Deceased", "Role": "BAT", "Batting Hand": "Right", "Age": "N/A", "Franchise": "Somerset / Auckland"},
    {"name": "Shane Bond", "Country": "New Zealand", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 51, "Franchise": "Kolkata Knight Riders / Canterbury"},
    {"name": "Chris Cairns", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 56, "Franchise": "Nottinghamshire / Canterbury"},
    {"name": "Nathan Astle", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 54, "Franchise": "Mumbai Indians / Canterbury"},
    {"name": "Scott Styris", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 51, "Franchise": "Chennai Super Kings / Deccan Chargers"},
    {"name": "Devon Conway", "Country": "New Zealand", "status": "Active", "Role": "WK", "Batting Hand": "Left", "Age": 35, "Franchise": "Chennai Super Kings / Wellington"},
    {"name": "Daryl Mitchell", "Country": "New Zealand", "status": "Active", "Role": "ALL", "Batting Hand": "Right", "Age": 35, "Franchise": "Chennai Super Kings / Canterbury"},
    {"name": "Rachin Ravindra", "Country": "New Zealand", "status": "Active", "Role": "ALL", "Batting Hand": "Left", "Age": 26, "Franchise": "Chennai Super Kings / Wellington"},
    {"name": "Mitchell Santner", "Country": "New Zealand", "status": "Active", "Role": "ALL", "Batting Hand": "Left", "Age": 34, "Franchise": "Chennai Super Kings / Northern Districts"},
    {"name": "Jacob Oram", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 48, "Franchise": "Chennai Super Kings / Mumbai Indians"},
    {"name": "Tom Latham", "Country": "New Zealand", "status": "Active", "Role": "WK", "Batting Hand": "Left", "Age": 34, "Franchise": "Canterbury"},
    {"name": "John Wright", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 72, "Franchise": "Derbyshire / Northern Districts"},
    {"name": "Glenn Phillips", "Country": "New Zealand", "status": "Active", "Role": "ALL", "Batting Hand": "Right", "Age": 29, "Franchise": "Sunrisers Hyderabad / Otago"},
    {"name": "Kyle Jamieson", "Country": "New Zealand", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 31, "Franchise": "Royal Challengers Bengaluru / Chennai Super Kings"},
    {"name": "Matt Henry", "Country": "New Zealand", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 34, "Franchise": "Punjab Kings / Lucknow Super Giants"},
    {"name": "Lockie Ferguson", "Country": "New Zealand", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 35, "Franchise": "Royal Challengers Bengaluru / KKR"},
    {"name": "Colin de Grandhomme", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 40, "Franchise": "Kolkata Knight Riders / RCB"},
    {"name": "Corey Anderson", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 35, "Franchise": "Mumbai Indians / Royal Challengers Bengaluru"},
    {"name": "Craig McMillan", "Country": "New Zealand", "status": "Retired", "Role": "ALL", "Batting Hand": "Right", "Age": 49, "Franchise": "Royal Challengers Bengaluru / Canterbury"},
    {"name": "Bert Sutcliffe", "Country": "New Zealand", "status": "Deceased", "Role": "BAT", "Batting Hand": "Left", "Age": "N/A", "Franchise": "Otago / Auckland"},
    {"name": "Geoff Howarth", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 75, "Franchise": "Surrey / Northern Districts"},
    {"name": "Martin Guptill", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 39, "Franchise": "Sunrisers Hyderabad / Mumbai Indians"},

    # South Africa
    {"name": "Jacques Kallis", "Country": "South Africa", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 50, "Franchise": "Kolkata Knight Riders / Royal Challengers Bangalore"},
    {"name": "AB de Villiers", "Country": "South Africa", "status": "Retired", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 42, "Franchise": "Royal Challengers Bangalore / Delhi Daredevils"},
    {"name": "Dale Steyn", "Country": "South Africa", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 43, "Franchise": "Sunrisers Hyderabad / Royal Challengers Bangalore"},
    {"name": "Shaun Pollock", "Country": "South Africa", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 53, "Franchise": "Mumbai Indians"},
    {"name": "Allan Donald", "Country": "South Africa", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 59, "Franchise": "Warwickshire / Free State"},
    {"name": "Graeme Smith", "Country": "South Africa", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 45, "Franchise": "Rajasthan Royals / Pune Warriors"},
    {"name": "Hashim Amla", "Country": "South Africa", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 43, "Franchise": "Kings XI Punjab / Cape Cobras"},
    {"name": "Kagiso Rabada", "Country": "South Africa", "status": "Active", "Role": "BOWL", "Batting Hand": "Left", "Age": 31, "Franchise": "Delhi Capitals / Punjab Kings"},
    {"name": "Quinton de Kock", "Country": "South Africa", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Left", "Age": 33, "Franchise": "Mumbai Indians / Lucknow Super Giants"},
    {"name": "Faf du Plessis", "Country": "South Africa", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 42, "Franchise": "Chennai Super Kings / Royal Challengers Bengaluru"},
    {"name": "Makhaya Ntini", "Country": "South Africa", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 49, "Franchise": "Chennai Super Kings"},
    {"name": "Mark Boucher", "Country": "South Africa", "status": "Retired", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 49, "Franchise": "Royal Challengers Bangalore / Kolkata Knight Riders"},
    {"name": "Gary Kirsten", "Country": "South Africa", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 58, "Franchise": "Western Province"},
    {"name": "Herschelle Gibbs", "Country": "South Africa", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 52, "Franchise": "Deccan Chargers / Mumbai Indians"},
    {"name": "Lance Klusener", "Country": "South Africa", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 54, "Franchise": "Middlesex / Dolphins"},
    {"name": "Jonty Rhodes", "Country": "South Africa", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 57, "Franchise": "Gloucestershire / Natal"},
    {"name": "Morne Morkel", "Country": "South Africa", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 41, "Franchise": "Delhi Daredevils / Kolkata Knight Riders"},
    {"name": "Vernon Philander", "Country": "South Africa", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 41, "Franchise": "Cape Cobras / Somerset"},
    {"name": "David Miller", "Country": "South Africa", "status": "Active", "Role": "BAT", "Batting Hand": "Left", "Age": 37, "Franchise": "Gujarat Titans / Punjab Kings"},
    {"name": "Imran Tahir", "Country": "South Africa", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 47, "Franchise": "Chennai Super Kings / Rising Pune Supergiant"},

    # West Indies
    {"name": "Sir Garfield Sobers", "Country": "West Indies", "status": "Deceased", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 89, "Franchise": "Barbados / South Australia"},
    {"name": "Sir Vivian Richards", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 74, "Franchise": "Somerset / Leeward Islands"},
    {"name": "Brian Lara", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 57, "Franchise": "Warwickshire / Trinidad and Tobago"},
    {"name": "Sir Curtly Ambrose", "Country": "West Indies", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 62, "Franchise": "Northamptonshire / Leeward Islands"},
    {"name": "Malcolm Marshall", "Country": "West Indies", "status": "Deceased", "Role": "BOWL", "Batting Hand": "Right", "Age": 41, "Franchise": "Hampshire / Barbados"},
    {"name": "Courtney Walsh", "Country": "West Indies", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 63, "Franchise": "Gloucestershire / Jamaica"},
    {"name": "Michael Holding", "Country": "West Indies", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 72, "Franchise": "Lancashire / Jamaica"},
    {"name": "Clive Lloyd", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 81, "Franchise": "Lancashire / Guyana"},
    {"name": "Chris Gayle", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 46, "Franchise": "Royal Challengers Bangalore / Punjab Kings"},
    {"name": "Shivnarine Chanderpaul", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 51, "Franchise": "Royal Challengers Bangalore / Guyana"},
    {"name": "Joel Garner", "Country": "West Indies", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 73, "Franchise": "Somerset / Barbados"},
    {"name": "Gordon Greenidge", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 75, "Franchise": "Hampshire / Barbados"},
    {"name": "Desmond Haynes", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 70, "Franchise": "Middlesex / Barbados"},
    {"name": "Kieron Pollard", "Country": "West Indies", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 39, "Franchise": "Mumbai Indians / MI Emirates"},
    {"name": "Dwayne Bravo", "Country": "West Indies", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 42, "Franchise": "Chennai Super Kings / Kolkata Knight Riders"},
    {"name": "Andre Russell", "Country": "West Indies", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 38, "Franchise": "Kolkata Knight Riders / Trinbago Knight Riders"},
    {"name": "Sunil Narine", "Country": "West Indies", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 38, "Franchise": "Kolkata Knight Riders / Trinbago Knight Riders"},
    {"name": "Lance Gibbs", "Country": "West Indies", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 91, "Franchise": "Warwickshire / Guyana"},
    {"name": "Rohan Kanhai", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 90, "Franchise": "Warwickshire / Guyana"},
    {"name": "Alvin Kallicharran", "Country": "West Indies", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 77, "Franchise": "Warwickshire / Guyana"},

    # Afghanistan
    {"name": "Rashid Khan", "Country": "Afghanistan", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 27, "Franchise": "Gujarat Titans / MI Cape Town"},
    {"name": "Mohammad Nabi", "Country": "Afghanistan", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 41, "Franchise": "Sunrisers Hyderabad / Mumbai Indians"},
    {"name": "Mujeeb Ur Rahman", "Country": "Afghanistan", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 25, "Franchise": "Kings XI Punjab / Kolkata Knight Riders"},
    {"name": "Rahmanullah Gurbaz", "Country": "Afghanistan", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 24, "Franchise": "Kolkata Knight Riders / Gujarat Titans"},
    {"name": "Ibrahim Zadran", "Country": "Afghanistan", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 24, "Franchise": "Kabul Eagles / Band-e-Amir Dragons"},
    {"name": "Fazalhaq Farooqi", "Country": "Afghanistan", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 25, "Franchise": "Sunrisers Hyderabad / Dhaka Dominators"},
    {"name": "Mohammad Shahzad", "Country": "Afghanistan", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 38, "Franchise": "Chittagong Vikings / Speenghar Tigers"},
    {"name": "Asghar Afghan", "Country": "Afghanistan", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 38, "Franchise": "Kabul Zwanan / Speenghar Tigers"},
    {"name": "Gulbadin Naib", "Country": "Afghanistan", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 35, "Franchise": "Delhi Capitals / Balkh Legends"},
    {"name": "Naveen-ul-Haq", "Country": "Afghanistan", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 26, "Franchise": "Lucknow Super Giants / Guyana Amazon Warriors"},
    {"name": "Rahmat Shah", "Country": "Afghanistan", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 33, "Franchise": "Mis Ainak Knights / Band-e-Amir Dragons"},
    {"name": "Najibullah Zadran", "Country": "Afghanistan", "status": "Active", "Role": "BAT", "Batting Hand": "Left", "Age": 33, "Franchise": "Karachi Kings / St Kitts & Nevis Patriots"},
    {"name": "Hamid Hassan", "Country": "Afghanistan", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 39, "Franchise": "Band-e-Amir Dragons / Speenghar Tigers"},
    {"name": "Dawlat Zadran", "Country": "Afghanistan", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 38, "Franchise": "Kandahar Knights / Band-e-Amir Dragons"},
    {"name": "Nawroz Mangal", "Country": "Afghanistan", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 42, "Franchise": "Mis Ainak Knights / Kabul Express"},

    # Bangladesh
    {"name": "Shakib Al Hasan", "Country": "Bangladesh", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 39, "Franchise": "Kolkata Knight Riders / Sunrisers Hyderabad"},
    {"name": "Tamim Iqbal", "Country": "Bangladesh", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 37, "Franchise": "Fortune Barishal / Peshawar Zalmi"},
    {"name": "Mushfiqur Rahim", "Country": "Bangladesh", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 39, "Franchise": "Sylhet Strikers / Fortune Barishal"},
    {"name": "Mahmudullah", "Country": "Bangladesh", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 40, "Franchise": "Fortune Barishal / Quetta Gladiators"},
    {"name": "Mashrafe Mortaza", "Country": "Bangladesh", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 42, "Franchise": "Kolkata Knight Riders / Dhaka Dynamites"},
    {"name": "Mustafizur Rahman", "Country": "Bangladesh", "status": "Active", "Role": "BOWL", "Batting Hand": "Left", "Age": 30, "Franchise": "Chennai Super Kings / Sunrisers Hyderabad"},
    {"name": "Litton Das", "Country": "Bangladesh", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 31, "Franchise": "Kolkata Knight Riders / Comilla Victorians"},
    {"name": "Taskin Ahmed", "Country": "Bangladesh", "status": "Active", "Role": "BOWL", "Batting Hand": "Left", "Age": 31, "Franchise": "Durdanto Dhaka / Bulawayo Brave Jaguars"},
    {"name": "Mehidy Hasan Miraz", "Country": "Bangladesh", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 28, "Franchise": "Fortune Barishal / Trinbago Knight Riders"},
    {"name": "Mohammad Ashraful", "Country": "Bangladesh", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 42, "Franchise": "Mumbai Indians / Dhaka Gladiators"},
    {"name": "Abdur Razzak", "Country": "Bangladesh", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 44, "Franchise": "Royal Challengers Bangalore / Khulna Royal Bengals"},
    {"name": "Rubel Hossain", "Country": "Bangladesh", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 36, "Franchise": "Sylhet Sunrisers / Chattogram Challengers"},
    {"name": "Imrul Kayes", "Country": "Bangladesh", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 39, "Franchise": "Comilla Victorians / Rangpur Riders"},
    {"name": "Habibul Bashar", "Country": "Bangladesh", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 53, "Franchise": "Khulna Division / Dhaka Warriors"},
    {"name": "Shahriar Nafees", "Country": "Bangladesh", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 41, "Franchise": "Barisal Burners / Khulna Titans"},

    # Sri Lanka
    {"name": "Muttiah Muralitharan", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 54, "Franchise": "Chennai Super Kings / Royal Challengers Bangalore"},
    {"name": "Kumar Sangakkara", "Country": "Sri Lanka", "status": "Retired", "Role": "WK-BAT", "Batting Hand": "Left", "Age": 48, "Franchise": "Kings XI Punjab / Deccan Chargers"},
    {"name": "Mahela Jayawardene", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 49, "Franchise": "Kings XI Punjab / Delhi Daredevils"},
    {"name": "Sanath Jayasuriya", "Country": "Sri Lanka", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 57, "Franchise": "Mumbai Indians / Khulna Royal Bengals"},
    {"name": "Lasith Malinga", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 42, "Franchise": "Mumbai Indians / Rangpur Riders"},
    {"name": "Aravinda de Silva", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 60, "Franchise": "Kent / Auckland"},
    {"name": "Tillakaratne Dilshan", "Country": "Sri Lanka", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 49, "Franchise": "Royal Challengers Bangalore / Delhi Daredevils"},
    {"name": "Chaminda Vaas", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 52, "Franchise": "Deccan Chargers / Northamptonshire"},
    {"name": "Angelo Mathews", "Country": "Sri Lanka", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 39, "Franchise": "Delhi Capitals / Kolkata Knight Riders"},
    {"name": "Wanindu Hasaranga", "Country": "Sri Lanka", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 29, "Franchise": "Royal Challengers Bangalore / Sunrisers Hyderabad"},
    {"name": "Marvan Atapattu", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 55, "Franchise": "Delhi Daredevils / Sinhalese Sports Club"},
    {"name": "Arjuna Ranatunga", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 62, "Franchise": "Sinhalese Sports Club"},
    {"name": "Rangana Herath", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Left", "Age": 48, "Franchise": "Surrey / Hampshire"},
    {"name": "Pathum Nissanka", "Country": "Sri Lanka", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 28, "Franchise": "Kandy Falcons / Colombo Strikers"},
    {"name": "Kusal Mendis", "Country": "Sri Lanka", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 31, "Franchise": "Pretoria Capitals / Galle Titans"},
    {"name": "Kusal Perera", "Country": "Sri Lanka", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Left", "Age": 35, "Franchise": "Rajasthan Royals / Dambulla Aura"},
    {"name": "Charith Asalanka", "Country": "Sri Lanka", "status": "Active", "Role": "BAT", "Batting Hand": "Left", "Age": 29, "Franchise": "Jaffna Kings / Colombo Strikers"},
    {"name": "Dinesh Chandimal", "Country": "Sri Lanka", "status": "Active", "Role": "WK-BAT", "Batting Hand": "Right", "Age": 36, "Franchise": "Rajasthan Royals / Colombo Strikers"},
    {"name": "Thilan Samaraweera", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 49, "Franchise": "Worcestershire / Sinhalese Sports Club"},
    {"name": "Upul Tharanga", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Left", "Age": 41, "Franchise": "Nondescripts Cricket Club / Dhaka Dynamites"},
    {"name": "Thisara Perera", "Country": "Sri Lanka", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Left", "Age": 37, "Franchise": "Chennai Super Kings / Mumbai Indians"},
    {"name": "Nuwan Kulasekara", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 44, "Franchise": "Chennai Super Kings / Colt Cricket Club"},
    {"name": "Dasun Shanaka", "Country": "Sri Lanka", "status": "Active", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 34, "Franchise": "Gujarat Titans / Seattle Orcas"},
    {"name": "Dushmantha Chameera", "Country": "Sri Lanka", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 34, "Franchise": "Lucknow Super Giants / Kolkata Knight Riders"},
    {"name": "Maheesh Theekshana", "Country": "Sri Lanka", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 25, "Franchise": "Chennai Super Kings / Texas Super Kings"},
    {"name": "Matheesha Pathirana", "Country": "Sri Lanka", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 23, "Franchise": "Chennai Super Kings / Colombo Strikers"},
    {"name": "Farveez Maharoof", "Country": "Sri Lanka", "status": "Retired", "Role": "ALL-ROUNDER", "Batting Hand": "Right", "Age": 41, "Franchise": "Delhi Daredevils / Lancashire"},
    {"name": "Ajantha Mendis", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 41, "Franchise": "Kolkata Knight Riders / Pune Warriors"},
    {"name": "Roy Dias", "Country": "Sri Lanka", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 73, "Franchise": "Colombo Cricket Club"},
    {"name": "Rumesh Ratnayake", "Country": "Sri Lanka", "status": "Retired", "Role": "BOWL", "Batting Hand": "Right", "Age": 62, "Franchise": "Nondescripts Cricket Club"}
]

PLAYERS = [
    # Premier League
    {"name": "David Raya", "league": "Premier League", "team": "Arsenal", "nation": "Spain", "position": "GK",
     "age": 28, "number": 22},
    {"name": "William Saliba", "league": "Premier League", "team": "Arsenal", "nation": "France", "position": "DF",
     "age": 23, "number": 2},
    {"name": "Bukayo Saka", "league": "Premier League", "team": "Arsenal", "nation": "England", "position": "FW",
     "age": 22, "number": 7},
    {"name": "Cole Palmer", "league": "Premier League", "team": "Chelsea", "nation": "England", "position": "MF",
     "age": 22, "number": 20},
    {"name": "Erling Haaland", "league": "Premier League", "team": "Manchester City", "nation": "Norway",
     "position": "FW", "age": 24, "number": 9},
    {"name": "Aaron Ramsdale", "league": "Premier League", "team": "Southampton", "nation": "England", "position": "GK",
     "age": 26, "number": 30},
    {"name": "Kevin De Bruyne", "league": "Premier League", "team": "Manchester City", "nation": "Belgium",
     "position": "MF", "age": 33, "number": 17},
    {"name": "Rodri", "league": "Premier League", "team": "Manchester City", "nation": "Spain", "position": "MF",
     "age": 28, "number": 16},
    {"name": "Phil Foden", "league": "Premier League", "team": "Manchester City", "nation": "England", "position": "MF",
     "age": 24, "number": 47},
    {"name": "Rúben Dias", "league": "Premier League", "team": "Manchester City", "nation": "Portugal",
     "position": "DF", "age": 27, "number": 3},
    {"name": "Bernardo Silva", "league": "Premier League", "team": "Manchester City", "nation": "Portugal",
     "position": "MF", "age": 29, "number": 20},
    {"name": "Ederson", "league": "Premier League", "team": "Manchester City", "nation": "Brazil", "position": "GK",
     "age": 30, "number": 31},
    {"name": "Josko Gvardiol", "league": "Premier League", "team": "Manchester City", "nation": "Croatia",
     "position": "DF", "age": 22, "number": 24},
    {"name": "Martin Ødegaard", "league": "Premier League", "team": "Arsenal", "nation": "Norway", "position": "MF",
     "age": 25, "number": 8},
    {"name": "Declan Rice", "league": "Premier League", "team": "Arsenal", "nation": "England", "position": "MF",
     "age": 25, "number": 41},
    {"name": "Gabriel Magalhães", "league": "Premier League", "team": "Arsenal", "nation": "Brazil", "position": "DF",
     "age": 26, "number": 6},
    {"name": "Kai Havertz", "league": "Premier League", "team": "Arsenal", "nation": "Germany", "position": "FW",
     "age": 25, "number": 29},
    {"name": "Gabriel Martinelli", "league": "Premier League", "team": "Arsenal", "nation": "Brazil", "position": "FW",
     "age": 23, "number": 11},
    {"name": "Leandro Trossard", "league": "Premier League", "team": "Arsenal", "nation": "Belgium", "position": "FW",
     "age": 29, "number": 19},
    {"name": "Jurriën Timber", "league": "Premier League", "team": "Arsenal", "nation": "Netherlands", "position": "DF",
     "age": 23, "number": 12},
    {"name": "Riccardo Calafiori", "league": "Premier League", "team": "Arsenal", "nation": "Italy", "position": "DF",
     "age": 22, "number": 33},
    {"name": "Mohamed Salah", "league": "Premier League", "team": "Liverpool", "nation": "Egypt", "position": "FW",
     "age": 32, "number": 11},
    {"name": "Virgil van Dijk", "league": "Premier League", "team": "Liverpool", "nation": "Netherlands",
     "position": "DF", "age": 33, "number": 4},
    {"name": "Trent Alexander-Arnold", "league": "Premier League", "team": "Liverpool", "nation": "England",
     "position": "DF", "age": 25, "number": 66},
    {"name": "Alisson Becker", "league": "Premier League", "team": "Liverpool", "nation": "Brazil", "position": "GK",
     "age": 31, "number": 1},
    {"name": "Alexis Mac Allister", "league": "Premier League", "team": "Liverpool", "nation": "Argentina",
     "position": "MF", "age": 25, "number": 10},
    {"name": "Dominik Szoboszlai", "league": "Premier League", "team": "Liverpool", "nation": "Hungary",
     "position": "MF", "age": 23, "number": 8},
    {"name": "Cody Gakpo", "league": "Premier League", "team": "Liverpool", "nation": "Netherlands", "position": "FW",
     "age": 25, "number": 18},
    {"name": "Luis Díaz", "league": "Premier League", "team": "Liverpool", "nation": "Colombia", "position": "FW",
     "age": 27, "number": 7},
    {"name": "Darwin Núñez", "league": "Premier League", "team": "Liverpool", "nation": "Uruguay", "position": "FW",
     "age": 25, "number": 9},
    {"name": "Ibrahima Konaté", "league": "Premier League", "team": "Liverpool", "nation": "France", "position": "DF",
     "age": 25, "number": 5},
    {"name": "Andy Robertson", "league": "Premier League", "team": "Liverpool", "nation": "Scotland", "position": "DF",
     "age": 30, "number": 26},
    {"name": "Enzo Fernández", "league": "Premier League", "team": "Chelsea", "nation": "Argentina", "position": "MF",
     "age": 23, "number": 8},
    {"name": "Moises Caicedo", "league": "Premier League", "team": "Chelsea", "nation": "Ecuador", "position": "MF",
     "age": 22, "number": 25},
    {"name": "Nicolas Jackson", "league": "Premier League", "team": "Chelsea", "nation": "Senegal", "position": "FW",
     "age": 23, "number": 15},
    {"name": "Pedro Neto", "league": "Premier League", "team": "Chelsea", "nation": "Portugal", "position": "FW",
     "age": 24, "number": 7},
    {"name": "Marc Cucurella", "league": "Premier League", "team": "Chelsea", "nation": "Spain", "position": "DF",
     "age": 26, "number": 3},
    {"name": "Levi Colwill", "league": "Premier League", "team": "Chelsea", "nation": "England", "position": "DF",
     "age": 21, "number": 6},
    {"name": "Bruno Fernandes", "league": "Premier League", "team": "Manchester United", "nation": "Portugal",
     "position": "MF", "age": 29, "number": 8},
    {"name": "Kobbie Mainoo", "league": "Premier League", "team": "Manchester United", "nation": "England",
     "position": "MF", "age": 19, "number": 37},
    {"name": "Alejandro Garnacho", "league": "Premier League", "team": "Manchester United", "nation": "Argentina",
     "position": "FW", "age": 20, "number": 17},
    {"name": "Lisandro Martínez", "league": "Premier League", "team": "Manchester United", "nation": "Argentina",
     "position": "DF", "age": 26, "number": 6},
    {"name": "Matthijs de Ligt", "league": "Premier League", "team": "Manchester United", "nation": "Netherlands",
     "position": "DF", "age": 24, "number": 4},
    {"name": "Diogo Dalot", "league": "Premier League", "team": "Manchester United", "nation": "Portugal",
     "position": "DF", "age": 25, "number": 20},
    {"name": "Manuel Ugarte", "league": "Premier League", "team": "Manchester United", "nation": "Uruguay",
     "position": "MF", "age": 23, "number": 25},

    # La Liga
    {"name": "Unai Simón", "league": "La Liga", "team": "Athletic Club", "nation": "Spain", "position": "GK", "age": 27,
     "number": 1},
    {"name": "Jude Bellingham", "league": "La Liga", "team": "Real Madrid", "nation": "England", "position": "MF",
     "age": 21, "number": 5},
    {"name": "Lamine Yamal", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "FW", "age": 17,
     "number": 19},
    {"name": "Kylian Mbappé", "league": "La Liga", "team": "Real Madrid", "nation": "France", "position": "FW",
     "age": 25, "number": 9},
    {"name": "Vinícius Júnior", "league": "La Liga", "team": "Real Madrid", "nation": "Brazil", "position": "FW",
     "age": 24, "number": 7},
    {"name": "Rodrygo", "league": "La Liga", "team": "Real Madrid", "nation": "Brazil", "position": "FW", "age": 23,
     "number": 11},
    {"name": "Federico Valverde", "league": "La Liga", "team": "Real Madrid", "nation": "Uruguay", "position": "MF",
     "age": 26, "number": 8},
    {"name": "Eduardo Camavinga", "league": "La Liga", "team": "Real Madrid", "nation": "France", "position": "MF",
     "age": 21, "number": 6},
    {"name": "Aurelien Tchouaméni", "league": "La Liga", "team": "Real Madrid", "nation": "France", "position": "MF",
     "age": 24, "number": 14},
    {"name": "Luka Modrić", "league": "La Liga", "team": "Real Madrid", "nation": "Croatia", "position": "MF",
     "age": 38, "number": 10},
    {"name": "Antonio Rüdiger", "league": "La Liga", "team": "Real Madrid", "nation": "Germany", "position": "DF",
     "age": 31, "number": 22},
    {"name": "Éder Militão", "league": "La Liga", "team": "Real Madrid", "nation": "Brazil", "position": "DF",
     "age": 26, "number": 3},
    {"name": "Thibaut Courtois", "league": "La Liga", "team": "Real Madrid", "nation": "Belgium", "position": "GK",
     "age": 32, "number": 1},
    {"name": "Robert Lewandowski", "league": "La Liga", "team": "Barcelona", "nation": "Poland", "position": "FW",
     "age": 35, "number": 9},
    {"name": "Pedri", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "MF", "age": 21,
     "number": 8},
    {"name": "Gavi", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "MF", "age": 19,
     "number": 6},
    {"name": "Raphinha", "league": "La Liga", "team": "Barcelona", "nation": "Brazil", "position": "FW", "age": 27,
     "number": 11},
    {"name": "Frenkie de Jong", "league": "La Liga", "team": "Barcelona", "nation": "Netherlands", "position": "MF",
     "age": 27, "number": 21},
    {"name": "Jules Koundé", "league": "La Liga", "team": "Barcelona", "nation": "France", "position": "DF", "age": 25,
     "number": 23},
    {"name": "Ronald Araújo", "league": "La Liga", "team": "Barcelona", "nation": "Uruguay", "position": "DF",
     "age": 25, "number": 4},
    {"name": "Marc-André ter Stegen", "league": "La Liga", "team": "Barcelona", "nation": "Germany", "position": "GK",
     "age": 32, "number": 1},
    {"name": "Dani Olmo", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "MF", "age": 26,
     "number": 20},
    {"name": "Pau Cubarsí", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "DF", "age": 17,
     "number": 2},
    {"name": "Antoine Griezmann", "league": "La Liga", "team": "Atlético Madrid", "nation": "France", "position": "FW",
     "age": 33, "number": 7},
    {"name": "Julián Alvarez", "league": "La Liga", "team": "Atlético Madrid", "nation": "Argentina", "position": "FW",
     "age": 24, "number": 19},
    {"name": "Rodrigo De Paul", "league": "La Liga", "team": "Atlético Madrid", "nation": "Argentina", "position": "MF",
     "age": 30, "number": 5},
    {"name": "Jan Oblak", "league": "La Liga", "team": "Atlético Madrid", "nation": "Slovenia", "position": "GK",
     "age": 31, "number": 1},
    {"name": "Conor Gallagher", "league": "La Liga", "team": "Atlético Madrid", "nation": "England", "position": "MF",
     "age": 24, "number": 4},
    {"name": "Robin Le Normand", "league": "La Liga", "team": "Atlético Madrid", "nation": "Spain", "position": "DF",
     "age": 27, "number": 24},
    {"name": "Nico Williams", "league": "La Liga", "team": "Athletic Club", "nation": "Spain", "position": "FW",
     "age": 22, "number": 10},

    # Serie A
    {"name": "Lautaro Martínez", "league": "Serie A", "team": "Inter Milan", "nation": "Argentina", "position": "FW",
     "age": 26, "number": 10},
    {"name": "Rafael Leão", "league": "Serie A", "team": "AC Milan", "nation": "Portugal", "position": "FW", "age": 25,
     "number": 10},
    {"name": "Nicolo Barella", "league": "Serie A", "team": "Inter Milan", "nation": "Italy", "position": "MF",
     "age": 27, "number": 23},
    {"name": "Alessandro Bastoni", "league": "Serie A", "team": "Inter Milan", "nation": "Italy", "position": "DF",
     "age": 25, "number": 95},
    {"name": "Hakan Çalhanoğlu", "league": "Serie A", "team": "Inter Milan", "nation": "Türkiye", "position": "MF",
     "age": 30, "number": 20},
    {"name": "Marcus Thuram", "league": "Serie A", "team": "Inter Milan", "nation": "France", "position": "FW",
     "age": 26, "number": 9},
    {"name": "Yann Sommer", "league": "Serie A", "team": "Inter Milan", "nation": "Switzerland", "position": "GK",
     "age": 35, "number": 1},
    {"name": "Federico Dimarco", "league": "Serie A", "team": "Inter Milan", "nation": "Italy", "position": "DF",
     "age": 26, "number": 32},
    {"name": "Denzel Dumfries", "league": "Serie A", "team": "Inter Milan", "nation": "Netherlands", "position": "DF",
     "age": 28, "number": 2},
    {"name": "Theo Hernández", "league": "Serie A", "team": "AC Milan", "nation": "France", "position": "DF", "age": 26,
     "number": 19},
    {"name": "Mike Maignan", "league": "Serie A", "team": "AC Milan", "nation": "France", "position": "GK", "age": 29,
     "number": 16},
    {"name": "Christian Pulisic", "league": "Serie A", "team": "AC Milan", "nation": "USA", "position": "FW", "age": 25,
     "number": 11},
    {"name": "Tijjani Reijnders", "league": "Serie A", "team": "AC Milan", "nation": "Netherlands", "position": "MF",
     "age": 26, "number": 14},
    {"name": "Alvaro Morata", "league": "Serie A", "team": "AC Milan", "nation": "Spain", "position": "FW", "age": 31,
     "number": 7},
    {"name": "Dušan Vlahović", "league": "Serie A", "team": "Juventus", "nation": "Serbia", "position": "FW", "age": 24,
     "number": 9},
    {"name": "Gleison Bremer", "league": "Serie A", "team": "Juventus", "nation": "Brazil", "position": "DF", "age": 27,
     "number": 3},
    {"name": "Teun Koopmeiners", "league": "Serie A", "team": "Juventus", "nation": "Netherlands", "position": "MF",
     "age": 26, "number": 8},
    {"name": "Kenan Yildiz", "league": "Serie A", "team": "Juventus", "nation": "Türkiye", "position": "FW", "age": 19,
     "number": 10},
    {"name": "Douglas Luiz", "league": "Serie A", "team": "Juventus", "nation": "Brazil", "position": "MF", "age": 26,
     "number": 26},
    {"name": "Khvicha Kvaratskhelia", "league": "Serie A", "team": "Napoli", "nation": "Georgia", "position": "FW",
     "age": 23, "number": 77},
    {"name": "Romelu Lukaku", "league": "Serie A", "team": "Napoli", "nation": "Belgium", "position": "FW", "age": 31,
     "number": 11},
    {"name": "Alessandro Buongiorno", "league": "Serie A", "team": "Napoli", "nation": "Italy", "position": "DF",
     "age": 25, "number": 4},
    {"name": "Scott McTominay", "league": "Serie A", "team": "Napoli", "nation": "Scotland", "position": "MF",
     "age": 27, "number": 8},
    {"name": "Paulo Dybala", "league": "Serie A", "team": "Roma", "nation": "Argentina", "position": "FW", "age": 30,
     "number": 21},
    {"name": "Artem Dovbyk", "league": "Serie A", "team": "Roma", "nation": "Ukraine", "position": "FW", "age": 27,
     "number": 11},
    {"name": "Lorenzo Pellegrini", "league": "Serie A", "team": "Roma", "nation": "Italy", "position": "MF", "age": 28,
     "number": 7},
    {"name": "Maneul Locatelli", "league": "Serie A", "team": "Juventus", "nation": "Italy", "position": "MF",
     "age": 26, "number": 5},
    {"name": "Benjamin Pavard", "league": "Serie A", "team": "Inter Milan", "nation": "France", "position": "DF",
     "age": 28, "number": 28},
    {"name": "Piotr Zieliński", "league": "Serie A", "team": "Inter Milan", "nation": "Poland", "position": "MF",
     "age": 30, "number": 7},

    # Bundesliga
    {"name": "Manuel Neuer", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "GK",
     "age": 38, "number": 1},
    {"name": "Dayot Upamecano", "league": "Bundesliga", "team": "Bayern Munich", "nation": "France", "position": "DF",
     "age": 25, "number": 2},
    {"name": "Min-jae Kim", "league": "Bundesliga", "team": "Bayern Munich", "nation": "South Korea", "position": "DF",
     "age": 27, "number": 3},
    {"name": "Alphonso Davies", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Canada", "position": "DF",
     "age": 23, "number": 19},
    {"name": "Josip Stanišić", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Croatia", "position": "DF",
     "age": 24, "number": 44},
    {"name": "Joshua Kimmich", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "MF",
     "age": 29, "number": 6},
    {"name": "Leon Goretzka", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "MF",
     "age": 29, "number": 8},
    {"name": "Konrad Laimer", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Austria", "position": "MF",
     "age": 27, "number": 27},
    {"name": "Aleksandar Pavlović", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany",
     "position": "MF", "age": 20, "number": 45},
    {"name": "Jamal Musiala", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "MF",
     "age": 21, "number": 42},
    {"name": "Michael Olise", "league": "Bundesliga", "team": "Bayern Munich", "nation": "France", "position": "FW",
     "age": 22, "number": 17},
    {"name": "Leroy Sané", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "FW",
     "age": 28, "number": 10},
    {"name": "Serge Gnabry", "league": "Bundesliga", "team": "Bayern Munich", "nation": "Germany", "position": "FW",
     "age": 29, "number": 7},
    {"name": "Harry Kane", "league": "Bundesliga", "team": "Bayern Munich", "nation": "England", "position": "FW",
     "age": 30, "number": 9},
    {"name": "Granit Xhaka", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Switzerland",
     "position": "MF", "age": 31, "number": 34},
    {"name": "Florian Wirtz", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Germany", "position": "MF",
     "age": 21, "number": 10},
    {"name": "Jeremie Frimpong", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Netherlands",
     "position": "DF", "age": 23, "number": 30},
    {"name": "Alejandro Grimaldo", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Spain",
     "position": "DF", "age": 28, "number": 20},
    {"name": "Jonathan Tah", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Germany", "position": "DF",
     "age": 28, "number": 4},
    {"name": "Piero Hincapié", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Ecuador",
     "position": "DF", "age": 22, "number": 3},
    {"name": "Exequiel Palacios", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Argentina",
     "position": "MF", "age": 25, "number": 25},
    {"name": "Victor Boniface", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Nigeria",
     "position": "FW", "age": 23, "number": 22},
    {"name": "Robert Andrich", "league": "Bundesliga", "team": "Bayer Leverkusen", "nation": "Germany",
     "position": "MF", "age": 29, "number": 8},
    {"name": "Gregor Kobel", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Switzerland",
     "position": "GK", "age": 26, "number": 1},
    {"name": "Nico Schlotterbeck", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany",
     "position": "DF", "age": 24, "number": 4},
    {"name": "Emre Can", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany", "position": "MF",
     "age": 30, "number": 23},
    {"name": "Julian Brandt", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany",
     "position": "MF", "age": 28, "number": 10},
    {"name": "Marcel Sabitzer", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Austria",
     "position": "MF", "age": 30, "number": 20},
    {"name": "Karim Adeyemi", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany",
     "position": "FW", "age": 22, "number": 27},
    {"name": "Donyell Malen", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Netherlands",
     "position": "FW", "age": 25, "number": 21},
    {"name": "Serhou Guirassy", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Guinea",
     "position": "FW", "age": 28, "number": 9},
    {"name": "Pascal Groß", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany", "position": "MF",
     "age": 33, "number": 13},
    {"name": "Waldemar Anton", "league": "Bundesliga", "team": "Borussia Dortmund", "nation": "Germany",
     "position": "DF", "age": 28, "number": 3},
    {"name": "Xavi Simons", "league": "Bundesliga", "team": "RB Leipzig", "nation": "Netherlands", "position": "MF",
     "age": 21, "number": 10},
    {"name": "Loïs Openda", "league": "Bundesliga", "team": "RB Leipzig", "nation": "Belgium", "position": "FW",
     "age": 24, "number": 11},
    {"name": "David Raum", "league": "Bundesliga", "team": "RB Leipzig", "nation": "Germany", "position": "DF",
     "age": 26, "number": 22},
    {"name": "Castello Lukeba", "league": "Bundesliga", "team": "RB Leipzig", "nation": "France", "position": "DF",
     "age": 21, "number": 23},
    {"name": "Benjamin Šeško", "league": "Bundesliga", "team": "RB Leipzig", "nation": "Slovenia", "position": "FW",
     "age": 21, "number": 30},
    {"name": "Deniz Undav", "league": "Bundesliga", "team": "VfB Stuttgart", "nation": "Germany", "position": "FW",
     "age": 28, "number": 26},
    {"name": "Angelo Stiller", "league": "Bundesliga", "team": "VfB Stuttgart", "nation": "MF", "age": 23, "number": 6},
    {"name": "Maximilian Mittelstädt", "league": "Bundesliga", "team": "VfB Stuttgart", "nation": "Germany",
     "position": "DF", "age": 27, "number": 7},
    {"name": "Chris Führich", "league": "Bundesliga", "team": "VfB Stuttgart", "nation": "Germany", "position": "MF",
     "age": 26, "number": 27},
    {"name": "Alexander Nübel", "league": "Bundesliga", "team": "VfB Stuttgart", "nation": "Germany", "position": "GK",
     "age": 27, "number": 33},
    {"name": "Kevin Trapp", "league": "Bundesliga", "team": "Eintracht Frankfurt", "nation": "Germany",
     "position": "GK", "age": 34, "number": 1},
    {"name": "Omar Marmoush", "league": "Bundesliga", "team": "Eintracht Frankfurt", "nation": "Egypt",
     "position": "FW", "age": 25, "number": 7},
    {"name": "Hugo Ekitiké", "league": "Bundesliga", "team": "Eintracht Frankfurt", "nation": "France",
     "position": "FW", "age": 22, "number": 11},
    {"name": "Mario Götze", "league": "Bundesliga", "team": "Eintracht Frankfurt", "nation": "Germany",
     "position": "MF", "age": 32, "number": 27},
    {"name": "Robin Koch", "league": "Bundesliga", "team": "Eintracht Frankfurt", "nation": "Germany", "position": "DF",
     "age": 28, "number": 4},
    {"name": "Andrej Kramarić", "league": "Bundesliga", "team": "TSG Hoffenheim", "nation": "Croatia", "position": "FW",
     "age": 33, "number": 27},
    {"name": "Oliver Baumann", "league": "Bundesliga", "team": "TSG Hoffenheim", "nation": "Germany", "position": "GK",
     "age": 34, "number": 1},
    {"name": "Ritsu Doan", "league": "Bundesliga", "team": "SC Freiburg", "nation": "Japan", "position": "FW",
     "age": 26, "number": 42},
    {"name": "Vincenzo Grifo", "league": "Bundesliga", "team": "SC Freiburg", "nation": "Italy", "position": "FW",
     "age": 31, "number": 32},
    {"name": "Matthias Ginter", "league": "Bundesliga", "team": "SC Freiburg", "nation": "Germany", "position": "DF",
     "age": 30, "number": 28},

    # Ligue 1
    {"name": "Ousmane Dembélé", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "France",
     "position": "FW", "age": 27, "number": 10},
    {"name": "Gianluigi Donnarumma", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Italy",
     "position": "GK", "age": 25, "number": 99},
    {"name": "Achraf Hakimi", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Morocco", "position": "DF",
     "age": 25, "number": 2},
    {"name": "Marquinhos", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Brazil", "position": "DF",
     "age": 30, "number": 5},
    {"name": "Nuno Mendes", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Portugal", "position": "DF",
     "age": 22, "number": 25},
    {"name": "Lucas Beraldo", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Brazil", "position": "DF",
     "age": 20, "number": 35},
    {"name": "Willian Pacho", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Ecuador", "position": "DF",
     "age": 22, "number": 51},
    {"name": "Vitinha", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Portugal", "position": "MF",
     "age": 24, "number": 17},
    {"name": "Warren Zaïre-Emery", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "France",
     "position": "MF", "age": 18, "number": 33},
    {"name": "Joao Neves", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Portugal", "position": "MF",
     "age": 19, "number": 87},
    {"name": "Fabian Ruiz", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Spain", "position": "MF",
     "age": 28, "number": 8},
    {"name": "Lee Kang-in", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "South Korea",
     "position": "MF", "age": 23, "number": 19},
    {"name": "Bradley Barcola", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "France",
     "position": "FW", "age": 21, "number": 29},
    {"name": "Gonçalo Ramos", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Portugal",
     "position": "FW", "age": 23, "number": 9},
    {"name": "Randal Kolo Muani", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "France",
     "position": "FW", "age": 25, "number": 23},
    {"name": "Marco Asensio", "league": "Ligue 1", "team": "Paris Saint-Germain", "nation": "Spain", "position": "FW",
     "age": 28, "number": 11},
    {"name": "Rayan Cherki", "league": "Ligue 1", "team": "Lyon", "nation": "France", "position": "MF", "age": 20,
     "number": 18},
    {"name": "Adrien Rabiot", "league": "Ligue 1", "team": "Marseille", "nation": "France", "position": "MF", "age": 29,
     "number": 25},
    {"name": "Elye Wahi", "league": "Ligue 1", "team": "Marseille", "nation": "France", "position": "FW", "age": 21,
     "number": 9},
    {"name": "Gerónimo Rulli", "league": "Ligue 1", "team": "Marseille", "nation": "Argentina", "position": "GK",
     "age": 32, "number": 1},
    {"name": "Leonardo Balerdi", "league": "Ligue 1", "team": "Marseille", "nation": "Argentina", "position": "DF",
     "age": 25, "number": 5},
    {"name": "Jonathan David", "league": "Ligue 1", "team": "Lille", "nation": "Canada", "position": "FW", "age": 24,
     "number": 9},
    {"name": "Maghnes Akliouche", "league": "Ligue 1", "team": "Monaco", "nation": "France", "position": "MF",
     "age": 22, "number": 21}
]

F1_DRIVERS = [
    {"name": "Max Verstappen", "team": "Red Bull Racing", "number": 1, "age": 27, "debut": 2015, "wins": 63},
    {"name": "Liam Lawson", "team": "Red Bull Racing", "number": 30, "age": 23, "debut": 2023, "wins": 0},
    {"name": "Lando Norris", "team": "McLaren", "number": 4, "age": 25, "debut": 2019, "wins": 4},
    {"name": "Oscar Piastri", "team": "McLaren", "number": 81, "age": 24, "debut": 2023, "wins": 2},
    {"name": "Charles Leclerc", "team": "Ferrari", "number": 16, "age": 27, "debut": 2018, "wins": 8},
    {"name": "Lewis Hamilton", "team": "Ferrari", "number": 44, "age": 40, "debut": 2007, "wins": 105},
    {"name": "George Russell", "team": "Mercedes", "number": 63, "age": 27, "debut": 2019, "wins": 2},
    {"name": "Andrea Kimi Antonelli", "team": "Mercedes", "number": 12, "age": 18, "debut": 2025, "wins": 0},
    {"name": "Fernando Alonso", "team": "Aston Martin", "number": 14, "age": 43, "debut": 2001, "wins": 32},
    {"name": "Lance Stroll", "team": "Aston Martin", "number": 18, "age": 26, "debut": 2017, "wins": 0},
    {"name": "Pierre Gasly", "team": "Alpine", "number": 10, "age": 29, "debut": 2017, "wins": 1},
    {"name": "Jack Doohan", "team": "Alpine", "number": 7, "age": 22, "debut": 2025, "wins": 0},
    {"name": "Franco Colapinto", "team": "Alpine", "number": 43, "age": 21, "debut": 2024, "wins": 0},
    {"name": "Esteban Ocon", "team": "Haas", "number": 31, "age": 28, "debut": 2016, "wins": 1},
    {"name": "Oliver Bearman", "team": "Haas", "number": 87, "age": 19, "debut": 2024, "wins": 0},
    {"name": "Yuki Tsunoda", "team": "Racing Bulls", "number": 22, "age": 24, "debut": 2021, "wins": 0},
    {"name": "Isack Hadjar", "team": "Racing Bulls", "number": 6, "age": 20, "debut": 2025, "wins": 0},
    {"name": "Nico Hülkenberg", "team": "Kick Sauber", "number": 27, "age": 37, "debut": 2010, "wins": 0},
    {"name": "Gabriel Bortoleto", "team": "Kick Sauber", "number": 5, "age": 20, "debut": 2025, "wins": 0},
    {"name": "Alexander Albon", "team": "Williams", "number": 23, "age": 28, "debut": 2019, "wins": 0},
    {"name": "Carlos Sainz Jr.", "team": "Williams", "number": 55, "age": 30, "debut": 2015, "wins": 4},

    {"name": "Sergio Pérez", "team": "Red Bull Racing", "number": 11, "age": 34, "debut": 2011, "wins": 6},
    {"name": "Daniel Ricciardo", "team": "RB", "number": 3, "age": 35, "debut": 2011, "wins": 8},
    {"name": "Valtteri Bottas", "team": "Kick Sauber", "number": 77, "age": 35, "debut": 2013, "wins": 10},
    {"name": "Kevin Magnussen", "team": "Haas", "number": 20, "age": 32, "debut": 2014, "wins": 0},
    {"name": "Zhou Guanyu", "team": "Kick Sauber", "number": 24, "age": 25, "debut": 2022, "wins": 0},
    {"name": "Logan Sargeant", "team": "Williams", "number": 2, "age": 24, "debut": 2023, "wins": 0},

    {"name": "Nyck de Vries", "team": "AlphaTauri", "number": 21, "age": 31, "debut": 2022, "wins": 0},

    {"name": "Sebastian Vettel", "team": "Aston Martin", "number": 5, "age": 35, "debut": 2007, "wins": 53},
    {"name": "Mick Schumacher", "team": "Haas", "number": 47, "age": 23, "debut": 2021, "wins": 0},
    {"name": "Nicholas Latifi", "team": "Williams", "number": 6, "age": 27, "debut": 2020, "wins": 0},

    {"name": "Antonio Giovinazzi", "team": "Alfa Romeo", "number": 99, "age": 28, "debut": 2017, "wins": 0},
    {"name": "Nikita Mazepin", "team": "Haas", "number": 9, "age": 22, "debut": 2021, "wins": 0},
    {"name": "Robert Kubica", "team": "Alfa Romeo", "number": 88, "age": 37, "debut": 2006, "wins": 1},

    {"name": "Nico Rosberg", "team": "Mercedes", "number": 6, "age": 31, "debut": 2006, "wins": 23},
    {"name": "Romain Grosjean", "team": "Haas", "number": 8, "age": 34, "debut": 2009, "wins": 0},
    {"name": "Daniil Kvyat", "team": "AlphaTauri", "number": 26, "age": 26, "debut": 2014, "wins": 0},
    {"name": "Pietro Fittipaldi", "team": "Haas", "number": 51, "age": 24, "debut": 2020, "wins": 0},
    {"name": "Jack Aitken", "team": "Williams", "number": 89, "age": 25, "debut": 2020, "wins": 0},
    {"name": "Marcus Ericsson", "team": "Sauber", "number": 9, "age": 28, "debut": 2014, "wins": 0},
    {"name": "Felipe Massa", "team": "Williams", "number": 19, "age": 36, "debut": 2002, "wins": 11},
    {"name": "Felipe Nasr", "team": "Sauber", "number": 12, "age": 24, "debut": 2015, "wins": 0},
    {"name": "Alexander Rossi", "team": "Manor Marussia", "number": 53, "age": 24, "debut": 2015, "wins": 0},

    {"name": "Mark Webber", "team": "Red Bull Racing", "number": 2, "age": 37, "debut": 2002, "wins": 9},
    {"name": "Michael Schumacher", "team": "Mercedes", "number": 7, "age": 43, "debut": 1991, "wins": 91},
    {"name": "Rubens Barrichello", "team": "Williams", "number": 11, "age": 39, "debut": 1993, "wins": 11},
    {"name": "Bruno Senna", "team": "Williams", "number": 19, "age": 29, "debut": 2010, "wins": 0},
    {"name": "Max Chilton", "team": "Marussia", "number": 4, "age": 23, "debut": 2013, "wins": 0},
    {"name": "Giedo van der Garde", "team": "Caterham", "number": 21, "age": 28, "debut": 2013, "wins": 0},

    {"name": "Michael Schumacher", "team": "Ferrari", "number": 1, "age": 36, "debut": 1991, "wins": 91},
    {"name": "Fernando Alonso", "team": "Renault", "number": 5, "age": 24, "debut": 2001, "wins": 32},
    {"name": "Kimi Räikkönen", "team": "McLaren", "number": 9, "age": 26, "debut": 2001, "wins": 21},
    {"name": "Ralf Schumacher", "team": "Toyota", "number": 17, "age": 30, "debut": 1997, "wins": 6},
    {"name": "Jenson Button", "team": "BAR Honda", "number": 3, "age": 25, "debut": 2000, "wins": 15},
    {"name": "Mark Webber", "team": "Williams", "number": 7, "age": 29, "debut": 2002, "wins": 9},
    {"name": "Felipe Massa", "team": "Sauber", "number": 12, "age": 24, "debut": 2002, "wins": 11},

    {"name": "Ayrton Senna", "team": "McLaren", "number": 1, "age": 34, "debut": 1984, "wins": 41},
    {"name": "Alain Prost", "team": "Williams", "number": 2, "age": 38, "debut": 1980, "wins": 51},
    {"name": "Niki Lauda", "team": "McLaren", "number": 8, "age": 36, "debut": 1971, "wins": 25},
    {"name": "Juan Manuel Fangio", "team": "Maserati", "number": 1, "age": 47, "debut": 1950, "wins": 24},
    {"name": "Jackie Stewart", "team": "Tyrrell", "number": 1, "age": 34, "debut": 1965, "wins": 27},
    {"name": "Jim Clark", "team": "Lotus", "number": 1, "age": 32, "debut": 1960, "wins": 25},
    {"name": "Nigel Mansell", "team": "Williams", "number": 5, "age": 41, "debut": 1980, "wins": 31},
    {"name": "Nelson Piquet", "team": "Benetton", "number": 20, "age": 39, "debut": 1978, "wins": 23},
    {"name": "Gilles Villeneuve", "team": "Ferrari", "number": 27, "age": 32, "debut": 1977, "wins": 6},
    {"name": "James Hunt", "team": "McLaren", "number": 1, "age": 31, "debut": 1973, "wins": 10},
    {"name": "Emerson Fittipaldi", "team": "McLaren", "number": 1, "age": 33, "debut": 1970, "wins": 14},
    {"name": "Graham Hill", "team": "BRM", "number": 1, "age": 46, "debut": 1958, "wins": 14},
    {"name": "Jack Brabham", "team": "Brabham", "number": 1, "age": 44, "debut": 1955, "wins": 14},
    {"name": "Stirling Moss", "team": "Vanwall", "number": 18, "age": 32, "debut": 1951, "wins": 16},
    {"name": "Mario Andretti", "team": "Lotus", "number": 1, "age": 42, "debut": 1968, "wins": 12},
    {"name": "Damon Hill", "team": "Jordan", "number": 9, "age": 39, "debut": 1992, "wins": 22},
    {"name": "Jacques Villeneuve", "team": "BAR", "number": 22, "age": 28, "debut": 1996, "wins": 11},
    {"name": "Mika Häkkinen", "team": "McLaren", "number": 1, "age": 31, "debut": 1991, "wins": 20}
]
MAX_TRIES = 7


def get_daily_target(db):
    if not db:
        return None
    today_seed = int(datetime.date.today().strftime("%Y%m%d"))
    rng = random.Random(today_seed)
    return rng.choice(db)


def get_random_target(db):
    if not db:
        return None
    return random.choice(db)


# ==========================================
# 3. STATE & STORAGE MANAGEMENT
# ==========================================
# Check for restored state in query params
if "data" in st.query_params:
    try:
        st.session_state.sports_data = json.loads(st.query_params["data"])
    except Exception:
        pass

# Fallback initialization if sports_data isn't populated
if "sports_data" not in st.session_state:
    st.session_state.sports_data = {
        "Cricket": {
            "stats": {"played": 0, "won": 0, "streak": 0, "max_streak": 0},
            "guesses": [],
            "game_over": False,
            "show_hints": False,
            "daily_completed_date": None,
            "target_player": get_daily_target(CRICKET_PLAYERS),
        },
        "Football": {
            "stats": {"played": 0, "won": 0, "streak": 0, "max_streak": 0},
            "guesses": [],
            "game_over": False,
            "show_hints": False,
            "daily_completed_date": None,
            "target_player": get_daily_target(PLAYERS),
        },
        "F1": {
            "stats": {"played": 0, "won": 0, "streak": 0, "max_streak": 0},
            "guesses": [],
            "game_over": False,
            "show_hints": False,
            "daily_completed_date": None,
            "target_player": get_daily_target(F1_DRIVERS),
        },
    }

if "game_mode" not in st.session_state:
    st.session_state.game_mode = "Daily Challenge"


def save_and_sync():
    """Syncs session state directly to browser LocalStorage and query params."""
    json_data = json.dumps(st.session_state.sports_data)
    st.query_params["data"] = json_data

    st.html(f"""
        <script>
            try {{
                localStorage.setItem('sportsle_v4_data', JSON.stringify({json_data}));
            }} catch(e) {{}}
        </script>
    """)


# Restore from browser LocalStorage on initial site load if URL param is absent
if "restored_init" not in st.session_state:
    st.session_state.restored_init = True
    if "data" not in st.query_params:
        st.html("""
            <script>
                try {
                    const saved = localStorage.getItem('sportsle_v4_data');
                    if (saved) {
                        const url = new URL(window.location.href);
                        url.searchParams.set('data', saved);
                        window.location.href = url.toString();
                    }
                } catch(e) {}
            </script>
        """)

# Active Sport reference
active_sport = st.session_state.sport
current_sport_data = st.session_state.sports_data[active_sport]


def get_current_database():
    if st.session_state.sport == "Cricket":
        return CRICKET_PLAYERS
    elif st.session_state.sport == "Football":
        return PLAYERS
    else:
        return F1_DRIVERS


def start_new_game(mode=None, sport=None):
    if sport:
        st.session_state.sport = sport
    if mode:
        st.session_state.game_mode = mode

    active_sp = st.session_state.sport
    sp_data = st.session_state.sports_data[active_sp]

    sp_data["guesses"] = []
    sp_data["game_over"] = False
    sp_data["show_hints"] = False

    current_db = get_current_database()
    if st.session_state.game_mode == "Daily Challenge":
        sp_data["target_player"] = get_daily_target(current_db)
    else:
        sp_data["target_player"] = get_random_target(current_db)

    save_and_sync()


today_str = str(datetime.date.today())
is_daily_already_done = (
    st.session_state.game_mode == "Daily Challenge"
    and current_sport_data["daily_completed_date"] == today_str
)

# ==========================================
# 4. SIDEBAR - INDIVIDUAL RECORD & MODES
# ==========================================
with st.sidebar:
    st.markdown("### 🏆 Select Sport")

    sport_options = ["🏏 Cricket", "⚽ Football", "🏎️ F1"]

    current_index = 0
    if st.session_state.sport == "Football":
        current_index = 1
    elif st.session_state.sport == "F1":
        current_index = 2

    selected_sport_raw = st.radio(
        "Select Sport",
        options=sport_options,
        index=current_index,
        label_visibility="collapsed",
    )

    if "Cricket" in selected_sport_raw:
        selected_sport = "Cricket"
    elif "Football" in selected_sport_raw:
        selected_sport = "Football"
    else:
        selected_sport = "F1"

    if selected_sport != st.session_state.sport:
        st.session_state.sport = selected_sport
        st.rerun()

    st.markdown("---")

    st.markdown("### 🎮 Game Mode")
    selected_mode = st.radio(
        "Select Mode",
        options=["Daily Challenge", "Practice Mode"],
        index=0 if st.session_state.game_mode == "Daily Challenge" else 1,
        label_visibility="collapsed",
    )

    if selected_mode != st.session_state.game_mode:
        start_new_game(selected_mode, st.session_state.sport)
        st.rerun()

    st.markdown("---")

    st.markdown(f"### {st.session_state.sport} Stats")
    stats = current_sport_data["stats"]

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Played", stats["played"])
        st.metric("Current Streak", stats["streak"])
    with col_s2:
        win_pct = (
            round((stats["won"] / stats["played"] * 100))
            if stats["played"] > 0
            else 0
        )
        st.metric("Win %", f"{win_pct}%")
        st.metric("Max Streak", stats["max_streak"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("New Practice Target") and st.session_state.game_mode == "Practice Mode":
        start_new_game("Practice Mode", st.session_state.sport)
        st.rerun()

# ==========================================
# 5. DIALOG / POPUP MODAL ON WIN OR LOSS
# ==========================================
@st.dialog("🎯 Game Result")
def show_result_popup(is_win, target_player, attempts_count):
    if is_win:
        st.markdown(f"### 🎉 Spectacular Victory!")
        st.markdown(f"You guessed **{target_player['name']}** in **{attempts_count}** attempts!")
        st.balloons()
    else:
        st.markdown(f"### ❌ Hard Luck!")
        st.markdown(f"Out of tries! The hidden player was **{target_player['name']}**.")

    st.markdown("---")
    st.markdown("#### 📊 Updated Stats")
    s = current_sport_data["stats"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Played", s["played"])
    c2.metric("Won", s["won"])
    c3.metric("Streak", s["streak"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.session_state.game_mode == "Practice Mode":
        if st.button("Play Next Game"):
            start_new_game("Practice Mode", st.session_state.sport)
            st.rerun()

# ==========================================
# 6. MAIN GAME INTERFACE & LOGIC
# ==========================================
st.markdown(
    f"""
    <div class="title-container">
        <span class="logo-icon">🏆</span>
        <h1 class="main-title">SPORTSLE ({active_sport.upper()})</h1>
    </div>
""",
    unsafe_allow_html=True,
)

tries_left = MAX_TRIES - len(current_sport_data["guesses"])
st.markdown(
    f'<div class="tries-counter">Tries Left: <b>{tries_left} / {MAX_TRIES}</b> | Mode: <b>{st.session_state.game_mode}</b></div>',
    unsafe_allow_html=True,
)

target = current_sport_data["target_player"]
db = get_current_database()

guessed_names = [g["name"] for g in current_sport_data["guesses"]]
available_players = [p for p in db if p["name"] not in guessed_names]

col_select, col_submit = st.columns([3, 1], gap="medium")

with col_select:
    selected_guess = st.selectbox(
        "Guess a player:",
        options=[""] + [p["name"] for p in available_players],
        disabled=current_sport_data["game_over"] or is_daily_already_done,
        key=f"guess_select_{active_sport}",
        label_visibility="collapsed",
    )


def handle_guess():
    if not selected_guess or current_sport_data["game_over"]:
        return

    guessed_obj = next((p for p in db if p["name"] == selected_guess), None)
    if not guessed_obj:
        return

    current_sport_data["guesses"].append(guessed_obj)

    if guessed_obj["name"] == target["name"]:
        current_sport_data["game_over"] = True
        stats["played"] += 1
        stats["won"] += 1
        stats["streak"] += 1
        stats["max_streak"] = max(stats["streak"], stats["max_streak"])
        if st.session_state.game_mode == "Daily Challenge":
            current_sport_data["daily_completed_date"] = today_str
        save_and_sync()
        show_result_popup(True, target, len(current_sport_data["guesses"]))

    elif len(current_sport_data["guesses"]) >= MAX_TRIES:
        current_sport_data["game_over"] = True
        stats["played"] += 1
        stats["streak"] = 0
        if st.session_state.game_mode == "Daily Challenge":
            current_sport_data["daily_completed_date"] = today_str
        save_and_sync()
        show_result_popup(False, target, len(current_sport_data["guesses"]))
    else:
        save_and_sync()


with col_submit:
    st.button(
        "Submit Guess",
        on_click=handle_guess,
        disabled=current_sport_data["game_over"] or not selected_guess,
    )

st.markdown("<br>", unsafe_allow_html=True)


def compare_field(val1, val2):
    if str(val1).lower() == str(val2).lower():
        return "grid-card-correct"

    try:
        v1, v2 = float(val1), float(val2)
        if v1 < v2:
            return "grid-card-wrong", " ↑"
        elif v1 > v2:
            return "grid-card-wrong", " ↓"
    except (ValueError, TypeError):
        pass

    return "grid-card-wrong", ""


if current_sport_data["guesses"]:
    if active_sport == "Cricket":
        cols = st.columns(7, gap="small")
        headers = ["Name", "Country", "Status", "Role", "Batting", "Age", "Franchise"]
    elif active_sport == "Football":
        cols = st.columns(7, gap="small")
        headers = ["Name", "League", "Team", "Nation", "Pos", "Age", "No."]
    else:
        cols = st.columns(6, gap="small")
        headers = ["Name", "Team", "No.", "Age", "Debut", "Wins"]

    for col, h in zip(cols, headers):
        col.markdown(f'<div class="grid-header">{h}</div>', unsafe_allow_html=True)

    for guess in reversed(current_sport_data["guesses"]):
        if active_sport == "Cricket":
            fields = [
                ("name", guess["name"], "grid-card-correct" if guess["name"] == target["name"] else "grid-card-neutral"),
                ("Country", guess["Country"], compare_field(guess["Country"], target["Country"])),
                ("status", guess["status"], compare_field(guess["status"], target["status"])),
                ("Role", guess["Role"], compare_field(guess["Role"], target["Role"])),
                ("Batting Hand", guess["Batting Hand"], compare_field(guess["Batting Hand"], target["Batting Hand"])),
                ("Age", guess["Age"], compare_field(guess["Age"], target["Age"])),
                ("Franchise", guess["Franchise"], compare_field(guess["Franchise"], target["Franchise"])),
            ]
        elif active_sport == "Football":
            fields = [
                ("name", guess["name"], "grid-card-correct" if guess["name"] == target["name"] else "grid-card-neutral"),
                ("league", guess["league"], compare_field(guess["league"], target["league"])),
                ("team", guess["team"], compare_field(guess["team"], target["team"])),
                ("nation", guess["nation"], compare_field(guess["nation"], target["nation"])),
                ("position", guess["position"], compare_field(guess["position"], target["position"])),
                ("age", guess["age"], compare_field(guess["age"], target["age"])),
                ("number", guess["number"], compare_field(guess["number"], target["number"])),
            ]
        else:
            fields = [
                ("name", guess["name"], "grid-card-correct" if guess["name"] == target["name"] else "grid-card-neutral"),
                ("team", guess["team"], compare_field(guess["team"], target["team"])),
                ("number", guess["number"], compare_field(guess["number"], target["number"])),
                ("age", guess["age"], compare_field(guess["age"], target["age"])),
                ("debut", guess["debut"], compare_field(guess["debut"], target["debut"])),
                ("wins", guess["wins"], compare_field(guess["wins"], target["wins"])),
            ]

        grid_cols = st.columns(len(fields), gap="small")
        for col, item in zip(grid_cols, fields):
            val = item[1]
            style_info = item[2]

            arrow = ""
            if isinstance(style_info, tuple):
                css_class, arrow = style_info
            else:
                css_class = style_info

            col.markdown(f'<div class="{css_class}">{val}{arrow}</div>', unsafe_allow_html=True)