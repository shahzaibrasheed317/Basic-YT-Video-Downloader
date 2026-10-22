import os
import tempfile
from pathlib import Path

import streamlit as st
import yt_dlp

st.set_page_config(
    page_title="YTFetch",
    page_icon="▶",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@500;600;700;800&display=swap');

    :root {
        --background: #f8fafc;
        --panel: #ffffff;
        --teal: #0d9488;
        --purple: #7c3aed;
        --magenta: #db2777;
        --copper: #ea580c;
        --text: #0f172a;
        --muted: #64748b;
        --border: #e2e8f0;
    }

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        color: var(--text);
        background: 
            radial-gradient(ellipse at 85% 0%, rgba(124, 58, 237, 0.08), transparent 34%),
            radial-gradient(ellipse at 0% 18%, rgba(13, 148, 136, 0.08), transparent 32%),
            linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stToolbar"], #MainMenu, footer, .stDeployButton {
        visibility: hidden;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3 {
        font-family: 'Manrope', sans-serif !important;
        color: var(--text) !important;
    }

    p, label, [data-testid="stCaptionContainer"] {
        color: var(--muted);
    }

    .top-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0 0 2rem;
    }

    .app-mark {
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        color: #fff;
        font-size: 22px;
        font-weight: 800;
        background: linear-gradient(135deg, var(--teal), var(--purple) 58%, var(--magenta));
        box-shadow: 0 8px 24px rgba(124, 58, 237, 0.25);
    }

    .app-name {
        font-family: 'Manrope', sans-serif;
        font-size: 1.25rem;
        font-weight: 800;
        color: var(--text);
        letter-spacing: -.4px;
    }

    .page-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(2rem, 4vw, 3.15rem);
        font-weight: 800;
        letter-spacing: -1.5px;
        line-height: 1.12;
        color: var(--text);
        margin: .1rem 0 1.5rem;
    }

    .page-title span {
        background: linear-gradient(90deg, var(--teal), #7c3aed, var(--copper));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
    }

    .panel-heading {
        font-family: 'Manrope', sans-serif;
        font-size: 1.08rem;
        font-weight: 800;
        color: var(--text);
        margin-bottom: .35rem;
    }

    .helper {
        font-size: .88rem;
        line-height: 1.55;
        color: var(--muted);
        margin-bottom: .8rem;
    }

    .rule {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(13, 148, 136, 0.3), rgba(219, 39, 119, 0.3), transparent);
        margin: 1.2rem 0;
    }

    .stTextInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background: #ffffff !important;
        color: var(--text) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        min-height: 46px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .stTextInput input::placeholder {
        color: #94a3b8 !important;
    }

    .stTextInput input:focus,
    .stSelectbox div[data-baseweb="select"] > div:focus-within {
        border-color: var(--purple) !important;
        box-shadow: 0 0 0 1px var(--purple) !important;
    }

    .stButton > button,
    .stDownloadButton > button {
        width: 100%;
        border: 0;
        border-radius: 12px;
        min-height: 47px;
        color: #fff;
        font-weight: 800;
        background: linear-gradient(100deg, #7c3aed, #db2777);
        box-shadow: 0 8px 22px rgba(124, 58, 237, 0.25);
        transition: filter .15s ease, transform .15s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        filter: brightness(1.12);
        transform: translateY(-1px);
        color: #fff;
        border: 0;
    }

    div[data-testid="stAlert"] {
        border-radius: 12px;
        border: 1px solid var(--border);
    }

    .preview-placeholder {
        min-height: 300px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 1.25rem;
        border-radius: 16px;
        background: 
            radial-gradient(circle at 50% 35%, rgba(124, 58, 237, 0.04), transparent 48%),
            linear-gradient(145deg, #ffffff, #f8fafc);
        border: 1px dashed #cbd5e1;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    }

    .placeholder-icon {
        font-size: 3rem;
        margin-bottom: .6rem;
        color: var(--teal);
        opacity: 0.8;
    }

    .placeholder-title {
        color: var(--text);
        font-weight: 800;
        font-size: 1.08rem;
    }

    .placeholder-copy {
        color: var(--muted);
        font-size: .87rem;
        margin-top: .35rem;
    }

    .safety-note {
        font-size: .8rem;
        line-height: 1.5;
        color: #94a3b8;
        margin-top: 1.1rem;
    }

    @media (max-width: 800px) {
        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }

        .page-title {
            letter-spacing: -.8px;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="top-row">
        <div class="app-mark">▶</div>
        <div class="app-name">YTFetch</div>
    </div>
    <div class="page-title">Video <span>Downloader</span></div>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([1.12, 0.88], gap="large")

quality_options = {
    "Best available quality": "best",
    "Up to 1080p": "1080",
    "Up to 720p": "720",
    "Up to 480p": "480",
    "Audio only (MP3)": "mp3",
}

with left:
    st.markdown('<div class="panel-heading">Video link</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="helper">Enter the URL of a video you are allowed to download.</div>',
        unsafe_allow_html=True,
    )

    url = st.text_input(
        "Video URL",
        placeholder="Paste video URL here…",
        label_visibility="collapsed",
        key="video_url",
    )
    selected_label = st.selectbox("Format and quality", list(quality_options.keys()))
    fetch_clicked = st.button("Fetch video details", use_container_width=True)

    if fetch_clicked:
        if not url.strip():
            st.warning("Paste a video URL first.")
        else:
            try:
                with st.spinner("Fetching video details…"):
                    options = {
                        "quiet": True,
                        "no_warnings": True,
                        "noplaylist": True,
                        "skip_download": True,
                    }
                    with yt_dlp.YoutubeDL(options) as ydl:
                        details = ydl.extract_info(url.strip(), download=False)

                    st.session_state["clipfetch_info"] = {
                        "title": details.get("title") or "Untitled video",
                        "uploader": details.get("uploader") or details.get("channel") or "Unknown creator",
                        "duration": details.get("duration"),
                        "thumbnail": details.get("thumbnail"),
                    }
                    st.session_state["clipfetch_url"] = url.strip()
                st.success("Details loaded. Check the preview, then prepare your file.")
            except Exception as exc:
                st.error("Couldn't fetch this video. Check the link and try again.")
                with st.expander("Technical details"):
                    st.code(str(exc))

    info = st.session_state.get("clipfetch_info")
    current_url_matches = info and st.session_state.get("clipfetch_url") == url.strip()

    if current_url_matches:
        st.markdown('<div class="rule"></div>', unsafe_allow_html=True)
        st.markdown("**Selected format:** " + selected_label)

        if st.button("Prepare download", use_container_width=True, type="primary"):
            try:
                with st.spinner("Preparing your file… this may take a while."):
                    with tempfile.TemporaryDirectory(prefix="clipfetch_") as temp_dir:
                        output_template = os.path.join(temp_dir, "%(title).150s.%(ext)s")
                        choice = quality_options[selected_label]
                        download_options = {
                            "quiet": True,
                            "no_warnings": True,
                            "noplaylist": True,
                            "outtmpl": output_template,
                            "restrictfilenames": True,
                        }

                        if choice == "mp3":
                            download_options.update({
                                "format": "bestaudio/best",
                                "postprocessors": [{
                                    "key": "FFmpegExtractAudio",
                                    "preferredcodec": "mp3",
                                    "preferredquality": "192",
                                }],
                            })
                        else:
                            if choice == "best":
                                download_options["format"] = "bestvideo*+bestaudio/best"
                            else:
                                download_options["format"] = (
                                    f"bestvideo[height<={choice}]+bestaudio/"
                                    f"best[height<={choice}]/best"
                                )
                            download_options["merge_output_format"] = "mp4"

                        with yt_dlp.YoutubeDL(download_options) as ydl:
                            ydl.download([st.session_state["clipfetch_url"]])

                        output_files = [path for path in Path(temp_dir).iterdir() if path.is_file()]
                        if not output_files:
                            raise RuntimeError("No output file was created.")

                        output_file = max(output_files, key=lambda path: path.stat().st_size)
                        file_bytes = output_file.read_bytes()
                        mime_type = "audio/mpeg" if choice == "mp3" else "video/mp4"
                        download_name = output_file.name

                st.download_button(
                    "Download file",
                    data=file_bytes,
                    file_name=download_name,
                    mime=mime_type,
                    use_container_width=True,
                    key="clipfetch_download_file",
                )
                st.info("Click Download file to save it to your device.")
            except Exception as exc:
                st.error("The file couldn't be prepared. The source may not support this format.")
                with st.expander("Technical details"):
                    st.code(str(exc))

    st.markdown(
        '<div class="safety-note">Download only content you own or are authorized to save. This app does not bypass DRM, paywalls, or access restrictions.</div>',
        unsafe_allow_html=True,
    )

with right:
    info = st.session_state.get("clipfetch_info")
    if info and st.session_state.get("clipfetch_url") == url.strip():
        if info.get("thumbnail"):
            st.image(info["thumbnail"], use_container_width=True)

        st.markdown(
            '<div class="panel-heading" style="margin-top:.9rem">'
            + str(info["title"])
            + "</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="helper">' + str(info["uploader"]) + "</div>",
            unsafe_allow_html=True,
        )

        duration = info.get("duration")
        if duration:
            minutes, seconds = divmod(int(duration), 60)
            hours, minutes = divmod(minutes, 60)
            duration_label = (
                f"{hours}:{minutes:02d}:{seconds:02d}"
                if hours
                else f"{minutes}:{seconds:02d}"
            )
            st.caption(f"Duration: {duration_label}")
    else:
        st.markdown(
            """
            <div class="preview-placeholder">
                <div class="placeholder-icon">▶</div>
                <div class="placeholder-title">Video preview</div>
                <div class="placeholder-copy">Fetch details to see the thumbnail and video information here.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )