# Import necessary libraries
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
import joblib

def custom_test_bats(bat, name, oname):
    # Load the dataset
    df = pd.read_csv('batting_test.csv', encoding='latin-1')

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

    # Debug print to check unique teams in the dataset
    print("Unique Teams in Dataset:", df['Team'].unique())
    print("Unique Opponent Teams in Dataset:", df['Opponent'].unique())

    # Filter data for the specified teams
    filtered_df = df[(df['Opponent'].str.strip().str.lower() == opponent_team.strip().lower()) & 
                  (df['Team'].str.strip().str.lower() == team.strip().lower())]

##    # Debug print to check the filtered dataframe
##    print("Filtered DataFrame:")
##    print(filtered_df)

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
        joblib.dump(model, 'custom_batting_testmodel.joblib')

        # Make predictions using the loaded model
        loaded_model = joblib.load('custom_batting_testmodel.joblib')
        predicted_runs = loaded_model.predict(X)

        # Add predicted_runs to the dataframe
        filtered_df['PredictedRuns'] = predicted_runs

        # Get the top players based on predicted runs
        top_players = filtered_df.sort_values(by='PredictedRuns', ascending=False).head(num_players)

        # Print the top players along with their statistics
        print(f'Top {num_players} Batsmen against {opponent_team} for {team}:')
        print(top_players[['Player', 'Mat', 'Ave', 'SR', 'Runs', 'PredictedRuns']])
        return top_players