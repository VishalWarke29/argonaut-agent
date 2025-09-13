# -------------------------
# 📁 agent/arxiv_fetcher.py
# -------------------------
import arxiv

def fetch_arxiv_papers(query, max_results=3):
    client = arxiv.Client()
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)
    results = []
    for result in client.results(search):
        results.append({
            "title": result.title,
            "summary": result.summary,
            "url": result.entry_id,
            "pdf_url": result.pdf_url,
            "authors": [a.name for a in result.authors],
        })
    return results