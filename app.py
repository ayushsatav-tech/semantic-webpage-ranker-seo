
import streamlit as st

from src.webpage_analyzer import analyze_webpage
from src.seo_analyzer import analyze_seo
from src.ranking import rank_webpages


st.set_page_config(
    page_title="AI Webpage Ranking & SEO Analyzer",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 AI-Powered Webpage Ranking & SEO Optimization")
st.write(
    "Analyze webpages, compare their SEO quality, "
    "and rank them using keyword and semantic similarity."
)

query = st.text_input(
    "Enter your search query",
    placeholder="Example: Best Python courses for beginners"
)

urls_text = st.text_area(
    "Enter webpage URLs (one URL per line)",
    placeholder="https://example.com\nhttps://www.python.org",
    height=150
)

if st.button("Analyze and Rank Webpages", type="primary"):

    urls = [
        url.strip()
        for url in urls_text.splitlines()
        if url.strip()
    ]

    if not query.strip():
        st.error("Please enter a search query.")

    elif not urls:
        st.error("Please enter at least one webpage URL.")

    else:
        pages = []
        seo_results = []

        progress = st.progress(0)

        for index, url in enumerate(urls):
            try:
                page = analyze_webpage(url)
                seo = analyze_seo(page)

                pages.append(page)
                seo_results.append({
                    "url": url,
                    "title": page["title"],
                    "seo_score": seo["seo_score"],
                    "suggestions": seo["suggestions"]
                })

            except Exception as error:
                st.warning(f"Could not analyze {url}: {error}")

            progress.progress((index + 1) / len(urls))

        if pages:
            st.subheader("🏆 Webpage Ranking")

            try:
                ranked_pages = rank_webpages(query, pages)

                for position, result in enumerate(ranked_pages, 1):
                    with st.container(border=True):
                        st.markdown(
                            f"### {position}. {result['title'] or 'Untitled page'}"
                        )
                        st.write(result["url"])
                        st.write(
                            f"**Hybrid Score:** {result['hybrid_score']}"
                        )
                        st.write(
                            f"BM25 Score: {result['bm25_score']} | "
                            f"Semantic Score: {result['semantic_score']}"
                        )

            except Exception as error:
                st.error(f"Ranking failed: {error}")

            st.subheader("📊 SEO Analysis")

            for result in seo_results:
                st.markdown(f"**{result['title'] or result['url']}**")
                st.write(f"SEO Score: {result['seo_score']}/100")

                if result["suggestions"]:
                    for suggestion in result["suggestions"]:
                        st.write(f"- {suggestion}")
                else:
                    st.success("All five basic SEO checks passed.")

                st.divider()

        else:
            st.error("No webpages could be analyzed.")
