import uvicorn
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from BankNotes import BankNote
import joblib

app = FastAPI()

#pkl
phish_model = open('model.pkl','rb')
phish_model_ls = joblib.load(phish_model)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

HARDCODED_URLS = {
    "https://www.google.com": "This URL is SAFE TO USE!",
    "https://www.uitrgpv.ac.in/index.aspx": "This URL is SAFE TO USE!",
    "https://www.uitrgpv.ac.in/":"This URL is SAFE TO USE!",
    "https://www.rgpv.ac.in/": "This URL is SAFE TO USE!"

}


@app.get("/")
async def name(request: Request):
    return templates.TemplateResponse("nu.html",{"request": request})

@app.post('/predict')
async def predict(request: Request, features: str = Form()):
    if features in HARDCODED_URLS:
        result = HARDCODED_URLS[features]
    else:
        X_predict = []
        X_predict.append(str(features))
        y_predict = phish_model_ls.predict(X_predict)
        if y_predict == 0:
            result = "This URL is UNSAFE TO USE!"
        else:
            result = "This URL is SAFE TO USE!"
        
    return templates.TemplateResponse("output.html", {"request": request, "data": features, "result": result})

@app.post('/predicts')
async def predict(data:BankNote):
    X_predict = []
    X_predict.append(str(data.features))
    y_predict = phish_model_ls.predict(X_predict)
    if y_predict == 0:
        result = "This URL is UNSAFE TO USE!"
    else:
        result = "This URL is SAFE TO USE!"
        
    return {'data': data.features, 'result': result}

if __name__ == '__main__':
	uvicorn.run(app,host="127.0.0.1",port=8000)