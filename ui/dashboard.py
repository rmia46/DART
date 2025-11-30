import streamlit as st
from config import settings
from ui.components import map_widget

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title=settings.APP_TITLE,
    layout=settings.APP_LAYOUT
)

def main():
    # 2. Sidebar
    with st.sidebar:
        st.header("🎮 Controls")
        st.write("Status: **Initializing...**")

    # 3. Main Title
    st.title(f"🚦 {settings.APP_TITLE}")
    st.markdown("---")

    # 4. Load the Map Component
    map_widget.render()

if __name__ == "__main__":
    main()