"""
AniSage — Anime Recommender System
Streamlit application entry point.
"""

import streamlit as st
from pipeline.pipeline import AnimeRecommendationPipeline

# ── Page config (must be first Streamlit call) ─────────────────────────────
st.set_page_config(
    page_title="AniSage · Anime Recommender",
    page_icon="⛩️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown(
    """
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Inter:wght@300;400;500;600&display=swap');

/* ── Root palette ── */
:root {
    --bg-deep:       #0d0d14;
    --bg-card:       #13131f;
    --bg-card-hover: #1a1a2e;
    --border:        #2a2a45;
    --accent:        #9b59b6;
    --accent-glow:   rgba(155, 89, 182, 0.35);
    --accent-light:  #c39bd3;
    --gold:          #f0c040;
    --text-primary:  #e8e8f0;
    --text-muted:    #7a7a9a;
    --success:       #2ecc71;
    --danger:        #e74c3c;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-deep);
    color: var(--text-primary);
}

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; padding-bottom: 2rem; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-card);
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: var(--accent-light); }

/* ── Hero title ── */
.hero-title {
    font-family: 'Cinzel', serif;
    font-size: clamp(2.2rem, 5vw, 3.6rem);
    font-weight: 700;
    letter-spacing: 0.06em;
    background: linear-gradient(135deg, #c39bd3 0%, #9b59b6 50%, #f0c040 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.15;
    margin-bottom: 0.25rem;
}
.hero-tagline {
    font-size: 1rem;
    color: var(--text-muted);
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}

/* ── Search bar ── */
.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-size: 1.05rem !important;
    padding: 0.85rem 1.2rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px var(--accent-glow) !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #9b59b6, #7d3c98) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em;
    transition: transform 0.15s, box-shadow 0.15s !important;
    box-shadow: 0 4px 18px var(--accent-glow) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px var(--accent-glow) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Recommendation cards ── */
.rec-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
    position: relative;
    overflow: hidden;
}
.rec-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #9b59b6, #f0c040);
    border-radius: 16px 16px 0 0;
}
.rec-card:hover {
    border-color: var(--accent);
    box-shadow: 0 8px 30px var(--accent-glow);
    transform: translateY(-2px);
    background: var(--bg-card-hover);
}
.rec-number {
    font-family: 'Cinzel', serif;
    font-size: 0.7rem;
    color: var(--gold);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.rec-title {
    font-size: 1.25rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.6rem;
}
.rec-body {
    font-size: 0.95rem;
    color: var(--text-muted);
    line-height: 1.7;
}
.rec-body strong { color: var(--accent-light); font-weight: 500; }

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Source badge ── */
.source-badge {
    display: inline-block;
    background: rgba(155, 89, 182, 0.15);
    border: 1px solid rgba(155, 89, 182, 0.3);
    border-radius: 20px;
    padding: 0.2rem 0.75rem;
    font-size: 0.75rem;
    color: var(--accent-light);
    margin: 0.2rem 0.3rem 0.2rem 0;
}

/* ── Stats chips ── */
.stat-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.35rem 0.8rem;
    font-size: 0.82rem;
    color: var(--text-muted);
    margin: 0.25rem;
}
.stat-chip span { color: var(--text-primary); font-weight: 500; }

/* ── Example chips ── */
.example-chip {
    display: inline-block;
    background: rgba(155,89,182,0.08);
    border: 1px solid rgba(155,89,182,0.2);
    border-radius: 20px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    color: var(--accent-light);
    margin: 0.25rem;
    cursor: pointer;
    transition: background 0.15s, border-color 0.15s;
}
.example-chip:hover {
    background: rgba(155,89,182,0.2);
    border-color: var(--accent);
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-muted) !important;
    font-size: 0.85rem !important;
}
</style>
""",
    unsafe_allow_html=True,
)

# ── Pipeline initialisation (cached) ───────────────────────────────────────
@st.cache_resource(show_spinner="Loading AniSage engine…")
def _load_pipeline() -> AnimeRecommendationPipeline:
    return AnimeRecommendationPipeline()


# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⛩️ AniSage")
    st.markdown(
        "<p style='color:#7a7a9a;font-size:0.85rem;'>Your AI-powered anime curator</p>",
        unsafe_allow_html=True,
    )
    st.markdown("---")

    st.markdown("### 🎯 How to use")
    st.markdown(
        """
<div style='color:#7a7a9a;font-size:0.88rem;line-height:1.8'>
1. Describe the kind of anime you're in the mood for<br>
2. Be as specific as you like — genre, mood, setting, themes<br>
3. Hit <b style='color:#c39bd3'>Get Recommendations</b><br>
4. Explore your three curated picks
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### ⚙️ Settings")
    show_sources = st.toggle("Show retrieved sources", value=False)
    st.markdown("---")
    st.markdown(
        "<p style='color:#3a3a5a;font-size:0.75rem;text-align:center'>"
        "Powered by LLaMA 3.1 · ChromaDB · LangChain"
        "</p>",
        unsafe_allow_html=True,
    )

# ── Main layout ────────────────────────────────────────────────────────────
col_main, col_gap = st.columns([3, 1])

with col_main:
    # Hero
    st.markdown('<div class="hero-title">AniSage</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-tagline">Discover your next favourite anime with AI</div>',
        unsafe_allow_html=True,
    )

    # Example queries
    st.markdown(
        "<p style='color:#7a7a9a;font-size:0.85rem;margin-bottom:0.4rem'>Try asking for:</p>",
        unsafe_allow_html=True,
    )
    examples = [
        "dark psychological thriller",
        "wholesome slice-of-life with cooking",
        "mecha with deep world-building",
        "romance set in high school",
        "action with redemption arc",
    ]
    st.markdown(
        " ".join(f'<span class="example-chip">{e}</span>' for e in examples),
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Input row
    c_input, c_btn = st.columns([5, 1])
    with c_input:
        query = st.text_input(
            label="Preference",
            placeholder="e.g. dark psychological thriller with a morally grey protagonist…",
            label_visibility="collapsed",
        )
    with c_btn:
        search = st.button("Search", use_container_width=True)

    # ── Results ────────────────────────────────────────────────────────
    if search and query and query.strip():
        try:
            pipeline = _load_pipeline()
        except Exception as e:
            st.error(
                f"⚠️ Could not start the recommendation engine. "
                f"Make sure you have run the build pipeline and set your `.env`.\n\n`{e}`"
            )
            st.stop()

        with st.spinner("Curating your perfect picks…"):
            try:
                result = pipeline.recommend(query.strip())
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                st.stop()

        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            "<p style='color:#7a7a9a;font-size:0.85rem;margin-bottom:1rem'>"
            f"Results for: <b style='color:#c39bd3'>{query}</b>"
            "</p>",
            unsafe_allow_html=True,
        )

        # Render recommendation cards
        raw_answer = result.answer
        # Split on numbered list markers: "1.", "2.", "3."
        import re
        blocks = re.split(r"(?=\n?(?:\*\*)?[123]\.\s)", "\n" + raw_answer.strip())
        blocks = [b.strip() for b in blocks if b.strip()]

        ordinal = ["PICK ONE", "PICK TWO", "PICK THREE"]

        if len(blocks) >= 3:
            for i, block in enumerate(blocks[:3]):
                label = ordinal[i] if i < len(ordinal) else f"PICK {i+1}"
                # Remove leading "1. " etc.
                clean = re.sub(r"^\*?\*?[123]\.\s*\*?\*?", "", block).strip()
                # Extract title (first bold or first line)
                title_match = re.match(r"\*\*(.+?)\*\*", clean)
                if title_match:
                    title = title_match.group(1)
                    body = clean[title_match.end():].strip().lstrip("–—:-").strip()
                else:
                    lines = clean.split("\n", 1)
                    title = lines[0].strip()
                    body = lines[1].strip() if len(lines) > 1 else ""

                body_html = body.replace("**", "<strong>").replace("**", "</strong>")
                # crude bold fix — alternate open/close
                parts = body.split("**")
                body_html = ""
                for j, part in enumerate(parts):
                    body_html += f"<strong>{part}</strong>" if j % 2 == 1 else part

                st.markdown(
                    f"""
<div class="rec-card">
    <div class="rec-number">{label}</div>
    <div class="rec-title">{title}</div>
    <div class="rec-body">{body_html}</div>
</div>
""",
                    unsafe_allow_html=True,
                )
        else:
            # Fallback: render raw answer in a single card
            st.markdown(
                f'<div class="rec-card"><div class="rec-body">{raw_answer}</div></div>',
                unsafe_allow_html=True,
            )

        # Source documents
        if show_sources and result.source_documents:
            st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
            with st.expander(f"📚 Retrieved source documents ({len(result.source_documents)})"):
                for i, doc in enumerate(result.source_documents, 1):
                    st.markdown(
                        f"**[{i}]** `{doc.page_content[:300]}{'…' if len(doc.page_content) > 300 else ''}`"
                    )

    elif search and not query.strip():
        st.warning("Please enter your anime preferences before searching.")

    # Empty state
    if not query:
        st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            """
<div style='text-align:center;padding:3rem 0;color:#3a3a5a'>
    <div style='font-size:3rem;margin-bottom:1rem'>⛩️</div>
    <div style='font-size:1rem;color:#5a5a7a'>
        Describe what you're looking for and AniSage will find your next obsession.
    </div>
</div>
""",
            unsafe_allow_html=True,
        )
