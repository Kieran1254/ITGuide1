import streamlit as st
from pathlib import Path
from typing import List
import json
from categories import CATEGORIES
from utils import add_tutorial, list_by_category, get_markdown, search, load_tutorials, update_tutorial, TUTORIALS_DIR

st.set_page_config(page_title="IT Tutorials", page_icon="💼", layout="wide")

# ---- Sidebar ----
st.sidebar.title("IT Tutorials")
st.sidebar.markdown("A clean and simple portal for uploading and viewing internal IT guides.")

page = st.sidebar.radio("Navigate", ["Home", "Browse", "Upload", "Search", "About"])

# Reusable UI bits
def pill(text: str):
    st.markdown(f"<span style='padding:4px 10px; border:1px solid #e0e0e0; border-radius:999px; font-size:12px'>{text}</span>", unsafe_allow_html=True)

def tutorial_card(t: dict):
    with st.expander(f"📄 {t['title']} — *{t['category']}*"):
        st.caption(f"Slug: `{t['slug']}` • Tags: {', '.join(t.get('tags',[])) or '—'} • Difficulty: {t.get('difficulty') or '—'}")
        md = get_markdown(t["slug"])
        st.markdown(md)
        with st.popover("Quick actions"):
            new_title = st.text_input("Title", value=t["title"], key=f"title-{t['slug']}")
            new_category = st.selectbox("Category", CATEGORIES, index=CATEGORIES.index(t["category"]) if t["category"] in CATEGORIES else 0, key=f"cat-{t['slug']}")
            new_difficulty = st.selectbox("Difficulty", ["", "Beginner", "Intermediate", "Advanced"], index=["", "Beginner", "Intermediate", "Advanced"].index(t.get("difficulty","")), key=f"diff-{t['slug']}")
            new_tags = st.text_input("Tags (comma-separated)", value=", ".join(t.get("tags",[])), key=f"tags-{t['slug']}")
            new_md = st.text_area("Edit content (Markdown)", value=md, height=220, key=f"md-{t['slug']}")
            if st.button("Save changes", key=f"save-{t['slug']}"):
                ok, msg = update_tutorial(
                    t["slug"],
                    new_content_md=new_md,
                    title=new_title,
                    category=new_category,
                    difficulty=new_difficulty,
                    tags=[s.strip() for s in new_tags.split(",") if s.strip()],
                )
                if ok:
                    st.success("Saved.")
                else:
                    st.error(msg)

if page == "Home":
    st.title("💼 IT Tutorials")
    st.write("Upload, categorize, and browse internal IT procedures. Built with Streamlit.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tutorials", len(load_tutorials().get("tutorials", [])))
    with col2:
        cats = CATEGORIES
        st.metric("Categories", len(cats))
    with col3:
        st.metric("Storage", f"{len(list(Path(TUTORIALS_DIR).glob('*.md')))} files")
    st.divider()
    st.subheader("Quick Links")
    cols = st.columns(4)
    with cols[0]:
        if st.button("📚 Browse"):
            st.session_state["nav"] = "Browse"
    with cols[1]:
        if st.button("⬆️ Upload"):
            st.session_state["nav"] = "Upload"
    with cols[2]:
        if st.button("🔎 Search"):
            st.session_state["nav"] = "Search"
    with cols[3]:
        if st.button("ℹ️ About"):
            st.session_state["nav"] = "About"
    if "nav" in st.session_state:
        page = st.session_state.pop("nav")
        st.switch_page("app.py")

elif page == "Browse":
    st.title("Browse by Category")
    for cat in CATEGORIES:
        st.header(cat)
        items = list_by_category(cat)
        if not items:
            st.info("No tutorials yet.")
            continue
        for t in items:
            tutorial_card(t)

elif page == "Upload":
    st.title("Upload a new tutorial")
    with st.form("upload-form"):
        title = st.text_input("Title *")
        category = st.selectbox("Category *", CATEGORIES, index=0)
        difficulty = st.selectbox("Difficulty", ["", "Beginner", "Intermediate", "Advanced"])
        tags = st.text_input("Tags (comma-separated)")
        author = st.text_input("Author")
        source_choice = st.radio("How will you provide content?", ["Paste Markdown/Text", "Upload .md file"])
        content_md = ""
        uploaded_md = None
        if source_choice == "Paste Markdown/Text":
            content_md = st.text_area("Content (Markdown supported) *", height=240, placeholder="# Heading\nStep-by-step...\n- bullet 1\n- bullet 2")
        else:
            uploaded_md = st.file_uploader("Upload a Markdown file", type=["md"])
        submitted = st.form_submit_button("Save Tutorial")
        if submitted:
            if not title.strip():
                st.error("Please add a title.")
            else:
                try:
                    tags_list = [s.strip() for s in tags.split(",") if s.strip()]
                    if uploaded_md is not None:
                        content = uploaded_md.read().decode("utf-8", errors="ignore")
                    else:
                        content = content_md
                    if not content.strip():
                        st.error("Content cannot be empty.")
                    else:
                        ok, msg = add_tutorial(title, category, content, author=author, tags=tags_list, difficulty=difficulty)
                        if ok:
                            st.success("Tutorial added.")
                        else:
                            st.error(msg)
                except Exception as e:
                    st.error(f"Something went wrong while saving: {e}")

elif page == "Search":
    st.title("Search")
    q = st.text_input("Search titles, tags, or content...")
    if q:
        results = search(q)
        st.caption(f"{len(results)} result(s)")
        for t in results:
            tutorial_card(t)

elif page == "About":
    st.title("About this portal")
    st.markdown("""
This lightweight Streamlit app lets your 1st Line team upload and browse internal tutorials.
**Features**
- Categories aligned to your workflow
- Upload via paste or Markdown file
- Inline editing with quick actions
- Search by title, tags, or content
- Basic error handling and safe file writes

To add more categories, edit `categories.py`.
Data is stored in `app/data/tutorials.json` with the Markdown files in `app/tutorials/`.
""")
