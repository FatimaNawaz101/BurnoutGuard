import sqlite3
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI #import fastapi framework
from pydantic import BaseModel #this helps define request response structure
from typing import List , Optional #List is a list of items and can be this type or none
from analysis_engine import BurnoutAnalyzer #import our analyzer

#Create the FASTAPI app
#metadata
app=FastAPI(
    title="BurnoutGuard API",
    description="AI-powered burnout detection and wellness analytics",
    version="1.0.0"
)

#Create the analyzer (loads the AI model)
analyzer=BurnoutAnalyzer()

#Database setup
#path to database file in data folder
DB_PATH = Path(__file__).parent.parent / "data" / "burnout_tracker.db"

#This function sets up the database
def init_database():
    """ Create the database and tables if they dont exist """
    #Creates data folder if it doesnt exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    #Connect to database
    conn=sqlite3.connect(DB_PATH) # Get access to database
    cursor=conn.cursor()# Get a helper to run commands

    # Tell helper what to do
    #Create table to store entries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entries(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            text TEXT,
            activities TEXT,
            sleep_hours REAL,
            stress_level INTEGER,
            burnout_score REAL,
            risk_level TEXT,
            emotions TEXT,
            recommendations TEXT,
            insights TEXT     
                   )
        """)
    
    conn.commit() #Save changes
    conn.close() #Close connection
    print("Database initialized!")

    #Initialise database when app starts
init_database() #Run it when app starts

def save_entry(text,activities,sleep_hours,stress_level,result):
    """Save an entry to the database"""
    conn=sqlite3.connect(DB_PATH) #open connection to database
    cursor=conn.cursor()

    #execute this query to add a new row to database
    #? placeholders prevent SQL injection and safely insert values
    cursor.execute("""
        INSERT INTO entries (timestamp, text, activities, sleep_hours, stress_level,
                   burnout_score, risk_level, emotions, recommendations, insights)
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,(
        datetime.now().isoformat(), #current time as string
        text,
        str(activities), # converts list to string for storage
        sleep_hours,
        stress_level,
        result["burnout_score"],
        result["risk_level"],
        str(result["emotions"]),
        str(result["recommendations"]),
        result["insights"]
    ))
    conn.commit()
    conn.close()


#Define what data we expect from the user
#BaseModel from pydantic validates data automatically
#converts type if possible and returns clear errors if data is wrong
class JournalEntry(BaseModel):
    text: Optional[str] = None #journal entry can be empty
    activities: List[str] = [] #List of activities, empty by default
    sleep_hours: float = 7.0 #Hours of sleep
    stress_level: int = 5 #Stress 1-10

#Health check endpoint
#Simple endpoint to verify the API is running.
#This is a decorator which tells FASTAPI when someone visits / return this function
#get if for HTTP GET request used for fetching data
# "Give me the homepage" 
@app.get("/")
#sends back this JSON response
def health_check():
    return {"status": "healthy", "message": "BurnoutGuard API is running"}
    
#Main analyze endpoint
#POST request to /api/analyze
#HTTP POST (used for sending data)
#FastAPI automatically parses the incoming JSON into our 'JournalEntry' model
#"Here's my journal entry, analyze it" 
@app.post("/api/analyze")
def analyze_entry(entry: JournalEntry):
    #Calls our analysis engine
    result = analyzer.analyze(
        text=entry.text,
        activities=entry.activities,
        sleep_hours=entry.sleep_hours,
        stress_level=entry.stress_level
    )
    #this line calls the function save_entry which helps insert data into database
    #we call save entry after analysis
    save_entry(entry.text, entry.activities, entry.sleep_hours, entry.stress_level, result)
    
    return result #Sends back the burnout score, emotions

@app.get("/api/history")
#Sends a get request to fetch history
def get_history():
    """Get all past entries"""
    conn=sqlite3.connect(DB_PATH)
    cursor=conn.cursor()

    #We execute the sql query to get data from table
    #ordered to be newest first and only get last 50 entries
    cursor.execute("""
        SELECT id,timestamp,text,activities,sleep_hours,stress_level,
                   burnout_score,risk_level,emotions,insights
        FROM entries
        ORDER BY timestamp DESC
        LIMIT 50
    """)
    #this gets all matching rows
    rows=cursor.fetchall()
    conn.close()

    #Then we iterate over each row and convert each row into a dictionary and add it to the entries empty list
    entries=[]
    for row in rows:
        entries.append({
            "id": row[0],
            "timestamp" : row[1],
            "text": row[2],
            "activities": row[3],
            "sleep_hours": row[4],
            "stress_level": row[5],
            "burnout_score": row[6],
            "risk_level": row[7],
            "emotions": row[8],
            "insights": row[9]

        })
        #send back a JSON response
    return {"entries": entries, "count": len(entries)}


