"""
AI Quiz Arena
Interactive quiz game for Artificial Intelligence (Units I and II)
Built with Python and Streamlit.

How the app is organised
    1. Settings and small helper functions
    2. Game logic (start a game, check an answer, go to the next question)
    3. Screens (home, quiz, result, leaderboard, teacher question bank, about)
    4. Main part at the bottom that draws the banner and the tabs

The look of the app (colours, cards, buttons) is written in style.css.
"""
import html
import json
import os
import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

from questions import QUESTIONS, TOPICS

st.set_page_config(page_title="AI Quiz Arena", layout="centered")

# ----------------------------------------------------------------------
# 1. Settings and helper functions
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_POINTS = {"Easy": 10, "Medium": 20, "Hard": 30}   # points for a correct answer
BASE_TIME = {"Easy": 30, "Medium": 45, "Hard": 60}     # seconds per question
LIFELINES_AT_START = {"hint": 3, "fifty": 2, "skip": 1}
CHOICE_TYPES = ("MCQ", "Scenario", "Problem Solving", "True/False", "Assertion-Reason")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")


def load_css():
    """Read the design from style.css and give it to the page."""
    try:
        with open(os.path.join(BASE_DIR, "style.css"), encoding="utf-8") as f:
            css = f.read()
    except OSError:
        css = ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def teacher_passcode():
    """Passcode for the teacher question-bank page (can be changed in Streamlit secrets)."""
    try:
        return st.secrets["TEACHER_PASSCODE"]
    except Exception:
        return "teacher123"


def time_limit(q):
    """Seconds allowed for a question. Problem solving and matching get 30 extra seconds."""
    extra = 30 if q["type"] in ("Problem Solving", "Match the Following") else 0
    return BASE_TIME[q["level"]] + extra


def seconds_left(q):
    return time_limit(q) - (time.time() - st.session_state.q_start)


def safe(text):
    """Escape * so that text such as 'A*' is shown as written and not read as markdown italics."""
    return str(text).replace("*", "\\*")


def esc(text):
    """Make text safe to put inside our own HTML cards (keeps line breaks)."""
    return html.escape(str(text)).replace("\n", "<br>")


def clean(text):
    """Lower-case and keep only letters and digits, so 'Rationally.' matches 'rationally'."""
    return "".join(ch for ch in str(text).lower() if ch.isalnum())


def is_correct(q, user):
    if q["type"] == "Fill in the Blank":
        return clean(user) in [clean(a) for a in q["answer"]]
    if q["type"] == "Match the Following":
        return all(u == pair[1] for u, pair in zip(user, q["pairs"]))
    return user == q["answer"]


def correct_answer_text(q):
    if q["type"] == "Fill in the Blank":
        return q["answer"][0]
    if q["type"] == "Match the Following":
        return "\n".join(f"- {left}  ->  {right}" for left, right in q["pairs"])
    return q["answer"]


def user_answer_text(q, user):
    if user is None:
        return "(no answer)"
    if q["type"] == "Match the Following":
        return "\n".join(f"- {pair[0]}  ->  {u}" for pair, u in zip(q["pairs"], user))
    return str(user) if str(user).strip() else "(no answer)"


# ---------- leaderboard (saved in a small JSON file) ----------
def load_leaderboard():
    board = []
    try:
        with open(LEADERBOARD_FILE) as f:
            board = json.load(f)
    except Exception:
        pass
    board = board + st.session_state.get("local_board", [])
    return sorted(board, key=lambda e: (-e["score"], e["time"]))


def save_to_leaderboard(entry):
    board = []
    try:
        with open(LEADERBOARD_FILE) as f:
            board = json.load(f)
    except Exception:
        pass
    board.append(entry)
    board = sorted(board, key=lambda e: (-e["score"], e["time"]))[:200]
    try:
        with open(LEADERBOARD_FILE, "w") as f:
            json.dump(board, f)
    except Exception:
        # If the server does not allow writing files, keep the score for this session only.
        st.session_state.setdefault("local_board", []).append(entry)


