
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
  - **`data_prep`**: Scripts for data cleaning and preprocessing to format data suitably for model training.
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
3. **Environment Setup:**
Create a `.env` file in the project root directory and add your Spotify API credentials:
    ```bash
    SPOTIFY_CLIENT_ID='your_spotify_client_id'
    SPOTIFY_CLIENT_SECRET='your_spotify_client_secret'
4. **Run the Streamlit app:**
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