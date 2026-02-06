
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Load a sample of data (or recreate structure)
try:
    df = pd.read_csv('c:/Users/Admin/Documents/Jedha_Training/data_scientist/eda/tinder_project/Speed+Dating+Data.csv', encoding='ISO-8859-1')
except:
    # Fallback if file not readable here, verify logic with dummy data
    print("Could not load CSV, using dummy data")
    df = pd.DataFrame({
        'gender': [0, 0, 1, 1] * 10,
        'wave': [1, 2, 1, 2] * 10,
        'attr1_1': [10, 20, 15, 25] * 10,
        'sinc1_1': [10, 10, 10, 10] * 10,
        'intel1_1': [10, 10, 10, 10] * 10,
        'fun1_1': [10, 10, 10, 10] * 10,
        'amb1_1': [10, 10, 10, 10] * 10,
        'shar1_1': [10, 10, 10, 10] * 10,
    })

# Normalize (Simple version for repro)
cols_1_1 = ['attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1']

# The "Suspect" Block
population_1_1 = df.dropna(subset=cols_1_1)
print("Running Suspect Block... Done.")
print(f"Original DF Shape: {df.shape}")
print(f"Population 1_1 Shape: {population_1_1.shape}")

# The Plotting Logic
def inspect_containers(df, columns):
    value_cols = [c for c in columns if c != 'gender']
    sub_df = df[columns]
    melted = pd.melt(sub_df, id_vars=["gender"], value_vars=value_cols,
                     var_name="Variable_Attribut", value_name="Score_Importance")

    plt.figure(figsize=(10, 6))
    # Note: errorbar=('ci', 95) is the key
    try:
        ax = sns.barplot(
            data=melted,
            x="Variable_Attribut",
            y="Score_Importance",
            hue="gender",
            estimator="mean",
            errorbar=("ci", 95) 
        )
    except Exception as e:
        print(f"Seaborn raised error: {e}")
        return

    print(f"\nNumber of containers: {len(ax.containers)}")
    for i, container in enumerate(ax.containers):
        print(f"\n--- Container {i} ---")
        print(f"Type: {type(container)}")
        if len(container) > 0:
            elem = container[0]
            print(f"First element type: {type(elem)}")
            if hasattr(elem, 'get_height'):
                attr = getattr(elem, 'get_height')
                print(f"Has get_height? Yes. Type: {type(attr)}")
                if callable(attr):
                    print("get_height is callable (method)")
                else:
                    print("get_height is NOT callable (property/attribute)")

inspect_containers(df, ['gender'] + cols_1_1)
