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


def load_html_with_static_paths():
    """index.html を読み込み、静的ファイルパスを Streamlit 用に変換"""
    html_path = Path(__file__).parent / "index.html"
    if not html_path.exists():
        st.error(f"index.html が見つかりません: {html_path}")
        return None

    html_content = html_path.read_text(encoding="utf-8")
    return html_content


def main():
    html_content = load_html_with_static_paths()
    if html_content is None:
        return

    # HTMLコンポーネントで埋め込み（高さを十分に確保）
    st.components.v1.html(html_content, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
