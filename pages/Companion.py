# pages/chatbot.py
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import google.generativeai as genai
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="SoulSpace", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "Bot", "content": "Hi! I'm your wellness and personal Bot companion. How can I help you today?"}
    ]

def format_chat_history(messages):
    formatted_history = ""
    for msg in messages:
        formatted_history += f"{msg['role']}: {msg['content']}\n"
    return formatted_history

def initialize_chatbot():
    llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    
    prompt = ChatPromptTemplate.from_template(
        """
        
            You are a compassionate, empathetic, and non-judgmental mental health companion. Your role is to help users process their feelings, feel heard, and take small steps toward emotional well-being. Always respond in a warm, friendly, and supportive tone.
            
            **Guidelines for Interaction:**
            1. **Acknowledge Feelings**: Validate the user's emotions and let them know it's okay to feel the way they do.
            2. **Ask Open-Ended Questions**: Encourage users to explore their feelings further.
            3. **Offer Gentle Suggestions**: Provide actionable advice or mindfulness exercises, but only if the user seems open to it.
            4. **Avoid Judgment**: Never criticize or dismiss the user's feelings.
            5. **Be Patient**: Allow users to express themselves at their own pace.
            6. **Maintain Context**: Reference previous parts of the conversation when relevant.
            
            **Complete Conversation History:**
            {chat_history}
            
            **User's Current Message:**
            {mood}
            
            **User's Goal (if any):**
            {goal}
            
            **Your Response:**
            Based on the complete conversation history and the user's current message, provide a contextually appropriate response that:
            1. Shows you've understood the ongoing conversation
            2. References relevant details from previous messages when appropriate
            3. Maintains a coherent thread of discussion
            4. Offers support and guidance that builds on previous interactions
            
        """
    )

    memory = ConversationBufferMemory(
        input_key="mood",
        memory_key="chat_history",
        return_messages=True,
        k=10
    )

    chatbot_chain = LLMChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        verbose=True
    )

    return chatbot_chain

def chat_with_bot(mood, goal, messages):
    chatbot_chain = initialize_chatbot()
    chat_history = format_chat_history(messages[:-1])
    response = chatbot_chain.run(
        mood=mood,
        goal=goal,
        chat_history=chat_history
    )
    return response

# Chatbot UI
st.title("Chat with your Wellness Companion")

# Add a button to return to the main page
if st.button("← Return to Journal"):
    st.switch_page("Home.py")

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(f"**{message['role']}:** {message['content']}")

# User input
input_text = st.chat_input("How are you feeling today?")
if input_text:
    # Add user message to history
    st.session_state.messages.append({"role": "User", "content": input_text})
    with st.chat_message("User"):
        st.markdown(f"**User:** {input_text}")

    # Generate response
    if st.session_state.messages[-1]["role"] != "Bot":
        with st.chat_message("Bot"):
            with st.spinner("Thinking..."):
                response = chat_with_bot(
                    input_text,
                    "",
                    st.session_state.messages
                )
                st.markdown(f"**Bot:** {response}")
        st.session_state.messages.append({"role": "Bot", "content": response})