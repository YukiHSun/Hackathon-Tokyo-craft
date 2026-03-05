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


def main():
    # static/index.html を iframe で表示。同一オリジンになるため相対パス assets/ で画像が読める
    base_url = get_static_base_url()
    iframe_src = f"{base_url}/app/static/index.html" if base_url else "/app/static/index.html"
    st.components.v1.iframe(iframe_src, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
