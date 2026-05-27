from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import select

from backend.src.model.user_role import UserRoleClass
from backend.src.model.user import UserClass
from backend.src.database.Session import session
from backend.src.core.config import settings
from backend.src.exceptions.CustomException import AppException
from backend.src.utils.logger import get_logger
from backend.src.router import all
from backend.src.middleware.cors import configure_cors
from backend.src.core.security import Security
from src.model.enum import UserRole

app = FastAPI(title="Certify : The Genome Project Certification Application", version="1.0")
logger = get_logger(__name__)

for router in all:
    app.include_router(router)

configure_cors(app)
@app.get('/')
def health():
    logger.info("The Application is up and Running")
    return {
        'message' : 'Certify : The Genome Project Certification Application is up and running!!!'
    }

@app.exception_handler(AppException)
def app_exception_handler(request, exc : AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success" : False,
            "message" : exc.message
        }
    )

@app.on_event("startup")
def seed_superadmin():
    db = session()
    try:
        new_super_admin = db.execute(
            select(UserRoleClass)
            .where(
                UserRoleClass.user_role==UserRole.SUPERADMIN
            )
        ).scalars().first()
        if not new_super_admin:
            password = Security.hash_password(settings.SUPERADMIN_PASSWORD)
            new_super_admin = UserClass(
                user_title = settings.SUPERADMIN_TITLE,
                user_first_name = settings.SUPERADMIN_FIRST_NAME,
                user_last_name = settings.SUPERADMIN_LAST_NAME,
                user_email = settings.SUPERADMIN_EMAIL,
                user_password = password
            )
            db.add(new_super_admin)
            db.commit()
            db.refresh(new_super_admin)
            logger.info("User_DB Seeded Successfully!!")
            role_superadmin = UserRoleClass(
                user_id = new_super_admin.user_id,
                user_role = "SUPERADMIN"
            )
            db.add(role_superadmin)
            db.commit()
            logger.info("Role_DB Seeded Succesfully!!!")
        else:
            logger.info("Admin Already Exists!!!")
    except Exception as e:
        db.rollback()
        logger.exception("Error creating admin: %s", str(e))

    finally:
        db.close()
