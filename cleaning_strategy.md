# Data Cleaning Strategy

Based on the documentation and our analysis, here is the recommended cleaning workflow:

## 1. Loading the Data
*   **Encoding**: Use `encoding='ISO-8859-1'` to handle special characters.
*   **Ids**: Ensure `iid` and `pid` are treated as identifiers, not just numbers.

## 2. Formatting "Hidden" Numbers
Some columns look like numbers but are stored as text because of commas (e.g., `"69,487.00"`).
*   **Target Columns**: `income`, `mn_sat`, `tuition`.
*   **Action**: Remove commas and convert to float.
    ```python
    cols_to_fix = ['income', 'mn_sat', 'tuition']
    for col in cols_to_fix:
        df[col] = df[col].astype(str).str.replace(',', '', regex=False)
        df[col] = pd.to_numeric(df[col], errors='coerce')
    ```

## 3. The "Wave Scaling" Fix (Critical)
Waves 6-9 used a 1-10 scale, while others used 100 points. We must standardize them.
*   **Target Columns**: `attr1_1` through `shar1_1` (and `_2`, `_3` if used).
*   **Action**: Calculate the row-wise total and normalize to percentage.
    ```python
    # Select the 6 attribute columns
    cols = ['attr1_1', 'sinc1_1', 'intel1_1', 'fun1_1', 'amb1_1', 'shar1_1']
    
    # Calculate total points given by the user
    df['total_points'] = df[cols].sum(axis=1)
    
    # Normalize: (Score / Total) * 100
    # This leaves 100-point waves unchanged (mostly) and fixes 1-10 waves
    for col in cols:
        df[col] = (df[col] / df['total_points']) * 100
    ```

## 4. Smart Imputation (Missing Values)
Instead of guessing with the mean, look up the **real** data.

### Subject Data (`age`, `race`, `imprace`)
A person's age doesn't change between dates. If it's missing in one row, it might be present in another.
*   **Action**: Group by `iid` and forward/backward fill.
    ```python
    # Fill missing values within the same person
    demographics = ['age', 'race', 'imprace', 'field_cd', 'goal', 'date', 'go_out']
    df[demographics] = df.groupby('iid')[demographics].transform(lambda x: x.ffill().bfill())
    ```

### Partner Data (`age_o`, `race_o`)
The partner `pid` in your row is a subject `iid` in another row. We can steal their info!
*   **Action**: Create a Lookup Table.
    ```python
    # Create dictionary: iid -> age
    lookup_age = df.groupby('iid')['age'].first().to_dict()
    lookup_race = df.groupby('iid')['race'].first().to_dict()
        
    # Fill missing partner info using the dictionary
    df['age_o'] = df['age_o'].fillna(df['pid'].map(lookup_age))
    df['race_o'] = df['race_o'].fillna(df['pid'].map(lookup_race))
    ```

## 5. Final Sanity Checks
*   **Drop Rows**: If `pid` is missing, the row represents a "skip" or error. Drop these.
*   **Remaining NaNs**: If data is still missing after the smart lookup (e.g., the partner never filled out their own survey), then use the median or drop.
