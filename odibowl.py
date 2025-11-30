# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib

def custom_ODI_bowl(bowl, name, oname):
    # Load the dataset
    df_bowl = pd.read_csv('bowling_odi.csv')

    # Data Preprocessing
    # Drop unnecessary columns
    df_bowl = df_bowl[['Player', 'Team', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ', 'Opponent']]

    # Convert non-numeric values to NaN
    df_bowl[['Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']] = df_bowl[['Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']].apply(pd.to_numeric, errors='coerce')

    # Handling missing values
    imputer = SimpleImputer(strategy='mean')
    df_bowl[['Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']] = imputer.fit_transform(df_bowl[['Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']])

    # Convert 'Ave' and 'Econ' to numeric (if not already)
    df_bowl['Ave'] = pd.to_numeric(df_bowl['Ave'], errors='coerce')
    df_bowl['Econ'] = pd.to_numeric(df_bowl['Econ'], errors='coerce')

    # Drop rows with missing or non-numeric values in the target variable ('Ave' and 'Econ')
    df_bowl = df_bowl.dropna(subset=['Ave', 'Econ'])

    # Take user input for the number of players, your team, and the opponent team
    num_players = int(bowl)
    your_team = name
    opponent_team = oname

    # Filter data for the specified teams
    filtered_df_bowl = df_bowl[(df_bowl['Opponent'].str.contains(opponent_team, case=False, regex=True)) & (df_bowl['Team'].str.contains(your_team, case=False, regex=True))]

    # Check if there are enough players against the specified opponent
    if len(filtered_df_bowl) < num_players:
        print(f"Error: There are not enough players against {opponent_team} for {your_team}.")
        return f"Error: There are not enough players against {opponent_team} for {your_team}."
    else:
        # Feature selection
        X_bowl = filtered_df_bowl[['Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']]
        y_bowl = filtered_df_bowl['Ave']  # Choose an appropriate target variable

        # Model Selection and Training
        model_bowl = RandomForestRegressor()
        model_bowl.fit(X_bowl, y_bowl)

        # Save the trained model to a file
        joblib.dump(model_bowl, 'custom_bowling_model.joblib')

        # Make predictions using the loaded model
        loaded_model_bowl = joblib.load('custom_bowling_model.joblib')
        predicted_ave = loaded_model_bowl.predict(X_bowl)

        # Get the top players based on predicted averages
        top_players_indices = predicted_ave.argsort()[::-1][:num_players]
        top_players = filtered_df_bowl.iloc[top_players_indices]

        # Print the top players along with their statistics
        print(f'Top {num_players} Players against {opponent_team} for {your_team}:')
        print(top_players[['Player', 'Mat', 'Inns', 'Overs', 'Mdns', 'Runs', 'Wkts', 'Ave', 'Econ']])
        return top_players