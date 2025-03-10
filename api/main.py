from fastapi import FastAPI

from routes import auth, products, users

app = FastAPI()
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(users.router)


@app.get('/')
def root():
    return {'msg': 'Hello, World!'}


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
