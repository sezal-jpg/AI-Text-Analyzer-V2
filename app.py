import streamlit as st
from services.pii_service import scan_and_redact
from services.language_service import (
    analyze_sentiment,
    extract_key_phrases,
    recognize_entities,)
from services.generation_service import generate_text
from utils.text_stats import calculate_stats

st.set_page_config(
    page_title="TextShield AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",)


st.markdown(
    """
<style>

/* =====================================================
   GLOBAL
   ===================================================== */

.stApp {
    background: #0b0d12;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
    padding-bottom: 4rem;
}


/* =====================================================
   HEADER
   ===================================================== */

.brand {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-icon {
    font-size: 2.3rem;
}

.brand-title {
    font-size: 2.1rem;
    font-weight: 750;
    color: #ffffff;
    margin: 0;
    letter-spacing: -0.5px;
}

.brand-subtitle {
    color: #9ca3af;
    font-size: 0.95rem;
    margin-left: 55px;
    margin-top: -2px;
    margin-bottom: 30px;
}


/* =====================================================
   PRIVACY BANNER
   ===================================================== */

.privacy-card {
    background: linear-gradient(
        135deg,
        rgba(42, 20, 70, 0.88),
        rgba(20, 24, 38, 0.96)
    );

    border: 1px solid rgba(139, 92, 246, 0.45);
    border-radius: 16px;

    padding: 18px 22px;
    margin-bottom: 34px;
}

.privacy-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
}

.protected {
    color: #a78bfa;
    font-weight: 750;
}

.privacy-text {
    color: #aeb4c2;
    font-size: 0.88rem;
    margin-top: 7px;
}


/* =====================================================
   PRIVACY REPORT
   ===================================================== */

.privacy-report {
    background: #151821;
    border: 1px solid #292e3a;
    border-radius: 14px;
    padding: 18px;
}

.privacy-report-title {
    color: #ffffff;
    font-size: 0.95rem;
    font-weight: 700;
    margin-bottom: 12px;
}

.privacy-item {
    color: #aeb4c2;
    font-size: 0.84rem;
    margin: 6px 0;
}

.privacy-highlight {
    color: #a78bfa;
    font-weight: 700;
}


/* =====================================================
   SECTION HEADINGS
   ===================================================== */

.section-title {
    color: #ffffff;
    font-size: 1.35rem;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 8px;
}

.section-description {
    color: #9ca3af;
    font-size: 0.9rem;
    margin-bottom: 14px;
}


/* =====================================================
   TEXT INPUT
   ===================================================== */

textarea {
    background-color: #171a22 !important;
    color: #f3f4f6 !important;
    border-radius: 12px !important;
}


/* =====================================================
   ANALYZE BUTTON
   ===================================================== */

div.stButton > button {
    width: 100%;
    height: 3.1rem;

    border-radius: 11px;

    background: #151821;
    border: 1px solid #3a4050;

    color: #ffffff;

    font-size: 1rem;
    font-weight: 650;

    transition: all 0.2s ease;
}

div.stButton > button:hover {
    border-color: #8b5cf6;
    background: #1b1e29;
}


/* =====================================================
   METRIC CARDS
   ===================================================== */

.metric-card {
    background: #151821;
    border: 1px solid #292e3a;

    border-radius: 14px;

    padding: 18px 10px;

    text-align: center;
}

.metric-value {
    color: #ffffff;
    font-size: 1.7rem;
    font-weight: 750;
}

.metric-label {
    color: #8f96a5;
    font-size: 0.75rem;
    margin-top: 5px;
    letter-spacing: 0.3px;
}


/* =====================================================
   RESULT PANELS
   ===================================================== */

.panel-title {
    color: #ffffff;
    font-size: 1rem;
    font-weight: 700;
    margin-bottom: 12px;
}


/* =====================================================
   SENTIMENT
   ===================================================== */

.sentiment-main {
    font-size: 2rem;
    font-weight: 750;
    color: #ffffff;

    margin: 5px 0 15px 0;
}


/* =====================================================
   BADGES
   ===================================================== */

.badge {
    display: inline-block;

    background: #1c2030;

    border: 1px solid #353b4d;

    border-radius: 8px;

    padding: 7px 11px;

    margin: 4px 4px 4px 0;

    color: #d8dce6;

    font-size: 0.84rem;
}

.badge-category {
    color: #a78bfa;
}


/* =====================================================
   AI OUTPUT
   ===================================================== */

.ai-label {
    color: #a78bfa;
    font-size: 0.82rem;
    font-weight: 650;
    margin-bottom: 8px;
}

.ai-description {
    color: #8f96a5;
    font-size: 0.82rem;
    margin-bottom: 12px;
}


/* =====================================================
   FOOTER
   ===================================================== */

.footer {
    text-align: center;
    color: #626978;
    font-size: 0.75rem;

    margin-top: 50px;
    padding-top: 20px;

    border-top: 1px solid #1e222c;
}

</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="brand">
    <div class="brand-icon">🛡️</div>
    <div class="brand-title">TextShield AI</div>
</div>
""",
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="brand-subtitle">'
    'Privacy-Aware Intelligent Text Analysis'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="privacy-card">'
    '<div class="privacy-title">'
    '🔒 Privacy-First AI Pipeline '
    '<span class="protected">● PROTECTED</span>'
    '</div>'
    '<div class="privacy-text">'
    'Sensitive information is detected and redacted before '
    'downstream AI analysis.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-title">Analyze your text</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Enter text and let the AI pipeline analyze sentiment, '
    'important concepts, entities and generate a continuation.'
    '</div>',
    unsafe_allow_html=True,
)

