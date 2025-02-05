from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
import google.generativeai as genai
from langchain.chains import LLMChain
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class Bot:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
        self.prompt = self.create_prompt()
        self.memory = ConversationBufferMemory(input_key="mood", memory_key="chat_history", return_messages=True, k=10)
        self.chatbot_chain = LLMChain(llm=self.llm, prompt=self.prompt, memory=self.memory, verbose=True)

    def create_prompt(self):
        return ChatPromptTemplate.from_template(
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
    
    def chat(self, mood, goal, chat_history):
        response = self.chatbot_chain.run(mood=mood, goal=goal, chat_history=chat_history)
        return response

# Utility function for formatting chat history
def format_chat_history(messages):
    formatted_history = ""
    for msg in messages:
        formatted_history += f"{msg['role']}: {msg['content']}\n"
    return formatted_history
