from fastapi import FastAPI
app = FastAPI(title="Random app for deployment in ec2")


@app.post("/")
def welcome():
    return{
        "status_code":200,
        "message" : "Your app is up"
    }

@app.post('/genrate-blog')
def generate_blog(title:str):
    if not title:
        return{
            "statusCode":301,
            "message" : "Enter title to genrate the blog"
        }
    return{
        "statusCode":200,
        "message" : f"This blog {title} is amazing"
    }