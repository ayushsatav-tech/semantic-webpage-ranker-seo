
def analyze_seo(page_data):
    title = page_data["title"]
    description = page_data["meta_description"]
    headings = page_data["headings"]
    word_count = page_data["word_count"]

    score = 0
    suggestions = []

    # Check title
    if title:
        if 30 <= len(title) <= 60:
            score += 20
        else:
            suggestions.append(
                "Keep the page title between 30 and 60 characters."
            )
    else:
        suggestions.append("Add a title to your webpage.")

    # Check meta description
    if description:
        if 120 <= len(description) <= 160:
            score += 20
        else:
            suggestions.append(
                "Keep the meta description between 120 and 160 characters."
            )
    else:
        suggestions.append("Add a meta description.")

    # Check H1 heading
    if len(headings["H1"]) == 1:
        score += 20
    elif len(headings["H1"]) == 0:
        suggestions.append("Add one main H1 heading.")
    else:
        suggestions.append("Use only one main H1 heading.")

    # Check H2 headings
    if len(headings["H2"]) >= 1:
        score += 20
    else:
        suggestions.append("Add relevant H2 subheadings.")

    # Check content length
    if word_count >= 300:
        score += 20
    else:
        suggestions.append(
            "Consider adding more useful and relevant webpage content."
        )

    return {
        "seo_score": score,
        "suggestions": suggestions
    }
