from rag.retriever import retrieve

class RightsLawAgent:

    def get_relevant_laws(self, clause):

        docs = retrieve(clause)

        results = []

        for doc in docs:

            results.append({
                "source": doc.metadata,
                "content": doc.page_content[:300]
            })

        return results
    