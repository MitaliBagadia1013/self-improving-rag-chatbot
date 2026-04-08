# def build_context(results: list[dict]) -> str:
#     context_parts = []

#     for i, result in enumerate(results, 1):
#         meta = result["metadata"]
#         context_parts.append(
#             f"""[Chunk {i}]
# Source: {meta["source"]}
# Page: {meta["page"]}
# Chunk ID: {meta["chunk_id"]}
# Text: {meta["text"]}
# """
#         )

#     return "\n\n".join(context_parts)


# def build_prompt(query: str, results: list[dict]) -> str:
#     context = build_context(results)

#     return f"""
# You are a helpful research assistant.

# Answer the user's question only using the provided context.
# If the answer is not supported by the context, say:
# "I could not find enough evidence in the retrieved documents."

# When possible, cite sources like:
# [Source: filename, Page: X, Chunk: Y]

# User Question:
# {query}

# Retrieved Context:
# {context}

# Answer:
# """

def build_prompt(query: str, results: list[dict]) -> str:
    context_parts = []

    for i, result in enumerate(results, 1):
        meta = result["metadata"]
        context_parts.append(
            f"""Document {i}:
Source: {meta["source"]} (Page {meta["page"]})
Content: {meta["text"]}
"""
        )

    context = "\n\n".join(context_parts)

    return f"""
You are a helpful research assistant that answers questions based on provided research documents.

INSTRUCTIONS:
1. Read all the provided documents carefully
2. Answer the question using ONLY information from the documents
3. Provide a clear, comprehensive, and well-structured response
4. Cite sources naturally in your answer using the format [Source: filename, Page: X]
5. DO NOT mention "Chunk", "Document 1", "Document 2", etc. in your answer
6. Write your answer as if you're explaining to a colleague, not referencing document numbers
7. If the answer is not in the documents, say: "I could not find enough evidence in the retrieved documents."

User Question:
{query}

Available Documents:
{context}

Please provide a clear and comprehensive answer with proper source citations:
"""