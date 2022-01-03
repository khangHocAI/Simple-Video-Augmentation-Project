from fastapi import FastAPI, UploadFile, File, requests
from fastapi.responses import FileResponse, RedirectResponse
import cv2
app = FastAPI()


@app.get("/")
async def main():
    return {"Hello": "World!"}

def process_video(file_name):
    # Read video file
    cap = cv2.VideoCapture(file_name)

    # get height, width and frame count of the video
    width, height = (
            int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        )
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter()
    output_file_name = "output.mp4"
    out.open(output_file_name, fourcc, fps, (width, height), True)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            im = frame
            out.write(im)
    except Exception as _:
        # Release resources
        cap.release()
        out.release()
        

    # Release resources
    cap.release()
    out.release()

@app.post("/video_upload")
async def upload_video(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1] in ("mp4", "avi")
    if not extension:
        return "Video must in mp4 or wav format!"
    process_video(file.filename)
    return FileResponse("output.mp4", media_type="video/mp4")

    
