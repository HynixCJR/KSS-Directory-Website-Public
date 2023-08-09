from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import glob

app = FastAPI()

# For some reason the server wouldn't run without this code?
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class openAnce():
    """The class for opening announcements and returning them as JSON files"""

    def date(date):
        """Returns the announcement JSON file at the specified date. If there is none, it the function returns 'none'."""
        try:
            anceData = open("announcements/" + date + ".json", "r+")
            ance = anceData.read()
            return json.loads(ance)
        except:
            return "none"

    def batch(num, index):
        """Returns the most recent 'num' number of announcements, at index of 'index'."""
        # Also returns if that index is the last one or not
        # I also call this "batches" in my comments elsewhere
        ances = {}
        all_ance = sorted(glob.glob("announcements/*.json"))
        for i in range(len(all_ance) - num * (index), 0, -1):
            if len(ances) == num:
                break
            else:
                anceData = open(all_ance[i-1], "r+")
                ance = anceData.read()
                ances.update({len(all_ance) - i: ance})
        if len(ances) == 0:
            return "none"
        else:
            if len(all_ance) - num * (index + 1) <= 0:
                ances.update({"Last": True})
            else:
                ances.update({"Last": False})
            return ances

# HTTP get request for an announcement JSON file at specified date
@app.get("/ance/date/{date}")
def getAnce(date: str):
    return openAnce.date(date)

# HTTP request for a batch of JSON files at a specified index.
@app.get("/ance/batch/{num}/{index}")
def getAnceBatch(num: int, index: int):
    # takes in index with start point of 0
    return openAnce.batch(num, index)


@app.get("/anceTotal/{year}/{month}")
def anceTotal(year: str, month: str):
    # Returns the name of the announcements within the provided month.
    # Not the actual JSON files themselves.
    # This is specifically for the calendar preview, so it doesn't return the actual announcements.
    ances = []
    for i in glob.glob("announcements/" + year + month + "*.json"):
        print(i[14:22])
        ances.append(i[14:22])
    return ances