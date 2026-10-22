import os
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="ClipFetch",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── Theme ──────────────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

dark = st.session_state.theme == "dark"

# ── Design tokens ──────────────────────────────────────────────────────────────
if dark:
    BG          = "#0c0c0e"
    SURFACE     = "#161618"
    SURFACE2    = "#1e1e21"
    BORDER      = "#2c2c30"
    BORDER2     = "#3a3a40"
    T1          = "#f2f2f3"
    T2          = "#98989f"
    T3          = "#5a5a62"
    ACCENT      = "#5e6ad2"
    ACCENT_H    = "#4d58c0"
    ACCENT_T    = "#ffffff"
    GREEN       = "#22c55e"
    GREEN_H     = "#16a34a"
    INPUT_BG    = "#131315"
    SHADOW      = "0 0 0 1px rgba(255,255,255,0.05), 0 8px 30px rgba(0,0,0,0.45)"
    SHADOW_S    = "0 1px 4px rgba(0,0,0,0.35)"
    RING        = "rgba(94,106,210,0.25)"
else:
    BG          = "#f4f4f6"
    SURFACE     = "#ffffff"
    SURFACE2    = "#f8f8fa"
    BORDER      = "#e2e2e8"
    BORDER2     = "#cbcbd4"
    T1          = "#101014"
    T2          = "#525260"
    T3          = "#9898a8"
    ACCENT      = "#4f46e5"
    ACCENT_H    = "#4338ca"
    ACCENT_T    = "#ffffff"
    GREEN       = "#16a34a"
    GREEN_H     = "#15803d"
    INPUT_BG    = "#ffffff"
    SHADOW      = "0 0 0 1px rgba(0,0,0,0.06), 0 6px 24px rgba(0,0,0,0.05)"
    SHADOW_S    = "0 1px 3px rgba(0,0,0,0.07)"
    RING        = "rgba(79,70,229,0.18)"

MOON_ICON = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
</svg>"""

SUN_ICON = """<svg width="16" height="16" viewBox="0 0 24 24" fill="none"
  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
  <circle cx="12" cy="12" r="5"/>
  <line x1="12" y1="1" x2="12" y2="3"/>
  <line x1="12" y1="21" x2="12" y2="23"/>
  <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
  <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
  <line x1="1" y1="12" x2="3" y2="12"/>
  <line x1="21" y1="12" x2="23" y2="12"/>
  <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
  <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
