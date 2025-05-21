from sentence_transformers import SentenceTransformer
from retrieval import Retrieval
from generator import Generator
import subprocess
import json
from intent_classifier import IntentClassifier

class Chatbot:

    search_engine = None
    llm = None
    llm_model = None
    ollama_api = None
    ollama_process = None
    config = None
    intent_classfier = None

    def __init__(self):
        self._get_configs()
        self._setup_intent_classifier()
        self._setup_retrieval()
        self._setup_llm()

    def cleanup(self):
        if self.ollama_process and self.ollama_process.poll() is None:
            self.ollama_process.terminate()
            try:
                self.ollama_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.ollama_process.kill()

    def _setup_intent_classifier(self):
        self.intent_classfier = IntentClassifier()

    def _setup_retrieval(self):
        
        embeddings_model = SentenceTransformer(self.config["embeddings_model"])

        with open('./data/fields_to_index.json', 'r') as f:
            fields_to_index = json.load(f)

        self.search_engine = Retrieval(self.config["data_filepath"], fields_to_index, embeddings_model)

    def _setup_llm(self):

        self.llm_model= self.config["LLM_model_name"]
        self.ollama_api = self.config["OLLAMA_API"]

        # start ollama
        self.ollama_process = subprocess.Popen(
            ["ollama", "run", self.llm_model],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True
        )

        self.llm = Generator(self.llm_model)

    def _get_configs(self):
        with open('./data/config.json', 'r') as f:
            self.config = json.load(f)