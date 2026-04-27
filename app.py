import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="Chase Hughes AI", page_icon="🧠")
st.title("🧠 Chase Hughes AI")

tab1, tab2 = st.tabs(["Chat", "Email Assistant"])

with tab1:
    st.header("Ask Chase Hughes")
    question = st.text_area("Ask anything about behavior, influence, or psychology:", height=100)
    if st.button("Get Answer", key="chat"):
        if question:
            with st.spinner("Thinking..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are Chase Hughes, behavioral expert and author of The Ellipsis Manual, Six Minute X-Ray, Tongue, and The Behavior Ops Manual. Answer using his frameworks: FATE, BMEPA, elicitation, behavior stacking, baseline, compliance triggers. Be direct and tactical."},
                        {"role": "user", "content": question}
                    ]
                )
                st.write(response.choices[0].message.content)

with tab2:
    st.header("Email Assistant")
    email = st.text_area("Paste the email you received:", height=200)
    if st.button("Write Response", key="email"):
        if email:
            with st.spinner("Crafting response..."):
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are Chase Hughes. Read this email and write a response using behavioral influence principles. Be strategic, direct, and use rapport building techniques."},
                        {"role": "user", "content": f"Write a response to this email:\n\n{email}"}
                    ]
                )
                st.write(response.choices[0].message.content)