text = st.text_area(
    "Text input",
    height=180,
    label_visibility="collapsed",
    placeholder=(
        "Example: I am excited about building AI applications "
        "with Microsoft Azure..."
    ),
)

analyze = st.button(
    "🔍  Analyze Text",
    use_container_width=True,
)

if analyze:

    if not text.strip():

        st.warning(
            "Please enter some text before starting the analysis."
        )

    else:

        try:

            with st.spinner(
                "🔒 Scanning text for sensitive information..."
            ):

                pii_result = scan_and_redact(text)

            safe_text = pii_result["redacted_text"]

            if pii_result["pii_detected"]:

                st.success(
                    "🔒 Protected — Sensitive information was "
                    "detected and redacted before AI analysis."
                )

            else:

                st.success(
                    "🔒 Protected — No sensitive information detected."
                )

            with st.container(border=True):

                st.markdown(
                    '<div class="privacy-report-title">'
                    '🛡️ Privacy Firewall Report'
                    '</div>',
                    unsafe_allow_html=True,
                )

                if pii_result["pii_detected"]:

                    categories = sorted(
                        set(
                            entity["category"]
                            for entity in pii_result["entities"]
                        )
                    )

                    category_text = ", ".join(categories)

                    st.markdown(
                        '<div class="privacy-item">'
                        '<span class="privacy-highlight">'
                        'Status:</span> Protected'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="privacy-item">'
                        '<span class="privacy-highlight">'
                        'Sensitive items secured:</span> '
                        f'{len(pii_result["entities"])}'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="privacy-item">'
                        '<span class="privacy-highlight">'
                        'Detection categories:</span> '
                        f'{category_text}'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    if pii_result.get("detection_sources"):

                        sources = ", ".join(
                            pii_result["detection_sources"]
                        )

                        st.markdown(
                            '<div class="privacy-item">'
                            '<span class="privacy-highlight">'
                            'Detection layers:</span> '
                            f'{sources}'
                            '</div>',
                            unsafe_allow_html=True,
                        )

                else:

                    st.markdown(
                        '<div class="privacy-item">'
                        '<span class="privacy-highlight">'
                        'Status:</span> No sensitive information detected'
                        '</div>',
                        unsafe_allow_html=True,
                    )

            with st.expander(
                "🔐 View sanitized text"
            ):

                st.code(
                    safe_text,
                    language="text",
                )

            stats = calculate_stats(safe_text)

            st.markdown(
                '<div class="section-title">'
                '📊 Text Overview'
                '</div>',
                unsafe_allow_html=True,
            )

            col1, col2, col3, col4 = st.columns(4)
            with col1:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">'
                    f'{stats["words"]}'
                    '</div>'
                    '<div class="metric-label">'
                    'WORDS'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )


            with col2:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">'
                    f'{stats["characters"]}'
                    '</div>'
                    '<div class="metric-label">'
                    'CHARACTERS'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )


            with col3:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">'
                    f'{stats["sentences"]}'
                    '</div>'
                    '<div class="metric-label">'
                    'SENTENCES'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )


            with col4:

                st.markdown(
                    '<div class="metric-card">'
                    '<div class="metric-value">'
                    f'{stats["reading_time"]} min'
                    '</div>'
                    '<div class="metric-label">'
                    'READING TIME'
                    '</div>'
                    '</div>',
                    unsafe_allow_html=True,
                )

            with st.spinner(
                "🧠 Running Azure AI analysis..."):

                sentiment = analyze_sentiment(
                    safe_text
                )

                key_phrases = extract_key_phrases(
                    safe_text
                )

                entities = recognize_entities(
                    safe_text
                )

            st.markdown(
                '<div class="section-title">'
                '🧠 Language Intelligence'
                '</div>',
                unsafe_allow_html=True,
            )


            left, right = st.columns(
                2,
                gap="large",
            )

            with left:

                with st.container(border=True):

                    st.markdown(
                        '<div class="panel-title">'
                        '😊 Sentiment Analysis'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.markdown(
                        '<div class="sentiment-main">'
                        f'{sentiment["sentiment"].upper()}'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    s1, s2, s3 = st.columns(3)


                    with s1:

                        st.metric(
                            "Positive",
                            f'{sentiment["positive"]:.1%}',
                        )


                    with s2:

                        st.metric(
                            "Neutral",
                            f'{sentiment["neutral"]:.1%}',
                        )


                    with s3:

                        st.metric(
                            "Negative",
                            f'{sentiment["negative"]:.1%}',
                        )

            with right:

                with st.container(border=True):

                    st.markdown(
                        '<div class="panel-title">'
                        '🔑 Key Phrases'
                        '</div>',
                        unsafe_allow_html=True,
                    )


                    if key_phrases:

                        phrase_html = ""

                        for phrase in key_phrases:

                            phrase_html += (
                                '<span class="badge">'
                                f'• {phrase}'
                                '</span>'
                            )

                        st.markdown(
                            phrase_html,
                            unsafe_allow_html=True,
                        )

                    else:

                        st.caption(
                            "No key phrases detected."
                        )

            st.markdown(
                '<div class="section-title">'
                '👤 Named Entities'
                '</div>',
                unsafe_allow_html=True,
            )


            if entities:

                with st.container(border=True):

                    entity_html = ""

                    for entity in entities:

                        entity_html += (
                            '<span class="badge">'
                            f'{entity["text"]} · '
                            '<span class="badge-category">'
                            f'{entity["category"]}'
                            '</span> · '
                            f'{entity["confidence"]:.0%}'
                            '</span>'
                        )


                    st.markdown(
                        entity_html,
                        unsafe_allow_html=True,
                    )

            else:

                with st.container(border=True):

                    st.caption(
                        "No named entities detected."
                    )

            st.markdown(
                '<div class="section-title">'
                '✨ AI Text Continuation'
                '</div>',
                unsafe_allow_html=True,
            )


            st.markdown(
                '<div class="ai-description">'
                'Generated from the privacy-sanitized text using '
                'the Qwen instruction-tuned language model.'
                '</div>',
                unsafe_allow_html=True,
            )

            with st.spinner(
                "✨ Generating continuation..."):
                continuation = generate_text(safe_text)

            if continuation:

                with st.container(border=True):
                    st.markdown(
                        '<div class="ai-label">'
                        '✨ GENERATED CONTINUATION'
                        '</div>',
                        unsafe_allow_html=True,
                    )

                    st.write(continuation)

            else:

                st.info(
                    "The model did not generate additional text."
                )

        except Exception as e:

            st.error(
                "An error occurred while processing the text."
            )

            st.exception(e)

st.markdown(
    '<div class="footer">'
    'TextShield AI · Privacy-Aware NLP Platform · '
    'Azure AI Language + Hugging Face'
    '</div>',
    unsafe_allow_html=True,
)