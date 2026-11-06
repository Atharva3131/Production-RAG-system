def build_context(chunks: list[dict]) -> str:

    if not chunks:
        return "No relevant documentation was retrieved."

    context_parts = []

    for chunk in chunks:

        context_parts.append(
            f"""
[SOURCE_ID: {chunk['chunk_id']}]
[DOCUMENT: {chunk['source']}]
[TITLE: {chunk['title']}]
[URL: {chunk['url']}]

CONTENT:
{chunk['content']}
"""
        )

    return "\n\n".join(context_parts)