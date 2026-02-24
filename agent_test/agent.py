import vertexai
from vertexai.preview import reasoning_engines
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Configuración inicial
AGENT_DEPLOY_NAME =  "Agent-test-01"
PROJECT_ID = "bluetab-colombia-data-qa"
LOCATION = "us-central1" # O tu región preferida
STAGING_BUCKET = "gs://bluetab-colombia-data-qa-staging-bucket" # Necesario para guardar el código
GEMINI_VERSION = "gemini-2.0-flash-exp"


vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

# 2. Definir el agente como una Clase
class HolaMundoAgent:
    def __init__(self, model_name: str):
        self.model_name = model_name

    def set_up(self):
        from langchain_google_vertexai import ChatVertexAI
        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
        from langchain_core.runnables.history import RunnableWithMessageHistory
        from langchain_community.chat_message_histories import ChatMessageHistory
        
        self.model = ChatVertexAI(model=self.model_name)
        
        # El prompt ahora debe incluir un lugar para el historial
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "Eres un asistente con memoria persistente."),
            MessagesPlaceholder(variable_name="history"),
            ("user", "{input}")
        ])
        
        self.chain = self.prompt | self.model
        
        # Usamos un diccionario local para este ejemplo, pero Agent Engine 
        # puede persistir esto si usas VertexAISessionService
        self.history_store = {}

        def get_session_history(session_id: str):
            if session_id not in self.history_store:
                self.history_store[session_id] = ChatMessageHistory()
            return self.history_store[session_id]

        self.with_history = RunnableWithMessageHistory(
            self.chain,
            get_session_history,
            input_messages_key="input",
            history_messages_key="history",
        )

    def query(self, input: str, session_id: str = "default"):
        # Importante: Ahora el método recibe un session_id
        return self.with_history.invoke(
            {"input": input},
            config={"configurable": {"session_id": session_id}}
        ).content

# 3. Desplegar
agent_instance = HolaMundoAgent(model_name=GEMINI_VERSION)

remote_agent = reasoning_engines.ReasoningEngine.create(
    agent_instance,
    requirements=[
        "google-cloud-aiplatform[reasoningengine,langchain]",
        "langchain-google-vertexai",
        "langchain-community", # <--- ESENCIAL para usar ChatMessageHistory
        "cloudpickle",
        "pydantic",
    ],
    display_name=AGENT_DEPLOY_NAME,
)

print(f"Despliegue finalizado: {remote_agent.resource_name}")