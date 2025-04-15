from app import app
import os

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    app.run(debug=True)