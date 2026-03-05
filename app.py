"""
Iris Phenotype Vision Generator - Streamlit App
index.html を Streamlit 上で表示するメインアプリケーション
"""
import base64
import json
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
    .block-container { padding-top: 0rem !important; }
    header[data-testid="stHeader"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


def build_image_map():
    """static/assets 以下の全 WebP をbase64エンコードし、JS用の辞書を返す"""
    assets_dir = Path(__file__).parent / "static" / "assets"
    assets_b64 = {}
    if assets_dir.exists():
        for img_path in sorted(assets_dir.rglob("*.webp")):
            try:
                b64_data = base64.b64encode(img_path.read_bytes()).decode("utf-8")
                assets_b64[img_path.stem] = f"data:image/webp;base64,{b64_data}"
            except Exception as e:
                st.warning(f"Failed to encode {img_path.name}: {e}")
    return assets_b64


def load_html():
    """index.html を読み込み、base64画像マップを注入して返す"""
    html_path = Path(__file__).parent / "index.html"
    if not html_path.exists():
        st.error(f"index.html が見つかりません: {html_path}")
        return None
    html_content = html_path.read_text(encoding="utf-8")
    # 画像マップを注入（index.html 内の '__BASE64_ASSETS__' プレースホルダーを置換）
    html_content = html_content.replace("'__BASE64_ASSETS__'", json.dumps(build_image_map()))
    return html_content


def main():
    html_content = load_html()
    if html_content is None:
        return
    st.components.v1.html(html_content, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
