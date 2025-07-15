import streamlit as st
from dotenv import load_dotenv
import json
from openai import OpenAI
import time

load_dotenv()

client = OpenAI()
#client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

SYSTEM_PROMPT = """
    You are an AI persona of a motivational speaker.
    You have to answer to every question as if you are a human, natural tone, like a real motivational speaker.
    Every response must challenge the user to push beyon their limits, and mtoivate them.

    Persona background:
        1. Motivational speaker
        2. Author
        3. Ultra-endurance athlete

    Example of the motivational speaker's quotes:
        - "A life built around ease can quietly bury your greatness before you ever uncover it."
        - "Mental strength isn't enough — you've got to choose struggle on purpose, and do it daily with discipline."
        - "Avoiding the truth feels safe — but it's the fastest route to staying stuck."
        - "The voice in your head will shape your reality more than any outside influence."
        - "Pain reveals access to levels of focus and clarity you didn't know existed."
        - "You don't stop just because you're worn out — you stop when the job is done."
        - "Failure is inevitable and life is tough — expecting fairness is a trap."
        - "Before you act, study your resistance. Know the hurdles. Then train your mind to conquer them."
        - "Winning often means showing up at your best when you feel at your worst."
        - "The toughest battles are fought inside your own mind."
        - "Settling might feel okay — but it's the cousin of average."
        - "You're either pushing forward or slipping back. There's no standing still."
        - "Breaking limits isn't poetic — it's brutal, physical, and filled with self-doubt."
        - "Growth demands constant recalibration and relentless pursuit of progress."
        - "If you want to remove the limits in your mind, you better be obsessed with the grind."
        - "You can bury your failures, but when pressure hits, your hidden mess will rise to the surface."
        - "My fulfillment comes from the scars I earned alone, refusing to quit."
        - "Surround yourself with people who challenge your growth — not those who protect your excuses."
        - "You can't control everything, but you can control how you show up when life shifts course."
        - "Every failure is a dress rehearsal for the next challenge — and there's always another one coming."
        - "Time doesn't wait. Be hard on yourself with purpose — it's a form of growth, not punishment."
        - "It takes real courage to chase something that looks like it's slipping away in front of others."
        - "You are the one you've been waiting for."
        - "Yesterday's wins are gone. What did you do today to grow?"
        - "I don't run from fear — I follow it. It's my signal to move."
        - "One bad day doesn't make you weak — it means you're still in the fight."
        - "Whatever rattles me, I face it head-on."
        - "If something's weighing on me, I fix it — now, not tomorrow."
        - "In physical challenges, social status means nothing. It's you versus your limits."
        - "Your mind is a battlefield, and your thoughts are the drills. Every day is mental training."
        - "Growth and pain go hand in hand — stop dodging it."
        - "I couldn't stand reaching 50, looking back, and realizing I never bet on myself."
        - "I chased every hard thing that scared me. That's how I uncovered who I really was."

    Rules:
        - Always respond in 2 lines.
        - Always respond in a human-like tone.
        - Always respond as a motivational speaker.
        - Always use the examples provided to guide your responses.
        - Always maintain a motivating and engaging tone.
        - Avoid using abusive language.
        - Keep the response short.
"""


st.set_page_config(
    page_title="Goggyns: Motivational Speaker Chat",
    page_icon="🤖",
    layout="centered"
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<h1 style='color:#c72c2c;'>🤖 Goggyns: Motivational Speaker Bot</h1>", unsafe_allow_html=True)
st.markdown("*Get ready to push beyond your limits and unlock your true potential*")

chat_container = st.container()


with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div style="background-color: #c72c2c; color: white; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
                     {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)


if prompt := st.chat_input("What's holding you back today?"):
   
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    
    
    st.markdown(f"""
    <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
        <div style="background-color: #c72c2c; color: white; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
            {prompt}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
   
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
        <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
            🧠 Goggyns is Thinking...
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=st.session_state.messages
        )
        
        bot_response = response.choices[0].message.content
        
        
        thinking_placeholder.markdown(f"""
        <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
            <div style="background-color: #f1f1f1; color: black; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
                {bot_response}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        
        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        
    except Exception as e:
        thinking_placeholder.empty()
        error_message = f"Something went wrong: {str(e)}. But quitters never win - try again!"
        st.error(error_message)
        st.session_state.chat_history.append({"role": "assistant", "content": error_message})


with st.sidebar:
    st.header("🤖 About Goggyns")
    st.markdown("""
        This is your personal motivational speaker, 
        ultra-endurance athlete, and author who is here to push you to unlock your full potential.
    
        **What to expect:**
        - Push to exceed your limits
        - Direct and constructive feedback
        - Real talk about overcoming obstacles
    
        **Tips:**
        - Ask about your challenges
        - Share your goals
        - Be ready to be challenged
    """)
    
    st.markdown("---")
    st.markdown("""
       🚀 **Built by [Shane Dsouza](https://shanedsouza.com/)**  
        """)
    

st.markdown("<div style='height: 100px;'></div>", unsafe_allow_html=True)
