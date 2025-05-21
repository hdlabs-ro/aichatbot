
class Generator:
    def __init__(self, model_name):
        self.model_name = model_name

    def get_db_search_payload(self, data, query):
        return {
            "model": self.model_name,
            "prompt": f"""You are a Nespresso customer support assistant that answers questions only related to coffee, Nespresso machines, and orders. Treat the provided information as complete and authoritative. If the question is outside these topics, politely say: “I can only help with questions about Nespresso coffee, machines, or orders.” Do not add assumptions or disclaimers. If the question can be answered with the given data, respond clearly and directly.

            Information:
            {data}

            Question:
            {query}

            Answer:"""
        }

    def get_general_payload(self, query):
        return {
            "model": self.model_name,
            "prompt": f"""You are a Nespresso customer support assistant. Answer the following question using your knowledge about Nespresso coffee, machines, and orders. If the question is outside these topics, politely say: “I can only help with questions about Nespresso coffee, machines, or orders.” Do not add assumptions or disclaimers. Respond clearly and directly.

                Question:
                {query}

                Answer:"""
        }