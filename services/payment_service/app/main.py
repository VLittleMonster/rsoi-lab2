import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from database.AppDatabase import AppDatabase
from routers import router as PaymentRouter
from config.config import get_settings

def get_openapi_schema():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers
        )

        for _, path in app.openapi_schema.get('paths').items():
            for _, param in path.items():
                responses = param.get('responses')
                if '422' in responses:
                    del responses['422']

        del app.openapi_schema['components']['schemas']['HTTPValidationError']
        del app.openapi_schema['components']['schemas']['ValidationError']
    return app.openapi_schema


settings = get_settings()
app = FastAPI(title="OpenAPI definition",
              version="v1",
              servers=[
                  {"url": f"http://localhost:{settings['port']}"},
                  {"url": f"http://{settings['external_ip']}:{settings['port']}"}
              ]
              )
app.include_router(PaymentRouter, prefix='')
app.openapi = get_openapi_schema
app_db = AppDatabase.app_db

if __name__ == "__main__":
    app_db.create_all()
    uvicorn.run('main:app',
                host=settings['host'],
                port=settings['port'],
                log_level=settings['log_level'],
                reload=settings['reload'])
