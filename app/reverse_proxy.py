import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
import httpx
import boto3

app = FastAPI()
S3_BUCKET_NAME = 'butena-public'


async def proxy_request(request: Request):
    s3_client = boto3.client('s3')
    request_url = request.url.path
    subdomain = request_url.split(".")[0]
    file = ''
    if '.html' not in request_url:
        file = 'index.html'

    # Construct the S3 object key based on your requirements
    x = request.url.path.split("/")[-2:]
    y = '/'.join(x)
    s3_key = f"website/{y}"

    try:
        # Get the object from S3
        response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key=s3_key)
    except s3_client.exceptions.NoSuchKey:
        raise HTTPException(status_code=404, detail="Object not found")

    # Return the S3 object's content back to the client
    return StreamingResponse(
        content=response['Body'].iter_chunks(),
        status_code=200,
        headers={"Content-Type": response['ContentType']},
    )

@app.middleware("http")
async def proxy_middleware(request: Request, call_next):
    try:
        return await proxy_request(request)
    except HTTPException as exc:
        return exc

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=9000)