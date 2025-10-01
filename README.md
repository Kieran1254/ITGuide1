# IT Tutorials (Streamlit)

A clean, simple Streamlit site for uploading and browsing internal IT tutorials.

## Quick start

```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a **public GitHub repo**.
2. In Streamlit, set the app entry point to `app/app.py`.
3. (Optional) Add secrets for any future integrations.

## Structure

```
app/
  app.py              # Streamlit UI
  categories.py       # Category list
  utils.py            # Load/save helpers, slugging, search
  data/tutorials.json # Index of tutorials
  tutorials/*.md      # Tutorial contents (Markdown)
```

## Notes

- File writes occur in the working directory (supported on Streamlit Community Cloud).
- If you need auth, add `stauth` or protect behind your SSO proxy.
- To add icons/images, drop them in `app/assets/` and embed in Markdown.
