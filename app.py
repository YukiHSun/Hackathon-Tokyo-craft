"""
Iris Phenotype Vision Generator - Streamlit App
index.html を Streamlit 上で表示するメインアプリケーション
"""
import streamlit as st
from pathlib import Path

# ページ設定（サイドバーを最小化し、フルワイド表示）
st.set_page_config(
    page_title="Iris Phenotype Vision Generator",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# カスタムCSS：StreamlitのデフォルトUIを非表示にしてHTMLゲームを前面に
st.markdown("""
<style>
    /* ヘッダー・パディングを最小化 */
    .block-container { padding-top: 0rem !important; }
    header[data-testid="stHeader"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def get_static_base_url():
    """リクエストからアプリのベースURLを取得"""
    try:
        ctx = getattr(st, "context", None)
        headers = getattr(ctx, "headers", None) if ctx else None
        if not headers:
            return ""
        host = (headers.get("host") or headers.get("Host") or "").strip()
        if not host:
            return ""
        proto = (headers.get("x-forwarded-proto") or headers.get("X-Forwarded-Proto") or "https").strip()
        if proto != "https" and "localhost" in host:
            proto = "http"
        return f"{proto}://{host}"
    except Exception:
        return ""


# 画像を GitHub Raw から配信（Streamlit Cloud の静的配信が iframe 内で読めないため）
GITHUB_RAW_BASE = "https://raw.githubusercontent.com/YukiHSun/Hackathon-Tokyo-craft/main"


def load_html_with_base_url():
    """index.html を読み込み、ベースURL・GitHub Raw URL を注入して返す"""
    html_path = Path(__file__).parent / "index.html"
    if not html_path.exists():
        st.error(f"index.html が見つかりません: {html_path}")
        return None
    html_content = html_path.read_text(encoding="utf-8")
    base_url = get_static_base_url()
    html_content = html_content.replace("__STREAMLIT_STATIC_BASE__", base_url)
    html_content = html_content.replace("__GITHUB_RAW_BASE__", GITHUB_RAW_BASE)
    return html_content


def main():
    html_content = load_html_with_base_url()
    if html_content is None:
        return
    st.components.v1.html(html_content, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
