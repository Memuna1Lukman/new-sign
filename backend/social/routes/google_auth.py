from fastapi import Depends,APIRouter,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
import uuid
import httpx
from ..database import get_db
from .. import models,oauth2,config

router = APIRouter(
    tags=["Google Auth"],
    prefix="/auth/google"
)


@router.get("/login")
def google_login():
    google_url = (
        "https://accounts.google.com/o/oauth2/v2/auth"
        f"?client_id={config.settings.google_client_id}"
        f"&redirect_uri={config.settings.google_redirect_url}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
    )
    return RedirectResponse(url=google_url)



@router.get("/callback")
async def google_callback(
    code:str = None,
    error:str = None,
    db:Session = Depends(get_db)
):
    if error or not code:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Google authentication failed.")


    async with httpx.AsyncClient() as client:
        token_res = await client.post(
            "https://oauth2.googleapis.com/token",
            data={
                "client_id": config.settings.google_client_id,
                "client_secret": config.settings.google_client_secret,
                "code" : code,
                "grant_type" : "authorization_code",
                "redirect_url" : config.settings.google_redirect_url,
            },
        ) 
        token_data = token_res.json()
        access_token = token_data.get("access_token")

        if not access_token:
            raise HTTPException(status_code=400, detail="Could not fetch Google access token.")

        # Fetch verified profile data

        user_info_res = await client.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_info = user_info_res.json()
        # Security check: Ensure email is verified by Google

        if not user_info.get("email_verified"):
            raise HTTPException(status_code=400, detail="Google account email is unverified.")

        google_id = user_info["id"]
        email = user_info["email"]


        # 1. Search for existing user by google_id or email
        db_user  = db.query(models.User).filter(
            (models.User.google_id == google_id) |( models.User.email == email)
        ).first()

        if not db_user:
            base_username = email.split("@")[0]
            unique_username = f"{base_username}_{uuid.uuid4().hex[:5]}"

            # Create new user without a password

            db_user = models.User(
                email = email,
                username = unique_username,
                google_id = google_id,
                password = None
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)

        else:
            # If user exists from email/password signup, link their google_id
            if not db_user.google_id:
                db_user.google_id = google_id
                db.commit()

        # 2. Issue YOUR app's JWT token using your existing oauth2 helper
    app_jwt = oauth2.create_token(data={"owner_id": str(db_user.id)})
    
    return {
        "access_token": app_jwt,
        "token_type": "bearer"
    }        