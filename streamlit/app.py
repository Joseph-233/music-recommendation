# Import Streamlit
import streamlit as st
import subprocess 

# Add a title and some text to your app
st.title('Spotify Running Recomender')
st.write('This is a streamlit application that leverages a recommendation model that takes into account your Spotify data and recommends songs based on the heart rate number provided. Hopefully it can help you find the perfect playlist for your next run.')

# The path to spotify_auth.py from the streamlit folder
script_path = '../spotify_reco/spotify_auth.py'

# Add a button to run the spotify_auth.py script
if st.button('Authorize Spotify'):
    # This will run your spotify_auth.py script located in the spotify_reco directory
    result = subprocess.run(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    # You can display the output or error to the Streamlit app if you want
    if result.returncode == 0:
        # If the script ran successfully
        st.success('Authorization successful!')
        # st.code(result.stdout)
    else:
        # If the script failed
        st.error('Authorization failed.')
        # st.code(result.stderr)

st.title('Heart Rate Input:')

# User input for heart rate
heart_rate = st.number_input('Enter your heart rate (bpm)', min_value=0)

# Display the entered heart rate
if heart_rate:
    st.write(f'Your entered heart rate is: {heart_rate} bpm')

    # Button for getting recommendations
if st.button('Get Recommendations'):
    # Placeholder for the logic to get recommendations
    # You would include any code here that is needed to get the recommendations
    # For now, it will just display a message
    st.write('Here are your recommendations...')
    # If you have the logic for recommendations, you can call it here
    # and display the results instead of the placeholder text


st.title('Top 10 Songs for Running:')

