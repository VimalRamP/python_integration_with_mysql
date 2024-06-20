import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings("ignore")

def perform_eda(table_name):
    # Create SQLAlchemy engine
    engine = create_engine('mysql+pymysql://root:admin123@localhost/data')
    
    # Read data from SQL table
    df = pd.read_sql_table(table_name, con=engine)

    # Define your plots and colors
    plots = ['hist', 'box', 'kde', 'scatter', 'pairplot']
    colors = ['blue', 'green', 'red', 'cyan', 'magenta']

    # Perform EDA with 5 different plots
    for plot, color in zip(plots, colors):
        if plot == 'hist':
            df.hist(color=color)
        elif plot == 'box':
            df.plot(kind='box', color=color)

        # Show the plot
        plt.show()    

    # Generate correlation heatmap
    numeric_columns = df.select_dtypes(include=["float","int"])
    plt.figure(figsize=(10,5))
    corr_matrix = numeric_columns.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix Heatmap')
    plt.show()

    
    

