from fibspov.main.database import init_db
from fibspov.main.app import app
import secrets



if __name__ == "__main__":
    print("🔧 Initialiserer databasen...")
    init_db()
    print("🚀 Starter Flask-applikasjonen...")
    app.run(host="0.0.0.0", port=5000, debug=True)
