import os
import pandas as pd

def load_xls(filename="10A.xls"):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, filename)

    # File is actually HTML disguised as .xls
    tables = pd.read_html(path, encoding="utf-8")  # returns a list of DataFrames
    if not tables:
        raise ValueError("No tables found in the file.")

    # Usually the first table is the grade table
    return tables[0]

def main():
    df = load_xls("10A.xls")
    print("Loaded:", df.shape)
    print(df.head())

    import code
    code.interact(local={"df": df, "pd": pd})

if __name__ == "__main__":
    main()
