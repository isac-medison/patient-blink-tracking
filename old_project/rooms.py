import os
from fastapi import APIRouter, Request, status
from fastapi.responses import StreamingResponse
from starlette.templating import Jinja2Templates


router = APIRouter()
VIDEO_FILE = "static/video.mp4"
CHUNK_SIZE = 1024 * 1024
templates = Jinja2Templates(directory="routers/templates")

def generate_video_chunks():
    with open(VIDEO_FILE, "rb") as file_object:
        counter = 0
        while True:
            chunk = file_object.read(CHUNK_SIZE)
            if not chunk:
                print("End of chunks")
                break  # "abcdef"
            counter = counter + 1
            print("Chunk Counter", counter)
            yield chunk

@router.get("/")
async def home(request: Request):
    return  templates.TemplateResponse("index.html", context={"request": request,"title":"Stream"})


@router.get("/stream-video")
async def stream_video(request: Request):
    print("123")
    file_size = os.stat(VIDEO_FILE).st_size
    headers = {
        "content-type": "video/mp4",
        "accept-ranges": "bytes",
        "content-encoding": "identity",
        "content-length": str(file_size),
        "content-range": f"bytes 0-{file_size-1}/{file_size}",
    }
    return StreamingResponse(
        content=generate_video_chunks(),
        headers=headers,
        status_code=status.HTTP_206_PARTIAL_CONTENT,
        media_type="video/mp4",
    )
@router.get("/rooms")
async def get_rooms():
    return "hello"


@router.get("/spectate/{room_id}")
async def spectate(room_id: int):
    return f"room {room_id}"


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
    contents = await file.read()
    np_arr = np.frombuffer(contents, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # ✅ Apply your OpenCV logic here
    processed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, processed = cv2.imencode(".jpg", processed)

    return Response(content=processed.tobytes(), media_type="image/jpeg")