# AI Quiz Arena

Interactive quiz game for DSC401-6 Artificial Intelligence (Units I and II).
Built with Python and Streamlit by Aaron Anthony.

## Files

| File | Purpose |
|---|---|
| `app.py` | The game: screens, scoring, timer, lifelines, leaderboard, teacher page |
| `style.css` | The design: pastel teal and coral theme, tabs, answer cards |
| `questions.py` | The question bank (all questions, answers, hints and explanations) |
| `requirements.txt` | Libraries needed (streamlit, pandas) |
| `.streamlit/config.toml` | App colours (optional) |

## Run on your computer

```
pip install -r requirements.txt
streamlit run app.py
```

The game opens in your browser (usually http://localhost:8501).

## Put it online (Streamlit Community Cloud, free)

1. Create a free account on https://github.com and click **New repository**.
   Name it `ai-quiz-game` and choose **Public**.
2. Click **uploading an existing file** and drag in `app.py`, `questions.py`,
   `style.css`, `requirements.txt` and the `.streamlit` folder. Click **Commit changes**.
   (If you cannot see the `.streamlit` folder, skip it. It only changes the base colours.)
3. Go to https://share.streamlit.io and sign in with GitHub.
4. Click **Create app**, choose your repository, branch `main`, and main file `app.py`.
5. Click **Deploy**. After 2 to 3 minutes you get a link such as
   `https://your-name-ai-quiz.streamlit.app`. Share that link with your teacher.

## Teacher page

Open the **Question Bank** tab at the top. The default passcode is `teacher123`.
To change it on Streamlit Cloud: open the app, click **Settings, Secrets**, and add
`TEACHER_PASSCODE = "your-new-code"`.

## Notes

- The leaderboard is saved in `leaderboard.json` on the server. It keeps scores while the app
  is running and can reset when Streamlit Cloud restarts the app.
- To add or change questions, edit `questions.py` only. The app and the teacher page update by themselves.
