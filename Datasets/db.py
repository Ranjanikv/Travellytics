import pandas as pd
from sqlalchemy import create_engine

# -------------------------------
# 1. DATABASE CONNECTION
# -------------------------------
try:
    engine = create_engine(
        "mysql+mysqlconnector://root:Security*101@localhost:3306/tourism_db"
    )
    conn = engine.connect()
    print("✅ Connected to MySQL database!")
except Exception as e:
    print(f"❌ Database connection failed: {e}")
    exit()

# -------------------------------
# 2. FILE PATHS (UPDATED TO CSV)
# -------------------------------
files = {
    "expenditure": r"C:\Users\kvran\OneDrive\Desktop\Travellytics\Datasets\Expenditure_Dataset.csv",
    "crowd_data": r"C:\Users\kvran\OneDrive\Desktop\Travellytics\Datasets\crowd_data.csv"
}

# -------------------------------
# 3. LOAD DATA INTO MYSQL
# -------------------------------
for table_name, file_path in files.items():
    print(f"\n📂 Processing: {table_name}")

    try:
        # Read file directly as CSV
        df = pd.read_csv(file_path)

        # -----------------------
        # Clean column names GENTLY 
        # (Removes accidental spaces but keeps capitalizations)
        # -----------------------
        df.columns = df.columns.str.strip()

        # Drop entirely empty rows
        df.dropna(how="all", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # -----------------------
        # Load into MySQL
        # -----------------------
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="replace",
            index=False
        )

        print(f"✅ Successfully loaded '{table_name}'")

    except FileNotFoundError:
        print(f"❌ Error: The file path was not found: {file_path}")
    except Exception as e:
        print(f"❌ Error in '{table_name}': {e}")

# -------------------------------
# DONE
# -------------------------------
print("\n🎉 All CSV datasets loaded successfully!")