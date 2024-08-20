import streamlit as st
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from decouple import config
from langchain.memory import ConversationBufferWindowMemory


# Load the CSS file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

prompt = PromptTemplate(
    input_variables=["chat_history", "question"],
    template="""You are an expert paddy farmer with a deep problem solving mindset who can bring well-rounded
    perspectives to any topic related with paddy farming {question}. I would like you to help the farmer to solve their
    {question} by providing a background and possible solution. End by providing me the suggested next 
    questions and action need based on {question}""",
)

llm = ChatOpenAI(openai_api_key=config("OPENAI_API_KEY"), model="gpt-4")
memory = ConversationBufferWindowMemory(memory_key="chat_history", k=4)
llm_chain = LLMChain(llm=llm, memory=memory, prompt=prompt)

# st.set_page_config(page_title="PaddyGPT Assistant", page_icon="🤖", layout="wide")

st.title("Hello farmers, How can I assist you?")

# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = [
        {"role": "assistant", "content": "I am a paddy farmer expert!"}
    ]

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_prompt = st.chat_input()

if user_prompt is not None:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.write(user_prompt)

if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Loading..."):
            ai_response = llm_chain.predict(question=user_prompt)
            st.write(ai_response)
    new_ai_message = {"role": "assistant", "content": ai_response}
    st.session_state.messages.append(new_ai_message)