</svg>"""

theme_icon_svg = SUN_ICON if dark else MOON_ICON

# ── Stylesheet ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [class*="css"] {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
}}

.stApp {{
    background: {BG};
    color: {T1};
}}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
#MainMenu, footer, .stDeployButton {{
    display: none !important;
}}

.block-container {{
    max-width: 680px !important;
    padding: 0 1.5rem 5rem !important;
}}

/* ── Scrollbar ── */
::-webkit-scrollbar {{ width: 5px; }}
::-webkit-scrollbar-track {{ background: transparent; }}
::-webkit-scrollbar-thumb {{ background: {BORDER2}; border-radius: 99px; }}

/* ── Navbar ── */
.cf-nav {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.6rem 0 1.4rem;
    border-bottom: 1px solid {BORDER};
    margin-bottom: 2.5rem;
}}

.cf-brand {{
    display: flex;
    align-items: center;
    gap: 9px;
}}

.cf-logo {{
    width: 30px;
    height: 30px;
    border-radius: 7px;
    background: {T1};
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}}

.cf-wordmark {{
    font-size: 1.05rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    color: {T1};
    line-height: 1;
}}

/* ── Theme icon button ── */
.theme-btn-wrap .stButton > button {{
    width: 34px !important;
    height: 34px !important;
    min-height: 34px !important;
    padding: 0 !important;
    border-radius: 8px !important;
    background: {SURFACE} !important;
    border: 1px solid {BORDER} !important;
    color: {T2} !important;
    box-shadow: {SHADOW_S} !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    line-height: 1 !important;
}}

.theme-btn-wrap .stButton > button:hover {{
    background: {SURFACE2} !important;
    border-color: {BORDER2} !important;
    color: {T1} !important;
}}

.theme-btn-wrap .stButton > button > div {{
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 0 !important;
    width: 100% !important;
    height: 100% !important;
}}

.theme-btn-wrap .stButton > button p {{
    display: none !important;
}}

/* ── Section label ── */
.section-label {{
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: {T3};
    margin-bottom: 0.9rem;
}}

/* ── Inputs ── */
.stTextInput label,
.stSelectbox label {{
    display: none !important;
}}

.stTextInput > div > div,
.stTextInput input {{
    background: {INPUT_BG} !important;
    color: {T1} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 9px !important;
    min-height: 46px !important;
    font-size: 0.925rem !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: {SHADOW_S} !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}

.stTextInput input:focus,
.stTextInput > div > div:focus-within {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {RING}, {SHADOW_S} !important;
    outline: none !important;
}}

.stTextInput input::placeholder {{
    color: {T3} !important;
    font-size: 0.9rem !important;
}}

.stSelectbox > div [data-baseweb="select"] > div {{
    background: {INPUT_BG} !important;
    color: {T1} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 9px !important;
    min-height: 46px !important;
    font-size: 0.925rem !important;
    box-shadow: {SHADOW_S} !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}}

.stSelectbox > div [data-baseweb="select"] > div:focus-within {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px {RING} !important;
}}

/* ── Field label text ── */
.field-label {{
    font-size: 0.825rem;
    font-weight: 600;
    color: {T2};
    margin-bottom: 0.45rem;
    letter-spacing: -0.01em;
    display: block;
}}

/* ── Buttons ── */
.stButton > button {{
    width: 100%;
    border-radius: 9px;
    min-height: 46px;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: -0.01em;
    border: 1px solid {BORDER};
    background: {SURFACE};
    color: {T1};
    box-shadow: {SHADOW_S};
    transition: all 0.15s ease;
    font-family: 'Inter', sans-serif;
}}

.stButton > button:hover {{
    background: {SURFACE2};
    border-color: {BORDER2};
}}

.stButton > button[kind="primary"] {{
    background: {ACCENT} !important;
    color: {ACCENT_T} !important;
    border-color: {ACCENT} !important;
    box-shadow: 0 2px 10px {RING}, {SHADOW_S} !important;
}}

.stButton > button[kind="primary"]:hover {{
    background: {ACCENT_H} !important;
    border-color: {ACCENT_H} !important;
}}

.stDownloadButton > button {{
    width: 100%;
    background: {GREEN} !important;
    color: #ffffff !important;
    border: 1px solid {GREEN} !important;
    border-radius: 9px !important;
    min-height: 46px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    font-family: 'Inter', sans-serif !important;
    box-shadow: 0 2px 10px rgba(34,197,94,0.22) !important;
    transition: background 0.15s !important;
}}

.stDownloadButton > button:hover {{
    background: {GREEN_H} !important;
    border-color: {GREEN_H} !important;
}}

/* ── Alerts ── */
div[data-testid="stAlert"] {{
    border-radius: 9px;
    border: 1px solid {BORDER};
    background: {SURFACE};
    font-size: 0.875rem;
    font-family: 'Inter', sans-serif;
}}

/* ── Spinner ── */
div[data-testid="stSpinner"] {{
    font-size: 0.875rem;
    color: {T2};
}}

/* ── Preview card ── */
.preview-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 14px;
    overflow: hidden;
    box-shadow: {SHADOW};
    margin-bottom: 1.25rem;
}}

.thumb-wrap {{
    position: relative;
    width: 100%;
    line-height: 0;
    background: #000;
}}

.thumb-img {{
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
    display: block;
}}

.dur-badge {{
    position: absolute;
    bottom: 10px;
    right: 10px;
    background: rgba(0,0,0,0.78);
    color: #ffffff;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    padding: 2px 8px;
    border-radius: 5px;
    backdrop-filter: blur(8px);
}}

.card-body {{
    padding: 1.25rem 1.4rem 1.4rem;
}}

.video-title {{
    font-size: 1.08rem;
    font-weight: 600;
    color: {T1};
    line-height: 1.4;
    letter-spacing: -0.02em;
    margin-bottom: 1.1rem;
}}

.meta-bar {{
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    border: 1px solid {BORDER};
    border-radius: 9px;
    overflow: hidden;
}}

.meta-item {{
    padding: 0.6rem 0.85rem;
    border-right: 1px solid {BORDER};
}}

.meta-item:last-child {{
    border-right: none;
}}

.meta-item-label {{
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    color: {T3};
    margin-bottom: 3px;
}}

.meta-item-value {{
    font-size: 0.845rem;
    font-weight: 500;
    color: {T1};
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}}

/* ── Ready banner ── */
.ready-banner {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-left: 3px solid {GREEN};
    border-radius: 9px;
    padding: 0.85rem 1.1rem;
    margin-bottom: 0.85rem;
}}

.ready-name {{
    font-size: 0.875rem;
    font-weight: 600;
    color: {T1};
    margin-bottom: 1px;
}}

.ready-sub {{
    font-size: 0.775rem;
    color: {T2};
}}

/* ── Empty state ── */
.empty-state {{
    border: 1.5px dashed {BORDER2};
    border-radius: 14px;
    background: {SURFACE};
    padding: 4rem 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
}}

.empty-icon-wrap {{
    width: 52px;
    height: 52px;
    border-radius: 13px;
    border: 1px solid {BORDER};
    background: {SURFACE2};
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.2rem;
    color: {T3};
}}

.empty-title {{
    font-size: 1rem;
    font-weight: 600;
    color: {T1};
    letter-spacing: -0.02em;
    margin-bottom: 0.4rem;
}}

.empty-sub {{
    font-size: 0.845rem;
    color: {T2};
    line-height: 1.55;
    max-width: 320px;
    margin: 0 auto;
}}

/* ── Divider ── */
.hr {{
    height: 1px;
    background: {BORDER};
    margin: 1.5rem 0;
}}

/* ── Footer ── */
.cf-footer {{
    font-size: 0.76rem;
    color: {T3};
    text-align: center;
    margin-top: 3rem;
    line-height: 1.5;
    padding-top: 1.5rem;
    border-top: 1px solid {BORDER};
}}
</style>
""", unsafe_allow_html=True)

