from conn import milvus_client, embed
import json

def results_to_context(search_res):
    if not search_res:
        return ""

    chunks = []
    for hits in search_res:
        for hit in hits:
            e = hit["entity"]
            chunk = (
                "[SECTION]: {section}\n"
                "[CONTENT]: {content}\n"
                "[LINK]: {link}\n"
                "[METADATA]: {metadata}"
            ).format(
                section=e.get("section", ""),
                content=e.get("content", ""),
                link=e.get("link", ""),
                metadata=json.dumps(e.get("metadata", {}), ensure_ascii=False)
            )
            chunks.append(chunk)

    return "\n\n".join(chunks)


def is_context_relevant(query, search_res, threshold=0.1):
    """
    Check if search results are actually relevant to the query.
    Returns True if at least one result has distance below threshold.
    """
    if not search_res or not search_res[0]:
        return False
    
    # Check best match distance
    best_distance = search_res[0][0]['distance']
    

        
    return best_distance > threshold

def vector_store(query: str):
    """
    Docstring for vector_store

    """
    search_res = milvus_client.search(
    collection_name="test01",
    data=[embed(query)],
    anns_field="vector",
    limit=3,
    output_fields=["section", "content", "link", "metadata"],
    search_params={
    "metric_type": "COSINE",
    "params": {}
}
)
    # Validate relevance of the search results
    if not is_context_relevant(query, search_res):
        return "[NO RELEVANT CONTEXT FOUND]"
    
    # Convert results to formatted context
    context = results_to_context(search_res)
    return context