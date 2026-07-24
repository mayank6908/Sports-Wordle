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

st.markdown(
    f"""
    <style>
    header[data-testid="stHeader"] {{
        background-color: transparent !important;
        visibility: visible !important;
    }}

    .stApp {{
        background-color: #070b14;
        color: #ffffff;
    }}

    [data-testid="stSidebar"] {{
        background-color: #090e1a !important;
        border-right: 1px solid #1e293b;
    }}

    [data-testid="stSidebar"] * {{
        color: #f8fafc !important;
    }}

    div.stButton > button {{
        background-color: {accent_color} !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 8px !important;
        height: 46px !important;
        width: 100% !important;
        border: none !important;
        box-shadow: 0 4px 14px {accent_color}66 !important;
        transition: all 0.2s ease;
        margin-top: 4px;
    }}
    div.stButton > button:hover {{
        background-color: {accent_hover} !important;
    }}

    .title-container {{
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 12px;
        margin-top: 5px;
        margin-bottom: 5px;
    }}

    .main-title {{
        font-size: 2.8rem;
        font-weight: 900;
        color: {accent_color};
        letter-spacing: 2px;
        margin: 0;
    }}

    .logo-icon {{
        font-size: 2.5rem;
    }}

    .tries-counter {{
        text-align: center;
        color: #94a3b8;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 25px;
    }}

    .grid-header {{
        background-color: #111827;
        color: #9ca3af;
        text-align: center;
        padding: 12px 8px;
        font-size: 0.8rem;
        font-weight: 800;
        border-radius: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
        border: 1px solid #1f2937;
        margin-bottom: 12px;
    }}

    .grid-card-neutral {{
        background-color: #1e293b;
        color: #e2e8f0;
        text-align: center;
        padding: 14px 8px;
        font-size: 0.9rem;
        font-weight: 700;
        border-radius: 8px;
        border: 1px solid #334155;
        min-height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
    }}

    .grid-card-correct {{
        background-color: #16a34a;
        color: #ffffff;
        text-align: center;
        padding: 14px 8px;
        font-size: 0.9rem;
        font-weight: 700;
        border-radius: 8px;
        min-height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        box-shadow: 0 0 12px rgba(22, 163, 74, 0.4);
    }}

    .grid-card-wrong {{
        background-color: #dc2626;
        color: #ffffff;
        text-align: center;
        padding: 14px 8px;
        font-size: 0.9rem;
        font-weight: 700;
        border-radius: 8px;
        min-height: 52px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 8px;
        box-shadow: 0 0 12px rgba(220, 38, 38, 0.4);
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. DATABASES
# ==========================================
CRICKET_PLAYERS = [
    {"name": "Sachin Tendulkar", "Country": "India", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 53, "Franchise": "Mumbai Indians"},
    {"name": "MS Dhoni", "Country": "India", "status": "Active", "Role": "WK", "Batting Hand": "Right", "Age": 45, "Franchise": "Chennai Super Kings"},
    {"name": "Virat Kohli", "Country": "India", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 37, "Franchise": "Royal Challengers Bengaluru"},
    {"name": "Rohit Sharma", "Country": "India", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 39, "Franchise": "Mumbai Indians"},
    {"name": "Jasprit Bumrah", "Country": "India", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 32, "Franchise": "Mumbai Indians"},
    {"name": "Steve Smith", "Country": "Australia", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 37, "Franchise": "Rajasthan Royals"},
    {"name": "Pat Cummins", "Country": "Australia", "status": "Active", "Role": "BOWL", "Batting Hand": "Right", "Age": 33, "Franchise": "Sunrisers Hyderabad"},
    {"name": "Joe Root", "Country": "England", "status": "Active", "Role": "BAT", "Batting Hand": "Right", "Age": 35, "Franchise": "Rajasthan Royals"},
    {"name": "Ben Stokes", "Country": "England", "status": "Retired", "Role": "ALL", "Batting Hand": "Left", "Age": 35, "Franchise": "Chennai Super Kings"},
    {"name": "Kane Williamson", "Country": "New Zealand", "status": "Retired", "Role": "BAT", "Batting Hand": "Right", "Age": 35, "Franchise": "Gujarat Titans"},
    {"name": "Rashid Khan", "Country": "Afghanistan", "status": "Active", "Role": "ALL", "Batting Hand": "Right", "Age": 27, "Franchise": "Gujarat Titans"},
]

FOOTBALL_PLAYERS = [
    {"name": "Erling Haaland", "league": "Premier League", "team": "Manchester City", "nation": "Norway", "position": "FW", "age": 24, "number": 9},
    {"name": "Kevin De Bruyne", "league": "Premier League", "team": "Manchester City", "nation": "Belgium", "position": "MF", "age": 33, "number": 17},
    {"name": "Bukayo Saka", "league": "Premier League", "team": "Arsenal", "nation": "England", "position": "FW", "age": 22, "number": 7},
    {"name": "Mohamed Salah", "league": "Premier League", "team": "Liverpool", "nation": "Egypt", "position": "FW", "age": 32, "number": 11},
    {"name": "Jude Bellingham", "league": "La Liga", "team": "Real Madrid", "nation": "England", "position": "MF", "age": 21, "number": 5},
    {"name": "Kylian Mbappé", "league": "La Liga", "team": "Real Madrid", "nation": "France", "position": "FW", "age": 25, "number": 9},
    {"name": "Vinícius Júnior", "league": "La Liga", "team": "Real Madrid", "nation": "Brazil", "position": "FW", "age": 24, "number": 7},
    {"name": "Lamine Yamal", "league": "La Liga", "team": "Barcelona", "nation": "Spain", "position": "FW", "age": 17, "number": 19},
    {"name": "Harry Kane", "league": "Bundesliga", "team": "Bayern Munich", "nation": "England", "position": "FW", "age": 30, "number": 9},
    {"name": "Lautaro Martínez", "league": "Serie A", "team": "Inter Milan", "nation": "Argentina", "position": "FW", "age": 26, "number": 10},
]

F1_DRIVERS = [
    {"name": "Max Verstappen", "team": "Red Bull Racing", "number": 1, "age": 27, "debut": 2015, "wins": 63},
    {"name": "Lando Norris", "team": "McLaren", "number": 4, "age": 25, "debut": 2019, "wins": 4},
    {"name": "Oscar Piastri", "team": "McLaren", "number": 81, "age": 24, "debut": 2023, "wins": 2},
    {"name": "Charles Leclerc", "team": "Ferrari", "number": 16, "age": 27, "debut": 2018, "wins": 8},
    {"name": "Lewis Hamilton", "team": "Ferrari", "number": 44, "age": 40, "debut": 2007, "wins": 105},
    {"name": "George Russell", "team": "Mercedes", "number": 63, "age": 27, "debut": 2019, "wins": 2},
    {"name": "Fernando Alonso", "team": "Aston Martin", "number": 14, "age": 43, "debut": 2001, "wins": 32},
    {"name": "Carlos Sainz Jr.", "team": "Williams", "number": 55, "age": 30, "debut": 2015, "wins": 4},
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
            "target_player": get_daily_target(FOOTBALL_PLAYERS),
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
        return FOOTBALL_PLAYERS
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