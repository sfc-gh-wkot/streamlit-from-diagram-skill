# CSS Patterns

Complete CSS patterns for navigation, panels, cards, and theming.

## Contents

- [Icon Navigation CSS](#icon-navigation-css)
- [Tiles Panel CSS](#tiles-panel-css)
- [Insight Card CSS](#insight-card-css)
- [Stat Card CSS](#stat-card-css)
- [Custom Theme Variables](#custom-theme-variables)
- [Dark Mode CSS](#dark-mode-css)
- [Hide Streamlit Branding](#hide-streamlit-branding)

---

## Icon Navigation CSS

Complete CSS for left icon navigation and header:

```python
st.markdown("""
<style>
/* Icon Navigation Header (top-left corner) */
.icon-nav-header {
    position: fixed;
    top: 0;
    left: 0;
    width: 48px;
    height: 56px;
    background: #ffffff;
    border-bottom: 1px solid #e5e5e5;
    border-right: 1px solid #e5e5e5;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
}

.icon-nav-header .nav-logo {
    width: 28px;
    height: 28px;
    border: 2px solid #1a1a1a;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
}

/* Left Icon Navigation */
.icon-nav {
    position: fixed;
    left: 0;
    top: 56px;
    bottom: 0;
    width: 48px;
    background: #ffffff;
    border-right: 1px solid #e5e5e5;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 16px;
    gap: 8px;
    z-index: 999998;
}

.icon-nav-item {
    width: 32px;
    height: 32px;
    border: 2px solid #d0d0d0;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    background: transparent;
    font-size: 14px;
    transition: all 0.2s ease;
}

.icon-nav-item.active {
    border-color: #2196f3;
    background: #e3f2fd;
}

.icon-nav-item:hover {
    border-color: #2196f3;
    transform: scale(1.05);
}

/* Adjust sidebar position for icon-nav */
[data-testid="stSidebar"] {
    top: 56px !important;
    left: 48px !important;
    height: calc(100vh - 56px) !important;
}
</style>
""", unsafe_allow_html=True)
```

---

## Tiles Panel CSS

```python
st.markdown("""
<style>
/* Right Tiles Panel */
.tiles-panel {
    position: fixed;
    right: 0;
    top: 56px;
    bottom: 0;
    width: 40px;
    background: #f5f5f5;
    border-left: 1px solid #e0e0e0;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding-top: 8px;
    z-index: 100;
}

.tiles-collapse {
    cursor: pointer;
    font-size: 16px;
    color: #666;
    margin-bottom: 4px;
    padding: 4px;
}

.tiles-collapse:hover {
    color: #2196f3;
}

.tiles-tab-label {
    writing-mode: vertical-rl;
    text-orientation: mixed;
    font-size: 12px;
    color: #666;
    font-weight: 500;
    padding: 8px 0;
    cursor: pointer;
}

.tiles-icons {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 20px;
}

.tiles-icon {
    width: 24px;
    height: 24px;
    background: #e0e0e0;
    border-radius: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s ease;
}

.tiles-icon:hover {
    background: #2196f3;
    color: white;
}

/* Adjust main content for panels */
.block-container {
    padding-right: 50px !important;
    max-width: 100% !important;
}
</style>
""", unsafe_allow_html=True)
```

---

## Insight Card CSS

```python
st.markdown("""
<style>
.insight-card {
    display: flex;
    gap: 12px;
    padding: 12px;
    background: #f8f9fa;
    border-radius: 8px;
    margin-bottom: 8px;
    border: 1px solid #e5e5e5;
}

.insight-card .card-icon {
    width: 40px;
    height: 40px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}

.insight-card .card-content {
    flex: 1;
    min-width: 0;
}

.insight-card .card-title {
    font-weight: 600;
    font-size: 14px;
    color: #1a1a1a;
    margin-bottom: 4px;
}

.insight-card .card-detail {
    font-size: 12px;
    color: #666;
    margin-bottom: 4px;
}

.insight-card .card-action {
    font-size: 11px;
    font-weight: 500;
}

.insight-card .card-action.positive {
    color: #4CAF50;
}

.insight-card .card-action.warning {
    color: #FF9800;
}
</style>
""", unsafe_allow_html=True)
```

---

## Stat Card CSS

```python
st.markdown("""
<style>
.stat-card {
    background: #f8f9fa;
    border: 1px solid #e5e5e5;
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 12px;
    text-align: center;
}

.stat-card .stat-label {
    font-size: 10px;
    font-weight: 600;
    color: #666;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
}

.stat-card .stat-value {
    font-size: 24px;
    font-weight: 700;
    color: #1a1a1a;
    margin-bottom: 4px;
}

.stat-card .stat-delta {
    font-size: 12px;
    font-weight: 500;
}

.stat-card .stat-delta.positive {
    color: #4CAF50;
}

.stat-card .stat-delta.warning {
    color: #FF9800;
}

.stat-card .stat-delta.negative {
    color: #E53935;
}
</style>
""", unsafe_allow_html=True)
```

---

## Custom Theme Variables

```python
st.markdown("""
<style>
:root {
    --primary: #4A90D9;
    --secondary: #E57373;
    --success: #81C784;
    --warning: #FFB74D;
    --text: #1a1a1a;
    --background: #f8f9fa;
    --border: #e5e5e5;
}

/* Custom card styling */
.custom-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 16px;
    margin-bottom: 16px;
}

.custom-card:hover {
    border-color: var(--primary);
    box-shadow: 0 2px 8px rgba(74, 144, 217, 0.15);
}
</style>
""", unsafe_allow_html=True)
```

---

## Dark Mode CSS

```python
def get_dark_mode_css():
    return """
    <style>
    /* Dark mode overrides */
    [data-testid="stAppViewContainer"] {
        background: #1a1a2e !important;
    }
    
    [data-testid="stSidebar"] {
        background: #16213e !important;
    }
    
    .icon-nav-header, .icon-nav {
        background: #16213e !important;
        border-color: #2a2a4a !important;
    }
    
    .icon-nav-header .nav-logo {
        border-color: #ffffff !important;
        color: #ffffff !important;
    }
    
    .icon-nav-item {
        border-color: #4a4a6a !important;
        color: #a0a0c0 !important;
    }
    
    .icon-nav-item.active {
        border-color: #4A90D9 !important;
        background: rgba(74, 144, 217, 0.2) !important;
    }
    
    .tiles-panel {
        background: #16213e !important;
        border-color: #2a2a4a !important;
    }
    
    .tiles-tab-label {
        color: #a0a0c0 !important;
    }
    
    .tiles-icon {
        background: #2a2a4a !important;
        color: #a0a0c0 !important;
    }
    
    .insight-card, .stat-card, .custom-card {
        background: #16213e !important;
        border-color: #2a2a4a !important;
    }
    
    .card-title, .stat-value {
        color: #ffffff !important;
    }
    
    .card-detail, .stat-label {
        color: #a0a0c0 !important;
    }
    </style>
    """

# Usage
if st.session_state.get("dark_mode"):
    st.markdown(get_dark_mode_css(), unsafe_allow_html=True)
```

---

## Hide Streamlit Branding

```python
st.markdown("""
<style>
/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
```

---

## Safe Fonts (CSP Compatible)

External fonts are blocked by CSP in SiS. Use system fonts only:

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```
