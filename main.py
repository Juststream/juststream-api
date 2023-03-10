import uvicorn
from mangum import Mangum

from server import app

# Mangum Handler, this is so important
handler = Mangum(app)

if __name__ == "__main__":
    # For development purposes
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
