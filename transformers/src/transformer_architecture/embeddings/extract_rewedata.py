
import re
import pdfplumber
import glob
import pandas as pd
import os

file_abs_path = os.path.abspath(os.path.dirname(__file__))
# print(f"Absolute path of the current file: {file_abs_path}")
def pdf_extract_convert_to_text():
    # 'transformers\src\transformer_architecture\embeddings\data\ReweData'
    pdf_dir = os.path.join(file_abs_path, 'data\ReweData')
    data = []

    try:
        for file_path in glob.glob(pdf_dir + "/*.pdf"):
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            
            data.append({
                "filename": file_path.split("\\")[-1],
                "document": text
            })

        df = pd.DataFrame(data)
        df.to_csv(os.path.join(file_abs_path, "data\\rewedata.csv"), index=False)
        print("Dataset conversion and saving complete!")

        return True
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def read_csv_to_dataframe():
    try:
        df = pd.read_csv(os.path.join(file_abs_path, r"data\rewedata.csv"))
        print("CSV file read successfully!")
        return df
    except FileNotFoundError:
        print("CSV file not found. Please ensure it has been created.")
        return None
    

def extract_rewedata():
    if not os.path.exists(os.path.join(file_abs_path, "data\\rewedata.csv")):
        if not pdf_extract_convert_to_text():
            print("Failed to convert PDF to CSV.")
    else:
        print("CSV file already exists, skipping conversion.")  

    df = read_csv_to_dataframe()    
    if df is not None:
        print(df.head())   
        return df

if __name__ == "__main__":
     
       extract_rewedata()
