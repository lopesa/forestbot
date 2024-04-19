import streamlit as st
from streamlit_chat import message
import Call_RAG

st.set_page_config(page_title="ForestBot Demo", page_icon=":robot:")
st.title("Forestbot")

# Initialize session variables if they are not already defined
if "generated" not in st.session_state:
    st.session_state["generated"] = []
    print("Initialized st.session_state['generated']")

if "past" not in st.session_state:
    st.session_state["past"] = []
    print("Initialized st.session_state['past']")

def get_text():
    input_text = st.text_input("You: ", "Ask a question", key="input")
    submit_button = st.button("Ask")
    print("Input Text:", input_text)  # Displays the entered text
    return input_text, submit_button

print("Script started or rerun")  # Indicates each time the script is executed or re-executed
user_input, submitted = get_text()

# Check if the button was pressed before calling Call_RAG.ask
if submitted and user_input:
    print("Button pressed with input:", user_input)  # Shows that the button was pressed with input
    output = Call_RAG.ask(user_input)
    print("Output from Call_RAG.ask:", output)  # Displays the output from the ask function
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)
    print("Updated st.session_state with new input and output")

print("Displaying messages")  # Indicates that messages will be displayed

# Display of generated messages and user questions
if st.session_state["generated"]:
    print("st.session_state['generated'] contents:", st.session_state["generated"])  # Displays the contents of generated
    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