# ── Helpers ────────────────────────────────────────────────────────────────────
quality_options = {
    "Best available":   "best",
    "1080p — Full HD":  "1080",
    "720p — HD":        "720",
    "480p — Standard":  "480",
    "Audio only (MP3)": "mp3",
}

def fmt_dur(secs):
    if not secs:
        return "—"
    m, s = divmod(int(secs), 60)
    h, m = divmod(m, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

# ── Navbar ─────────────────────────────────────────────────────────────────────
nav_l, nav_r = st.columns([0.85, 0.15])

with nav_l:
    st.markdown(f"""
    <div class="cf-nav">
        <div class="cf-brand">
            <div class="cf-logo">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                     stroke="{BG}" stroke-width="2.6"
                     stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="5 3 19 12 5 21 5 3"/>
                </svg>
            </div>
            <span class="cf-wordmark">ClipFetch</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with nav_r:
    st.markdown('<div class="theme-btn-wrap">', unsafe_allow_html=True)
    icon_key = ":material/light_mode:" if dark else ":material/dark_mode:"
    st.button("\u200B", icon=icon_key, on_click=toggle_theme, key="btn_theme")
    st.markdown('</div>', unsafe_allow_html=True)

# ── URL input ──────────────────────────────────────────────────────────────────
st.markdown('<span class="field-label">Video URL</span>', unsafe_allow_html=True)
url = st.text_input("url", placeholder="https://www.youtube.com/watch?v=...",
                    key="url_input", label_visibility="collapsed")

# ── Format + Fetch row ─────────────────────────────────────────────────────────
st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
col_fmt, col_btn = st.columns([0.62, 0.38], gap="medium")

with col_fmt:
    st.markdown('<span class="field-label">Quality</span>', unsafe_allow_html=True)
    selected_label = st.selectbox("fmt", list(quality_options.keys()),
                                  key="fmt_select", label_visibility="collapsed")
with col_btn:
    st.markdown('<span class="field-label">&nbsp;</span>', unsafe_allow_html=True)
    fetch_btn = st.button("Fetch details", type="primary",
                          use_container_width=True, key="btn_fetch")

st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

# ── Fetch logic ────────────────────────────────────────────────────────────────
if fetch_btn:
    clean = url.strip()
    if not clean:
        st.warning("Enter a video URL to continue.")
    else:
        try:
            with st.spinner("Fetching video details..."):
                with yt_dlp.YoutubeDL({"quiet": True, "no_warnings": True,
                                        "noplaylist": True, "skip_download": True}) as ydl:
                    info = ydl.extract_info(clean, download=False)

            st.session_state["cf_meta"] = {
                "title":    info.get("title")    or "Untitled video",
                "uploader": info.get("uploader") or info.get("channel") or "Unknown",
                "duration": info.get("duration"),
                "thumb":    info.get("thumbnail"),
            }
            st.session_state["cf_url"]  = clean
            st.session_state["cf_file"] = None

        except Exception as exc:
            st.error("Could not retrieve details for this URL. Check the link and try again.")
            with st.expander("Error details"):
                st.code(str(exc))

# ── Preview + download ─────────────────────────────────────────────────────────
meta   = st.session_state.get("cf_meta")
url_ok = meta and st.session_state.get("cf_url") == url.strip()

if url_ok:
    dur   = fmt_dur(meta.get("duration"))
    thumb = meta.get("thumb", "")

    thumb_block = ""
    if thumb:
        thumb_block = f"""
        <div class="thumb-wrap">
            <img src="{thumb}" class="thumb-img" alt="thumbnail"/>
            <div class="dur-badge">{dur}</div>
        </div>"""

    st.markdown(f"""
    <div class="preview-card">
        {thumb_block}
        <div class="card-body">
            <div class="video-title">{meta["title"]}</div>
            <div class="meta-bar">
                <div class="meta-item">
                    <div class="meta-item-label">Channel</div>
                    <div class="meta-item-value">{meta["uploader"]}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-item-label">Duration</div>
                    <div class="meta-item-value">{dur}</div>
                </div>
                <div class="meta-item">
                    <div class="meta-item-label">Format</div>
                    <div class="meta-item-value">{selected_label}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    prepare_btn = st.button("Prepare download", type="primary",
                            use_container_width=True, key="btn_prepare")

    if prepare_btn:
        choice = quality_options[selected_label]
        try:
            with st.spinner("Processing file — this may take a moment..."):
                with tempfile.TemporaryDirectory(prefix="clipfetch_") as td:
                    tpl      = os.path.join(td, "%(title).150s.%(ext)s")
                    dl_opts  = {
                        "quiet": True, "no_warnings": True,
                        "noplaylist": True, "outtmpl": tpl,
                        "restrictfilenames": True,
                    }
                    if choice == "mp3":
                        dl_opts.update({
                            "format": "bestaudio/best",
                            "postprocessors": [{
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }],
                        })
                    else:
                        dl_opts["format"] = (
                            "bestvideo*+bestaudio/best"
                            if choice == "best"
                            else f"bestvideo[height<={choice}]+bestaudio/best[height<={choice}]/best"
                        )
                        dl_opts["merge_output_format"] = "mp4"

                    with yt_dlp.YoutubeDL(dl_opts) as ydl:
                        ydl.download([st.session_state["cf_url"]])

                    files = [p for p in Path(td).iterdir() if p.is_file()]
                    if not files:
                        raise RuntimeError("No output file produced.")

                    out     = max(files, key=lambda p: p.stat().st_size)
                    data    = out.read_bytes()
                    mime    = "audio/mpeg" if choice == "mp3" else "video/mp4"
                    size_mb = len(data) / (1024 * 1024)

                    st.session_state["cf_file"] = {
                        "name": out.name, "data": data,
                        "mime": mime, "size_mb": size_mb,
                    }
        except Exception as exc:
            st.error("Download preparation failed. The source may restrict this format.")
            with st.expander("Error details"):
                st.code(str(exc))

    pf = st.session_state.get("cf_file")
    if pf:
        st.markdown(f"""
        <div class="ready-banner">
            <div class="ready-name">{pf["name"]}</div>
            <div class="ready-sub">{pf["size_mb"]:.2f} MB &middot; {pf["mime"]}</div>
        </div>
        """, unsafe_allow_html=True)

        st.download_button(
            label=f"Download  {pf['name']}",
            data=pf["data"],
            file_name=pf["name"],
            mime=pf["mime"],
            use_container_width=True,
            key="btn_dl",
        )

else:
    st.markdown(f"""
    <div class="empty-state">
        <div class="empty-icon-wrap">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none"
                 stroke="currentColor" stroke-width="1.7"
                 stroke-linecap="round" stroke-linejoin="round">
                <rect x="2" y="2" width="20" height="20" rx="2.5"/>
                <line x1="7"  y1="2"  x2="7"  y2="22"/>
                <line x1="17" y1="2"  x2="17" y2="22"/>
                <line x1="2"  y1="12" x2="22" y2="12"/>
                <line x1="2"  y1="7"  x2="7"  y2="7"/>
                <line x1="17" y1="7"  x2="22" y2="7"/>
                <line x1="2"  y1="17" x2="7"  y2="17"/>
                <line x1="17" y1="17" x2="22" y2="17"/>
            </svg>
        </div>
        <div class="empty-title">No video loaded</div>
        <div class="empty-sub">Paste a supported URL above, choose a quality setting, and click Fetch details to begin.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="cf-footer">
    Use this application only for content you are authorized to download.
</div>
""", unsafe_allow_html=True)