# ---------- session state ----------
def init_state():
    defaults = {
        "stage": "home",        # home -> quiz -> result
        "quiz": [],             # the questions chosen for this game
        "idx": 0,               # index of the current question
        "score": 0,
        "streak": 0,
        "best_streak": 0,
        "lifelines": dict(LIFELINES_AT_START),
        "records": [],          # one record per answered question
        "answered": False,      # has the current question been answered?
        "last": None,           # record of the last answered question
        "q_start": 0.0,         # time when the current question was shown
        "game_start": 0.0,
        "player": "Player",
        "mode": "Mixed",
        "saved": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ----------------------------------------------------------------------
# 2. Game logic
# ----------------------------------------------------------------------
def start_game(name, level, count, topics):
    s = st.session_state
    pool = [q for q in QUESTIONS if q["topic"] in topics and (level == "Mixed" or q["level"] == level)]
    chosen = random.sample(pool, min(count, len(pool)))   # random questions, random order

    quiz = []
    for q in chosen:
        item = dict(q)                                    # copy so the bank is not changed
        item["shown"] = list(q["options"])
        if q["type"] in ("MCQ", "Scenario", "Problem Solving"):
            random.shuffle(item["shown"])                 # shuffle the options
        if q["type"] == "Match the Following":
            rights = [pair[1] for pair in q["pairs"]]
            random.shuffle(rights)
            item["shown"] = rights                        # shuffled right-hand column
        item["removed"] = []                              # options removed by 50-50
        item["used_hint"] = False
        item["used_fifty"] = False
        quiz.append(item)

    s.quiz = quiz
    s.idx = 0
    s.score = 0
    s.streak = 0
    s.best_streak = 0
    s.lifelines = dict(LIFELINES_AT_START)
    s.records = []
    s.answered = False
    s.last = None
    s.q_start = time.time()
    s.game_start = time.time()
    s.player = name.strip() or "Player"
    s.mode = level
    s.saved = False
    s.stage = "quiz"


def finish_question(q, user=None, timed_out=False):
    """Check the answer, work out the points and store a record."""
    s = st.session_state
    limit = time_limit(q)
    taken = min(time.time() - s.q_start, limit)
    points = 0
    detail = ""

    if timed_out:
        status = "timeout"
    elif is_correct(q, user):
        status = "correct"
    else:
        status = "wrong"

    if status == "correct":
        base = BASE_POINTS[q["level"]]
        parts = [f"base {base}"]
        if q["used_hint"] or q["used_fifty"]:
            base = base // 2                              # lifeline penalty: half the points
            parts = [f"base {base} (halved because a lifeline was used)"]
        time_bonus = int(5 * (limit - taken) / limit)     # up to 5 points for answering fast
        s.streak += 1
        streak_bonus = 5 if s.streak >= 3 else 0          # 3 correct in a row
        points = base + time_bonus + streak_bonus
        parts.append(f"time bonus {time_bonus}")
        if streak_bonus:
            parts.append(f"streak bonus {streak_bonus}")
        detail = ", ".join(parts)
        s.best_streak = max(s.best_streak, s.streak)
    else:
        s.streak = 0

    s.score += points
    record = {
        "id": q["id"], "topic": q["topic"], "type": q["type"], "level": q["level"],
        "question": q["question"], "your": user_answer_text(q, user),
        "correct": correct_answer_text(q), "status": status, "points": points,
        "detail": detail, "explanation": q["explanation"], "time": round(taken, 1),
    }
    s.records.append(record)
    s.last = record
    s.answered = True


def go_to_next():
    s = st.session_state
    s.idx += 1
    s.answered = False
    s.last = None
    if s.idx >= len(s.quiz):
        s.stage = "result"
    else:
        s.q_start = time.time()


# ---------- lifeline callbacks ----------
def use_hint():
    s = st.session_state
    q = s.quiz[s.idx]
    if s.lifelines["hint"] > 0 and not q["used_hint"]:
        s.lifelines["hint"] -= 1
        q["used_hint"] = True


def use_fifty():
    s = st.session_state
    q = s.quiz[s.idx]
    if s.lifelines["fifty"] > 0 and not q["used_fifty"]:
        wrong = [o for o in q["shown"] if o != q["answer"]]
        q["removed"] = random.sample(wrong, 2)            # remove two wrong options
        q["used_fifty"] = True
        s.lifelines["fifty"] -= 1


def use_skip():
    s = st.session_state
    q = s.quiz[s.idx]
    if s.lifelines["skip"] > 0:
        s.lifelines["skip"] -= 1
        s.streak = 0
        s.records.append({
            "id": q["id"], "topic": q["topic"], "type": q["type"], "level": q["level"],
            "question": q["question"], "your": "(skipped)", "correct": correct_answer_text(q),
            "status": "skipped", "points": 0, "detail": "", "explanation": q["explanation"], "time": 0,
        })
        go_to_next()


# ----------------------------------------------------------------------
# 3. Screens
# ----------------------------------------------------------------------
def tree_svg():
    """A small decorative search tree for the banner (the same idea as the report cover)."""
    levels = [
        [(150, 18)],
        [(86, 54), (214, 54)],
        [(54, 92), (118, 92), (182, 92), (246, 92)],
        [(38, 130), (70, 130), (102, 130), (134, 130), (166, 130), (198, 130), (230, 130), (262, 130)],
    ]
    skip = {(3, 2), (3, 5)}                               # leave two leaves out so it looks natural
    lines, dots = [], []
    for li, level in enumerate(levels):
        for i, (x, y) in enumerate(level):
            if (li, i) in skip:
                continue
            if li > 0:
                px, py = levels[li - 1][i // 2]
                lines.append(f'<line x1="{px}" y1="{py}" x2="{x}" y2="{y}"/>')
            accent = (li == 0) or (li == 3 and i in (0, 4))
            cls = "accent" if accent else ""
            r = 7 - li
            dots.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="{r}"/>')
    return f'<svg class="hero-tree" viewBox="0 0 300 150">{"".join(lines)}{"".join(dots)}</svg>'


def show_hero(compact):
    pills = ""
    if not compact:
        pills = (f'<div class="hero-pills"><span>{len(QUESTIONS)} questions</span>'
                 f'<span>{len(TOPICS)} topics</span><span>7 formats</span></div>')
    cls = "hero compact" if compact else "hero"
    st.markdown(f'<div class="{cls}">{tree_svg()}<div class="hero-title">AI Quiz Arena</div>{pills}</div>',
                unsafe_allow_html=True)


def title(text):
    st.markdown(f'<div class="section-title">{esc(text)}</div>', unsafe_allow_html=True)


def show_home():
    s = st.session_state
    with st.container(border=True, key="card_new"):
        title("Start a new game")
        name = st.text_input("Your name", value=s.player if s.player != "Player" else "",
                             placeholder="Type your name")
        level = st.radio("Difficulty", ["Easy", "Medium", "Hard", "Mixed"], index=3, horizontal=True)
        with st.expander("Choose topics (all are selected)"):
            topics = st.multiselect("Topics", TOPICS, default=TOPICS, label_visibility="collapsed")

        pool = [q for q in QUESTIONS if q["topic"] in topics and (level == "Mixed" or q["level"] == level)]
        if len(pool) == 0:
            st.warning("No questions match these choices. Select more topics or change the difficulty.")
            count = 0
        else:
            count = st.number_input("Number of questions", min_value=1, max_value=len(pool),
                                    value=min(10, len(pool)), step=1)
            st.caption(f"{len(pool)} questions are available for your choices.")

        if st.button("Start quiz", type="primary", disabled=(len(pool) == 0)):
            start_game(name, level, int(count), topics)
            st.rerun()

    with st.expander("How to play and how scoring works"):
        st.markdown(
            f"""
- Questions come in 7 formats: MCQ, True/False, Assertion-Reason, Fill in the Blank,
  Match the Following, Scenario and Problem Solving.
- Each question has a countdown timer. If time runs out, the question counts as wrong.
- Correct answer: **{BASE_POINTS['Easy']} / {BASE_POINTS['Medium']} / {BASE_POINTS['Hard']}** points for Easy / Medium / Hard.
- **Time bonus:** up to +5 points for answering quickly.
- **Streak bonus:** +5 points each time you have 3 or more correct answers in a row.
- **Lifelines:** Hint (3), 50-50 (2) and Skip (1) for the whole game.
  Using Hint or 50-50 on a question halves the base points for that question.
- You get instant feedback and an explanation after every answer.
"""
        )


@st.fragment(run_every=1)
def timer_box():
    """Live countdown. It re-runs every second without reloading the whole page."""
    s = st.session_state
    q = s.quiz[s.idx]
    limit = time_limit(q)
    left = seconds_left(q)
    pct = max(0.0, min(100.0, 100 * left / limit))
    secs = max(0, int(left) + (1 if left > 0 else 0))
    low = " low" if left <= limit * 0.25 else ""
    st.markdown(
        f'<div class="timer{low}"><div class="timer-top"><span>Time left</span><b>{secs} s</b></div>'
        f'<div class="bar"><div class="fill" style="width:{pct:.1f}%"></div></div></div>',
        unsafe_allow_html=True)
    if left <= 0:
        st.rerun()   # full re-run so the app can mark the question as timed out


def question_card(q):
    diagram = f'<pre class="diagram">{html.escape(q["diagram"])}</pre>' if q["diagram"] else ""
    body = esc(q["question"]).replace("<br><br>", "<br><br>")
    st.markdown(
        f'<div class="qcard"><div class="chips-row">'
        f'<span class="tag">{esc(q["topic"])}</span>'
        f'<span class="tag type">{esc(q["type"])}</span>'
        f'<span class="tag lvl-{q["level"]}">{q["level"]}</span>'
        f'<span class="tag pts">{BASE_POINTS[q["level"]]} pts</span></div>'
        f'<div class="qtext">{body}</div>{diagram}</div>',
        unsafe_allow_html=True)


def feedback_card(r):
    if r["status"] == "correct":
        head, sub, cls = f"Correct!  +{r['points']} points", r["detail"], "ok"
    elif r["status"] == "timeout":
        head, sub, cls = "Time is up.", "This question counts as wrong.", "bad"
    else:
        head, sub, cls = "Incorrect.", "", "bad"
    sub_html = f'<div class="fb-sub">{esc(sub)}</div>' if sub else ""
    yours = ""
    if r["status"] != "correct":
        yours = f'<div class="ans-box"><div class="ans-label">Your answer</div>{esc(r["your"])}</div>'
    st.markdown(
        f'<div class="fb {cls}"><div class="fb-head">{esc(head)}</div>{sub_html}</div>'
        f'<div class="ans-grid">{yours}'
        f'<div class="ans-box good"><div class="ans-label">Correct answer</div>{esc(r["correct"])}</div></div>'
        f'<div class="why"><div class="ans-label">Why</div>{esc(r["explanation"])}</div>',
        unsafe_allow_html=True)


def show_quiz():
    s = st.session_state
    if not s.quiz:
        s.stage = "home"
        st.rerun()

    q = s.quiz[s.idx]
    total = len(s.quiz)

    # If the time ran out while the question was still open, mark it as timed out.
    if not s.answered and seconds_left(q) <= 0:
        finish_question(q, timed_out=True)

    done = s.idx + (1 if s.answered else 0)
    st.markdown(
        f'<div class="progress"><div class="progress-top"><span>Question {s.idx + 1} of {total}</span>'
        f'<span>{s.mode}</span></div><div class="bar"><div class="fill" style="width:{100 * done / total:.1f}%"></div></div></div>'
        f'<div class="stats"><div class="stat"><span>Score</span><b>{s.score}</b></div>'
        f'<div class="stat"><span>Streak</span><b>{s.streak}</b></div>'
        f'<div class="stat"><span>Lifelines</span><b>{sum(s.lifelines.values())}</b></div></div>',
        unsafe_allow_html=True)

    question_card(q)

    # ----- after answering: show feedback -----
    if s.answered:
        feedback_card(s.last)
        label = "See results" if s.idx + 1 >= total else "Next question"
        st.button(label, type="primary", on_click=go_to_next)
        return

    # ----- before answering: timer, input, lifelines -----
    timer_box()

    t = q["type"]
    user = None
    ready = False

    if t in CHOICE_TYPES:
        options = [o for o in q["shown"] if o not in q["removed"]]
        user = st.radio("Choose one answer:", options, index=None, label_visibility="collapsed",
                        key=f"ans_{s.idx}_{len(q['removed'])}")
        ready = user is not None
    elif t == "Fill in the Blank":
        user = st.text_input("Type your answer:", placeholder="Type your answer here", key=f"fill_{s.idx}")
        ready = bool(user.strip())
    elif t == "Match the Following":
        user = []
        for i, pair in enumerate(q["pairs"]):
            user.append(st.selectbox(pair[0], q["shown"], index=None, placeholder="Choose the match...",
                                     key=f"match_{s.idx}_{i}"))
        ready = all(u is not None for u in user)

    if q["used_hint"]:
        st.markdown(f'<div class="hint"><b>Hint</b> {esc(q["hint"])}</div>', unsafe_allow_html=True)

    b1, b2, b3, b4 = st.columns([1.3, 1, 1, 1])
    submit = b1.button("Submit", type="primary", key=f"submit_{s.idx}")
    b2.button(f"Hint ({s.lifelines['hint']})", on_click=use_hint,
              disabled=(s.lifelines["hint"] == 0 or q["used_hint"]))
    can_fifty = (t in CHOICE_TYPES and len(q["shown"]) >= 4 and s.lifelines["fifty"] > 0 and not q["used_fifty"])
    b3.button(f"50-50 ({s.lifelines['fifty']})", on_click=use_fifty, disabled=not can_fifty)
    b4.button(f"Skip ({s.lifelines['skip']})", on_click=use_skip, disabled=(s.lifelines["skip"] == 0))

    if submit:
        if ready:
            finish_question(q, user=user)
            st.rerun()
        else:
            st.warning("Please answer the question before submitting.")


def show_result():
    s = st.session_state
    total = len(s.quiz)
    correct = sum(1 for r in s.records if r["status"] == "correct")
    accuracy = round(100 * correct / total) if total else 0
    elapsed = int(time.time() - s.game_start)

    if not s.saved:
        save_to_leaderboard({
            "name": s.player, "score": s.score, "correct": correct, "total": total,
            "accuracy": accuracy, "level": s.mode, "time": elapsed,
            "date": datetime.now().strftime("%d %b %Y %H:%M"),
        })
        s.saved = True

    if accuracy >= 90:
        rank_title = "AI Master"
    elif accuracy >= 75:
        rank_title = "AI Expert"
    elif accuracy >= 50:
        rank_title = "AI Learner"
    else:
        rank_title = "Keep practising"

    st.markdown(
        f'<div class="result"><div class="ring" style="--p:{accuracy}"><div class="ring-in">'
        f'<b>{accuracy}%</b><span>accuracy</span></div></div>'
        f'<div class="result-text"><div class="small">Quiz complete</div>'
        f'<div class="rank-title">{esc(rank_title)}</div><div class="who">{esc(s.player)}</div></div></div>'
        f'<div class="stats four"><div class="stat"><span>Final score</span><b>{s.score}</b></div>'
        f'<div class="stat"><span>Correct</span><b>{correct} / {total}</b></div>'
        f'<div class="stat"><span>Time</span><b>{elapsed // 60}m {elapsed % 60}s</b></div>'
        f'<div class="stat"><span>Best streak</span><b>{s.best_streak}</b></div></div>',
        unsafe_allow_html=True)

    df = pd.DataFrame(s.records)
    df["correct_flag"] = (df["status"] == "correct") * 1
    title("Result by topic")
    by_topic = df.groupby("topic")["correct_flag"].agg(["sum", "count"]).reset_index()
    by_topic["Accuracy (%)"] = (100 * by_topic["sum"] / by_topic["count"]).round(0)
    by_topic = by_topic.rename(columns={"topic": "Topic", "sum": "Correct", "count": "Asked"})
    st.dataframe(
        by_topic, hide_index=True,
        column_config={"Accuracy (%)": st.column_config.ProgressColumn(
            "Accuracy (%)", min_value=0, max_value=100, format="%d%%")},
    )

    title("Review your answers")
    for n, r in enumerate(s.records, start=1):
        mark = {"correct": "Correct", "wrong": "Wrong", "timeout": "Timed out", "skipped": "Skipped"}[r["status"]]
        with st.expander(f"Q{n}. {mark}  -  {r['topic']}  ({r['points']} pts)"):
            st.markdown(safe(r["question"]))
            st.markdown("**Your answer:**")
            st.markdown(safe(r["your"]))
            st.markdown("**Correct answer:**")
            st.markdown(safe(r["correct"]))
            st.info(safe(r["explanation"]))

    result_csv = df.drop(columns=["correct_flag"]).to_csv(index=False).encode("utf-8")
    d1, d2 = st.columns(2)
    d1.download_button("Download my result (CSV)", result_csv, "my_quiz_result.csv", "text/csv")
    if d2.button("Play again", type="primary"):
        s.stage = "home"
        st.rerun()

    title("Top 5 on the leaderboard")
    show_board(limit=5)


def show_board(limit=20):
    board = load_leaderboard()[:limit]
    if not board:
        st.write("No scores yet. Be the first to play.")
        return
    rows = []
    for rank, e in enumerate(board, start=1):
        rows.append({
            "Rank": rank, "Name": e["name"], "Score": e["score"],
            "Correct": f"{e['correct']}/{e['total']}", "Accuracy": f"{e['accuracy']}%",
            "Level": e["level"], "Time (s)": e["time"], "Date": e["date"],
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True)


def show_leaderboard():
    title("Leaderboard")
    st.caption("Ranked by score (a faster time breaks a tie). Scores are stored on the server while the app is running.")
    top = load_leaderboard()[:3]
    if top:
        medals = ["1st", "2nd", "3rd"]
        cards = "".join(
            f'<div class="pod pod{i + 1}"><div class="pod-rank">{medals[i]}</div>'
            f'<div class="pod-name">{esc(e["name"])}</div><div class="pod-score">{e["score"]}</div>'
            f'<div class="pod-sub">{e["correct"]}/{e["total"]} correct</div></div>'
            for i, e in enumerate(top))
        st.markdown(f'<div class="podium">{cards}</div>', unsafe_allow_html=True)
    show_board(limit=20)


def bank_dataframe():
    rows = []
    for q in QUESTIONS:
        if q["type"] == "Match the Following":
            options = " | ".join(f"{a} -> {b}" for a, b in q["pairs"])
        else:
            options = " | ".join(q["options"])
        rows.append({
            "ID": q["id"], "Topic": q["topic"], "Type": q["type"], "Level": q["level"],
            "Question": q["question"].replace("\n\n", " "), "Options / Pairs": options,
            "Correct answer": correct_answer_text(q).replace("\n", " "),
            "Explanation": q["explanation"],
            "Real-world": "Yes" if q["real_world"] else "", "Search problem": "Yes" if q["search"] else "",
        })
    return pd.DataFrame(rows)


def show_question_bank():
    title("Question bank (teacher view)")
    code = st.text_input("Enter the teacher passcode", type="password", key="teacher_code")
    if not code:
        st.info("This page shows every question with its correct answer.")
        return
    if code != teacher_passcode():
        st.error("Wrong passcode.")
        return

    df = bank_dataframe()
    f1, f2, f3 = st.columns(3)
    topic = f1.selectbox("Topic", ["All"] + TOPICS)
    qtype = f2.selectbox("Type", ["All"] + sorted(df["Type"].unique()))
    level = f3.selectbox("Level", ["All", "Easy", "Medium", "Hard"])
    text = st.text_input("Search in questions")

    if topic != "All":
        df = df[df["Topic"] == topic]
    if qtype != "All":
        df = df[df["Type"] == qtype]
    if level != "All":
        df = df[df["Level"] == level]
    if text:
        df = df[df["Question"].str.contains(text, case=False)]

    st.caption(f"Showing {len(df)} of {len(QUESTIONS)} questions")
    st.dataframe(df, hide_index=True)
    st.download_button("Download question bank (CSV)", df.to_csv(index=False).encode("utf-8"),
                       "question_bank.csv", "text/csv")


def show_about():
    title("About this game")
    st.markdown(
        """
<div class="about">
<p><b>Tool used:</b> Python with the Streamlit library. Streamlit turns a Python script into a web app,
so the quiz can be opened with a link and no installation.</p>
<p><b>Files:</b> <code>app.py</code> (screens and game logic), <code>questions.py</code> (the question bank),
<code>style.css</code> (the design), <code>requirements.txt</code> (libraries needed).</p>
<p><b>Features:</b> random questions, three difficulty levels, a countdown timer, instant feedback with explanations,
lifelines (hint, 50-50, skip), progress bar, live score and streak, topic-wise result table,
answer review, leaderboard, downloadable result and a teacher question-bank page.</p>
</div>
""",
        unsafe_allow_html=True)
    df = pd.DataFrame(QUESTIONS)
    st.markdown(
        f'<div class="stats four"><div class="stat"><span>Total questions</span><b>{len(df)}</b></div>'
        f'<div class="stat"><span>Topics covered</span><b>{df["topic"].nunique()}</b></div>'
        f'<div class="stat"><span>Real-world</span><b>{int(df["real_world"].sum())}</b></div>'
        f'<div class="stat"><span>Search / state-space</span><b>{int(df["search"].sum())}</b></div></div>',
        unsafe_allow_html=True)
    title("Questions by format")
    st.bar_chart(df["type"].value_counts(), color="#6CC3BB")


# ----------------------------------------------------------------------
# 4. Main part
# ----------------------------------------------------------------------
init_state()
load_css()
show_hero(compact=(st.session_state.stage == "quiz"))

tab_play, tab_board, tab_bank, tab_about = st.tabs(["Play", "Leaderboard", "Question Bank", "About"])

with tab_play:
    if st.session_state.stage == "home":
        show_home()
    elif st.session_state.stage == "quiz":
        show_quiz()
    else:
        show_result()
with tab_board:
    show_leaderboard()
with tab_bank:
    show_question_bank()
with tab_about:
    show_about()

st.markdown('<div class="footer">Developed by Aaron Anthony  |  Built with Python and Streamlit</div>',
            unsafe_allow_html=True)
