import pandas as pd
from sqlalchemy import create_engine
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import warnings
warnings.filterwarnings("ignore")

def import_csv_to_sql():
    # Hide the main Tkinter window
    Tk().withdraw()
    
    # Show an "Open" dialog box and return the path to the selected file
    filename = askopenfilename()
    
    # Read CSV file
    df = pd.read_csv(filename)
    
    # Create SQLAlchemy engine
    engine = create_engine('mysql+pymysql://root:admin123@localhost/data')
    
    # Import data into MySQL database
    table_name = input('Enter the table name:')
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)


