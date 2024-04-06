from ast import mod
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from math import sqrt
from joblib import dump, load
import lightgbm as lgb
import pandas as pd

track_data_route = "spotify_reco/datasets/dataset_ready.csv"
aggregated_play_count_route = "spotify_reco/datasets/aggregated_play_count.csv"
model_route = "spotify_reco/models/saved_models/multi_output_lgb_regressor.joblib"
global model


def aggregate_play_count(route=track_data_route):
    track_data = pd.read_csv(route)
    track_data.drop(columns=track_data.columns[0], inplace=True)
    track_data.drop(["user", "user_encoded"], axis=1, inplace=True)
    column_without_play_count = track_data.drop("play_count", axis=1).columns.to_list()
    aggregated_data = track_data.groupby(column_without_play_count, as_index=False)[
        "play_count"
    ].sum()
    aggregated_data.to_csv(aggregated_play_count_route, index=False)


def get_predicted_features_name():
    track_data = pd.read_csv(aggregated_play_count_route)
    # print(track_data.loc[:, "tempo"].describe())
    return track_data.loc[:, "danceability":"valence"].columns.to_list()


def train_lgb():
    global model

    track_data = pd.read_csv(aggregated_play_count_route)
    tempo = track_data[["tempo"]]
    other_features_name = track_data.loc[:, "danceability":"valence"].columns.to_list()
    other_features = track_data.loc[:, other_features_name]

    # Create a LightGBM regressor
    lgb_regressor = lgb.LGBMRegressor()

    # Create a MultiOutputRegressor with LightGBM regressor
    multi_output_regressor = MultiOutputRegressor(lgb_regressor)

    X_train, X_test, y_train, y_test = train_test_split(
        tempo, other_features, test_size=0.2, random_state=42
    )
    # Fit the model
    model = multi_output_regressor.fit(X_train, y_train)

    # Get accuracy
    # predictions = predict_features(X_test)
    # # Calculate R-squared score for each output
    # for column in y_test.columns:
    #     y_test_one_feature = y_test.loc[:, column]
    #     y_pred_one_feature = predictions.loc[:, column]

    #     r2 = r2_score(y_test_one_feature, y_pred_one_feature)

    #     # Calculate RMSE
    #     rmse = sqrt(mean_squared_error(y_test_one_feature, y_pred_one_feature))

    #     # Calculate MAE
    #     mae = mean_absolute_error(y_test_one_feature, y_pred_one_feature)

    #     print(f"\nR-squared score for output {column}: {r2}")
    #     print(f"RMSE: {rmse}")
    #     print(f"MAE: {mae}")
    # print("predict 20000 bpm", multi_output_regressor.predict([[20000]]))
    print("predict 10 bpm", multi_output_regressor.predict(X_test))
    # print(multi_output_regressor.get_params())


def predict_features(tempo):
    global model
    track_data = pd.read_csv(aggregated_play_count_route)
    tempo_normalized = ((tempo - 40) / (200 - 40)) * (
        track_data.loc[:, "tempo"].max() - track_data.loc[:, "tempo"].min()
    ) + track_data.loc[:, "tempo"].min()
    features = model.predict([[tempo_normalized]])
    print("predict_features", features)
    columns = get_predicted_features_name()
    columns = ["target_" + col for col in columns]
    return pd.DataFrame(features, columns=columns)


def save_model():
    dump(model, model_route)


def load_model():
    global model
    model = load(model_route)


# train_lgb()
