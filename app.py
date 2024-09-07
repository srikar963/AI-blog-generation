import os
from turtle import st
from secret_api_keys import huggingface_api_key
os.environ['HUGGINGFACEHUB_API_TOKEN'] = huggingface_api_key

# Import Hugging Face endpoint class
from langchain_huggingface import HuggingFaceEndpoint
llm = HuggingFaceEndpoint(
repo_id= 'meta-llama/Meta-Llama-3-8B-Instruct',
token = huggingface_api_key,
temperature= 0.6
)

from langchain.prompts import PromptTemplate 
prompt_template_for_title_suggestion = PromptTemplate(
    input_variables=['topic'],
    template = 
    '''
I'm planning a blog post on topic : {topic}.
The title is informative, or humorous or persuasive.
The target audience is beginners, tech enthusiasts.
Suggest a list of ten cerative and attention-grabbing titles for this blog post.
Don't give any explanation or overview to each title.
    '''
)

# Define a PromptTemplate for blog content generation
prompt_template_for_blog = PromptTemplate(
    input_variables=['title', 'keywords', 'blog_length'],  # Specify input variables
    template=  # Define the prompt template
    '''Write a high-quality, informative, and plagiarism-free blog post on the topic: "{title}". 
    Target the content towards a beginner audience. 
    Use a conversational writing style and structure the content with an introduction, body paragraphs, and a conclusion. 
    Try to incorporate these keywords: {keywords}. 
    Aim for a content length of {blog_length} words. 
    Make the content engaging and capture the reader's attention.'''
)

#Create the chains
title_chain = prompt_template_for_title_suggestion | llm
#Blog Chain
blog_chian = prompt_template_for_blog | llm


#Desigining the user interface
import streamlit as st
st.title('AI Blog Content Assistant...🤖')
st.subheader('Create High-Quality Blog Content Without Breaking the Bank')
#Titile Generation
st.subheader('Title Generation')
topic_expander = st.expander('Input the topic')
with topic_expander:
    topic_name = st.text_input('',key = 'topic_name')
    button_topic = st.button('Submit the topic')
if button_topic:
    st.write(title_chain.invoke({topic_name}))
#Feature - 2 Blog generation
st.subheader('Blog Generation')
blog_expander = st.expander('Input Blog details ')

with blog_expander: 
    title_of_the_blog = st.text_input('',key = 'title_name')
    num_of_words = st.slider ('Number of words', min_value =50, max_value =1000, step=50)

    if 'keywords' not in st.session_state: # Manage keyword list in session state
        st.session_state['keywords'] = []  # Initialize empty list on first run
    keyword_input = st.text_input("Enter a keyword:") # Input field for adding keywords
    keyword_button = st.button("Add Keyword") # Button to add keyword to the list
    if keyword_button: # Handle button click for adding keyword
        st.session_state['keywords'].append(keyword_input) # Add the keyword to the session state list
        st.session_state['keyword_input'] = "" # Clear the keyword input field after adding
        for keyword in st.session_state['keywords']:  # Display the current list of keywords
            # Inline styling for displaying keywords
            st.write(f"<div style='display: inline-block; background-color: lightgray; padding: 5px; margin: 5px;'>{keyword}</div>", unsafe_allow_html=True)
    button_blog = st.button('Submit the info')
if button_blog:
    st.write(st.session_state['keywords'])
    st.subheader(title_of_the_blog)
    #st.write(blog_chian.invoke({'title': title_of_the_blog, 'keywords': formatted_keywords, 'blog_length':num_of_words}))
