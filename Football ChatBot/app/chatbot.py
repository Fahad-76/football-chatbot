#
#  chatbot.py
#  FBref Bot
#
#  Handles user queries about football stats:
#  - Single player stats
#  - Player vs. player comparisons
#  - Top stat queries (league-wide or per team)
#

from app.database import PlayerStats

# Load player stats from CSV once
stats_db = PlayerStats()

# Known team names to help detect team-specific queries
known_teams = [
    "arsenal", "aston villa", "bournemouth", "brentford", "brighton",
    "burnley", "chelsea", "crystal palace", "everton", "fulham", "ipswich",
    "liverpool", "manchester city", "man city", "manchester united", "man united",
    "newcastle", "nottingham forest", "sheffield united", "tottenham", "spurs",
    "west ham", "wolverhampton", "wolves"
]

# =========================================
# Extract a single player's name from free text
# =========================================
def extract_player_query(text):
    text = text.lower().strip()
    trigger_words = [
        "stats", "goals", "age", "position", "show", "tell", "info", "data",
        "how", "many", "does", "have"
    ]
    tokens = text.split()
    player_query = [word for word in tokens if word not in trigger_words]
    if not player_query:
        return None, "Couldn't extract player name."
    return " ".join(player_query), None

# =========================================
# Extract two player names from a comparison query
# =========================================
def extract_comparison_query(text):
    text = text.lower().strip()
    for keyword in ["compare", "versus", "vs", "with"]:
        text = text.replace(keyword, "and")
    parts = [p.strip() for p in text.split("and") if p.strip()]
    if len(parts) == 2:
        return parts[0], parts[1]
    return None, None

# =========================================
# League-wide top N players by stat
# =========================================
def get_top_players(stat="goals", title="🏆 Top Players", limit=10):
    try:
        df = stats_db.df.copy()
        df = df[df[stat].apply(lambda x: str(x).isdigit())]
        df[stat] = df[stat].astype(int)
        top_df = df.sort_values(by=stat, ascending=False).head(limit)
        lines = [f"{title}:\n"]
        for i, row in enumerate(top_df.itertuples(), 1):
            lines.append(f"{i}. {row.player}\n ({row.team})\n - {getattr(row, stat)}\n {stat}\n")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Failed to fetch top {stat} players: {e}"

# =========================================
# Top N players from a specific team
# =========================================
def get_team_top_players(team_name, stat="goals", title="Top Performers", limit=3):
    try:
        df = stats_db.df.copy()
        df["team"] = df["team"].str.lower()
        df = df[df["team"].str.contains(team_name.lower())]
        if df.empty:
            return f"❌ No data found for team '{team_name}'."
        df = df[df[stat].apply(lambda x: str(x).isdigit())]
        df[stat] = df[stat].astype(int)
        top_df = df.sort_values(by=stat, ascending=False).head(limit)
        lines = [f"📊 {title} for {team_name.title()}:\n"]
        for i, row in enumerate(top_df.itertuples(), 1):
            lines.append(f"{i}. {row.player} - {getattr(row, stat)} {stat}")
        return "\n".join(lines)
    except Exception as e:
        return f"❌ Failed to get top {stat} players from {team_name}: {e}"

# =========================================
# Main chatbot handler: routes text to correct logic
# =========================================
def handle_query(text):
    lowered = text.lower().strip()

    # 1. Team-name-first phrasing (e.g. "arsenal top scorers")
    for team in known_teams:
        if lowered.startswith(team) and "top" in lowered:
            if "goal" in lowered or "scorer" in lowered:
                return get_team_top_players(team, stat="goals", title=f"🏆 Top Scorers")
            elif "assist" in lowered:
                return get_team_top_players(team, stat="assists", title=f"🎯 Top Assist Providers")
            elif "g+a" in lowered or "ga" in lowered:
                return get_team_top_players(team, stat="ga", title=f"⚡ Top G+A Contributors")

    # 2. "Top [stat] from/for [team]" phrasing
    if "from" in lowered or "for" in lowered:
        tokens = lowered.split()
        if "goal" in lowered or "scorer" in lowered:
            stat = "goals"
            label = "🏆 Top Scorers"
        elif "assist" in lowered:
            stat = "assists"
            label = "🎯 Top Assist Providers"
        elif "g+a" in lowered or "ga" in lowered:
            stat = "ga"
            label = "⚡ Top G+A Contributors"
        else:
            stat = "goals"
            label = "🏆 Top Performers"

        # Guess team name: all words after "from" or "for"
        if "from" in tokens:
            idx = tokens.index("from")
        elif "for" in tokens:
            idx = tokens.index("for")
        else:
            idx = -1

        team_name = " ".join(tokens[idx + 1:]) if idx != -1 else ""
        return get_team_top_players(team_name, stat=stat, title=label)

    # 3. Player-vs-player comparison
    player1, player2 = extract_comparison_query(text)
    if player1 and player2:
        stats1 = stats_db.get_stats(player1)
        stats2 = stats_db.get_stats(player2)
        if not stats1 or not stats2:
            return "❌ Sorry, I couldn't find data for both players."
        return (
            f"📊 {stats1['player']} vs. {stats2['player']}\n\n"
            f"{'Stat':<12} | {stats1['player']:<15} | {stats2['player']:<15}\n"
            f"{'-'*45}\n"
            f"{'Team':<12} | {stats1['team']:<15} | {stats2['team']:<15}\n"
            f"{'Goals':<12} | {stats1['goals']:<15} | {stats2['goals']:<15}\n"
            f"{'Assists':<12} | {stats1['assists']:<15} | {stats2['assists']:<15}\n"
            f"{'G+A':<12} | {stats1['ga']:<15} | {stats2['ga']:<15}"
        )

    # 4. League-wide top stats
    if "top" in lowered:
        if "goal" in lowered or "scorer" in lowered:
            return get_top_players(stat="goals", title="🏆 Top Goal Scorers")
        elif "assist" in lowered:
            return get_top_players(stat="assists", title="🎯 Top Assist Providers")
        elif "g+a" in lowered or "ga" in lowered:
            return get_top_players(stat="ga", title="⚡ Top G+A Contributors")

    # 5. Fallback to single player query
    player_name, error = extract_player_query(text)
    if error:
        return "❌ Sorry, I couldn't understand your question."
    result = stats_db.get_stats(player_name)
    if not result:
        return f"❌ Sorry, I couldn't find data for '{player_name}'."
    return (
        f"📊 {result['player']} ({result['team']})\n"
        f"Position: {result['position']}\n"
        f"Age: {result['age']}\n"
        f"Goals: {result['goals']}\n"
        f"Assists: {result['assists']}\n"
        f"G+A: {result['ga']}"
    )
