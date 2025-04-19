import random
import string
from fastapi import Depends, FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.auth import check_auth_user

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/reports")
def get_reports(user: dict[str, str] = Depends(check_auth_user)):
    return {
        "report_id": f"REP{random.randint(100000, 999999)}",
        "report_data": {
            f"param_{i}": "".join(random.choices(string.ascii_uppercase + string.digits, k=6)) for i in range(1, 5)
        },
        "requesting_user_name": user.get("name"),
    }