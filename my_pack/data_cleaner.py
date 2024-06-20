import pandas as pd
from sqlalchemy import create_engine
from scipy import stats
import warnings
warnings.filterwarnings("ignore")

def clean_data(table_name):
    # Create SQLAlchemy engine
    engine = create_engine('mysql+pymysql://root:admin123@localhost/data')
    
    # Read data from SQL table
    df = pd.read_sql_table(table_name, con=engine)
    
    # Show info, describe, shape
    print(df.info())
    print(df.describe())
    print(f"Shape: {df.shape}")

    # Null values by column, total null values
    null_values_by_column = df.isnull().sum()
    total_null_values = null_values_by_column.sum()
    print(f"Null values by column:\n{null_values_by_column}")
    print(f"Total null values: {total_null_values}")

    # Drop duplicates
    df = df.drop_duplicates()

    # Drop columns with more than 50% null values
    half_null = len(df) / 2
    df = df.dropna(thresh=half_null, axis=1)

    # Null values in rows
    null_values_in_rows = df.isnull().sum(axis=1).max()
    print(f"Maximum null values in rows:\n{null_values_in_rows}")

    # Calculate the IQR for each numeric column
    Q1 = df.select_dtypes(include=['number']).quantile(0.25)
    Q3 = df.select_dtypes(include=['number']).quantile(0.75)
    IQR = Q3 - Q1

    # Define the upper and lower bounds for outlier detection
    lower_bound = (Q1 - 1.5 * IQR)-1
    upper_bound = (Q3 + 1.5 * IQR)+1

    # Remove rows with outliers
    df = df[~((df.select_dtypes(include=['number']) < lower_bound) | (df.select_dtypes(include=['number']) > upper_bound)).any(axis=1)]

    # Impute mean value for missing values in numerical columns
    for col in df.select_dtypes(include=['number']).columns:
        df[col].fillna(df[col].mean(), inplace=True)

    # Impute mode for each categorical column
    for col in df.select_dtypes(include='object').columns:
        mode_value = df[col].mode().iloc[0]
        df[col].fillna(mode_value, inplace=True)

    # Unique values
    unique_values = df.apply(lambda x : x.unique())
    print(f"Unique values:\n{unique_values}")

    # Show all columns and ask if want to drop any columns
    print(f"All columns: {df.columns.tolist()}")
        
    # Ask user if they want to drop any columns and drop them if requested
    columns_to_drop = input("Enter columns to drop (comma-separated): ").split(',')
        
    # Check if user entered any columns to drop and if those columns exist in the DataFrame
    if columns_to_drop != [''] and all(col in df.columns for col in columns_to_drop):
        df.drop(columns=columns_to_drop, inplace=True)
        
    # Finally show the shape
    print(f"Final shape: {df.shape}")
    
    # Write cleaned data back to SQL
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

