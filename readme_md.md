# YTFetch ▶️

YTFetch is a sleek, modern web application built with Streamlit that allows you to easily fetch details and download videos or audio from various online platforms. Powered by the robust `yt-dlp` library, it offers a user-friendly interface with built-in Light and Dark themes.

## Features

* **Clean UI:** A modern, responsive, SaaS-like interface.

* **Theme Toggle:** Switch between beautiful Light and Dark modes with a single click.

* **Video Preview:** Instantly fetch and view the video thumbnail, title, channel name, and duration before downloading.

* **Multiple Formats & Qualities:**

  * Best available quality

  * Up to 1080p, 720p, or 480p (MP4)

  * Audio only (MP3 extraction)

* **Secure Downloading:** Processes downloads in temporary directories to keep your system clean.

## Prerequisites

Before running this application, ensure you have the following installed on your system:

1. **Python 3.8+**

2. **FFmpeg:** Required for merging video/audio streams and extracting MP3 audio.

   * **Windows:** Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or use `winget install ffmpeg`

   * **macOS:** `brew install ffmpeg`

   * **Linux:** `sudo apt install ffmpeg`

## Installation

1. **Clone the repository** (or download the source code):

   ```bash
   git clone https://github.com/yourusername/ytfetch.git
   cd ytfetch
   ```

2. **Create a virtual environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the required Python packages**:

   ```bash
   pip install streamlit yt-dlp
   ```

## Usage

1. Start the Streamlit application:

   ```bash
   streamlit run app.py
   ```

   *(Note: Replace `app.py` with the actual name of your Python file if it differs).*

2. Open your web browser to the local URL provided by Streamlit (usually `http://localhost:8501`).

3. Paste a supported video URL into the input field.

4. Select your desired format and quality.

5. Click **Fetch details** to preview the video.

6. Click **Prepare Download** and wait for the file to process.

7. Once ready, click the **Download File** button to save it to your device.

## Disclaimer

**Download only content you own or are authorized to save.** This application is provided for educational and personal use. It does not bypass DRM, paywalls, or access restrictions. The developer assumes no responsibility for how this tool is used.

## License

This project is open-source and available under the [MIT License](LICENSE).