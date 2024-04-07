
# Run Pace Music Recommender System (RPMRS)

## Overview
The Run Pace Music Recommender System (RPMRS) enhances the running experience by dynamically recommending music that synchronizes with the runner's pace. Developed using Spotify's extensive dataset and advanced machine learning models, this system personalizes music playlists to fit individual running sessions based on tempo and previous user preferences.

## Features
- **Dynamic Music Recommendations**: Adjusts music recommendations in real-time based on the user's inputted heart rate.
- **Integration with Spotify API**: Leverages Spotify's rich dataset for up-to-date music metadata and user preferences.
- **User-friendly Interface**: Offers an intuitive interface built with Streamlit, allowing users to easily interact with the system.
- **Advanced Analytics**: Utilizes machine learning models, including LightGBM and KMeans clustering, to predict music preferences.

## Project Structure
The repository is organized into several main directories:

- **`spotify_reco`**:
  - **`eda`**: Contains Jupyter notebooks used for exploratory data analysis, feature engineering, and initial data insights.
- **`models`**: Includes trained models and scripts for model training and evaluation.
- **`streamlit`**:
  - **`app.py`**: The Streamlit application file that users interact with to receive music recommendations.

## Installation
To set up the project locally, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Joseph-233/music-recommendation.git
   cd music-recommendation
2. **Install Dependencies:**
Ensure you have Python 3.8+ installed, then run:
    ```bash
    pip install -r requirements.txt
3. **Setting Up Spotify API Credentials:**
You need to register the application with Spotify to obtain credentials necessary for using its Web API.
- **Create Spotify Application:**
Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an application. During the setup, set the Redirect URI to `http://localhost:8888/callback/` and tick 'Web API' under "Which API/SDKs are you planning to use?"
- **Obtain Credentials:**
Navigate to the app settings in your Spotify Developer Dashboard, and copy your Client ID and Client Secret.
- **Configure Credentials Locally:**
Create two files in the root directory of your project to store these credentials securely:
  ```bash
  echo YOUR_CLIENT_ID > client_id.txt
  echo YOUR_CLIENT_SECRET > client_secret.txt
Replace **'YOUR_CLIENT_ID'** and **'YOUR_CLIENT_SECRET'** with the actual values.

5. **Run the Streamlit app:**
Navigate to the `streamlit` directory and start the app:
    ```bash
    streamlit run app.py

## Usage
After launching the Streamlit app, input your current heart rate into the provided field. The system will use this along with your historical Spotify data to generate a personalized playlist that matches your running tempo.
## Contributing
We welcome contributions to the RPMRS project! If you have suggestions for improvements or new features, please open an issue or submit a pull request.
1. **Submitting Pull Requests:**
- Fork the repository.
- Create a new branch for your feature.
- Add your changes and commit with a clear message describing the enhancement.
- Push the branch and open a pull request against the main branch.
2. **Opening Issues:**
- Use GitHub Issues to submit bugs, feature requests, or suggestions.
- Be as specific as possible about the problem and suggest possible solutions if applicable.
