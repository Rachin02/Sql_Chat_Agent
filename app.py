import sqlite3
import streamlit as st
from pathlib import Path
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_classic.callbacks.streamlit import StreamlitCallbackHandler
from langchain_classic.agents.agent_types import AgentType
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
load_dotenv()

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"] # remove or comment this line if you are using in local



LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

def clear_history():
    if "messages" not in st.session_state or st.sidebar.button("Clear History"):
          st.session_state["messages"] = [{"role":"assistant","content":"How can I help you?"}]

    st.sidebar.markdown(
        """
            <div style="
                background-color: #8dc6ff;
                color: black;
                padding: 7px;
                border-radius: 10px;
                text-align: center;
                font-size: 13px;
                font-weight: 200;
            ">
                Developed by Rachin
            </div>

        """,
        unsafe_allow_html= True
    )

st.title("Chat with SQL Database")
st.set_page_config(page_title = "SQLchat:Agent", page_icon = "📚")

radio_option = ["Use sqlite 3 student_information.db", "Connect to your MySQL Database"]
select_option = st.sidebar.radio("Choose Database to chat", options= radio_option)

if radio_option.index(select_option) == 1:
    db_uri = MYSQL
    mysql_host = st.sidebar.text_input("Provide MySQL host")
    mysql_user = st.sidebar.text_input("MySQL user")
    mysql_pass = st.sidebar.text_input("MySQL password", type= "password")
    mysql_db = st.sidebar.text_input("MySQL Database")
else:
    db_uri = LOCALDB


api_key = st.sidebar.text_input( label="Enter your API key", placeholder="GPT API key", type="password")

if not db_uri:
    st.info("Please enter the database information and uri")
if not api_key:
    st.info("Please provide your GPT api key")
    st.stop()


model = ChatOpenAI(model = "gpt-4o-mini", api_key = api_key, streaming = True)


@st.cache_resource(ttl = "2h")
def config_db(db_uri, mysql_host= None, mysql_user = None, mysql_pass = None, mysql_db = None):
    if db_uri == LOCALDB:
        db_path = (Path(__file__).parent/"student_batch_221.db").absolute()
        creator = lambda: sqlite3.connect(f"file:{db_path}?mode = ro", uri = True)
        return SQLDatabase(create_engine(f"sqlite:///", creator = creator))
    elif db_uri == MYSQL:
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{mysql_user}:{mysql_pass}@{mysql_host}/{mysql_db}"))



if db_uri == MYSQL:
    if not (mysql_host and mysql_user and mysql_pass and mysql_db):
            st.error("Please provide all MySQL connection details.")
            clear_history()
            st.stop()
    else:
            db = config_db(db_uri, mysql_host, mysql_user, mysql_pass, mysql_db)
else:
    db = config_db(db_uri)


toolkit = SQLDatabaseToolkit(llm = model, db = db)
sql_agent = create_sql_agent(llm = model, toolkit = toolkit, verbose = True, agent_type = AgentType.ZERO_SHOT_REACT_DESCRIPTION, max_iterations=20 )
sql_agent.handle_parsing_errors = True

clear_history()

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])


user_input = st.chat_input("Ask Question")

if user_input:
    st.session_state.messages.append({"role":"user","content":user_input})
    st.chat_message("user").write(user_input)

    with st.chat_message("assistant"):
        streamlit_callback = StreamlitCallbackHandler(st.container())

        response = sql_agent.run(user_input, callbacks= [streamlit_callback])
        st.session_state.messages.append({"role":"assistant","content":response})
        st.write(response)
