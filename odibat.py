# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib

def custom_ODI_bats(bat, name, oname):
    # Load the dataset
    df = pd.read_csv('batting_odi.csv', encoding='latin-1')

    # Data Preprocessing
    # Drop unnecessary columns
    df = df[['Player', 'Mat', 'Ave', 'SR', 'Runs', 'Opponent', 'Team']]

    # Convert non-numeric values to NaN
    df[['Mat', 'Ave', 'SR', 'Runs']] = df[['Mat', 'Ave', 'SR', 'Runs']].apply(pd.to_numeric, errors='coerce')

    # Handling missing values
    imputer = SimpleImputer(strategy='mean')
    df[['Mat', 'Ave', 'SR', 'Runs']] = imputer.fit_transform(df[['Mat', 'Ave', 'SR', 'Runs']])

    # Convert 'Runs' to numeric (if not already)
    df['Runs'] = pd.to_numeric(df['Runs'], errors='coerce')

    # Drop rows with missing or non-numeric values in the target variable ('Runs')
    df = df.dropna(subset=['Runs'])

    # Take user input for the number of players, your team, and the opposite team
    num_players = int(bat)
    team = name
    opponent_team = oname

    # Filter data for the specified teams
    filtered_df = df[(df['Opponent'] == opponent_team) & (df['Team'] == team)]

    # Check if there are enough batsmen against the specified opponent team for the given player's team
    if len(filtered_df) < num_players:
        print(f"Error: There are not enough batsmen against {opponent_team} for {team}.")
        return f"Error: There are not enough batsmen against {opponent_team} for {team}."
    else:
        # Feature selection
        X = filtered_df[['Mat', 'Ave', 'SR', 'Runs']]
        y = filtered_df['Runs']

        # Model Selection and Training
        model = RandomForestRegressor()
        model.fit(X, y)

        # Save the trained model to a file
        joblib.dump(model, 'custom_batting_odimodel.joblib')

        # Make predictions using the loaded model
        loaded_model = joblib.load('custom_batting_odimodel.joblib')
        predicted_runs = loaded_model.predict(X)

        # Get the top players based on predicted runs
        top_players_indices = predicted_runs.argsort()[::-1][:num_players]
        top_players = filtered_df.iloc[top_players_indices]

        # Print the top players along with their statistics
        print(f'Top {num_players} Batsmen against {opponent_team} for {team}:')
        print(top_players[['Player', 'Mat', 'Ave', 'SR', 'Runs']])
        return top_players