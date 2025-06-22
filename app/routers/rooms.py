from fastapi import APIRouter, Request, Path,UploadFile, File
from fastapi.responses import StreamingResponse, Response
from starlette.templating import Jinja2Templates
import cv2
import numpy as np
router = APIRouter()
templates = Jinja2Templates(directory="routers/templates")

@router.get("/")
async def home(request: Request):
    return  templates.TemplateResponse("index.html", context={"request": request})


@router.get("/rooms")
async def get_rooms():
    return "hello"


@router.get("/host/{room_id}")
def video_feed():
    # return the response generated along with the specific media
    # type (mime type)
    # return StreamingResponse(generate())
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")


def generate():
    # grab global references to the output frame and lock variables
    global outputFrame, lock
    # loop over frames from the output stream
    while True:
        # wait until the lock is acquired
        with lock:
            # check if the output frame is available, otherwise skip
            # the iteration of the loop
            if outputFrame is None:
                continue
            # encode the frame in JPEG format
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            # ensure the frame was successfully encoded
            if not flag:
                continue
        # yield the output frame in the byte format
        yield b''+bytearray(encodedImage)



@router.post("/process-frame")
async def process_frame(file: UploadFile = File(...)):
    print(123123)
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # ✅ Apply your OpenCV logic here
    processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, processed = cv2.imencode(".jpg", processed)

    return Response(content=processed.tobytes(), media_type="image/jpeg")