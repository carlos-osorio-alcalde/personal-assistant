from PIL import Image
import io
from fastapi import FastAPI, UploadFile, File
from transformers import BlipProcessor, BlipForConditionalGeneration

# Create FastAPI instance
app = FastAPI(title="Vision Captioning API", version="0.1.0")


@app.get("/")
async def root() -> dict:
    """
    Root of the API
    """
    return {"message": "This is the Vision Captioning API"}

# Load model and processor
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    cache_dir="visioncaptioning/models/",
    local_files_only=True,
)
model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base",
    cache_dir="visioncaptioning/models/",
    local_files_only=True,
)


@app.post("/caption")
async def get_caption_image(image: UploadFile = File(...)) -> str:
    """
    This function returns the caption of the image

    Parameters
    ----------
    image : PIL.Image
        Image to caption

    Returns
    -------
    str
        Caption of the image
    """
    image_data = await image.read()
    image_data = Image.open(io.BytesIO(image_data)).convert("RGB")

    # unconditional image captioning
    inputs = processor(image_data, return_tensors="pt")

    output = model.generate(**inputs)
    return processor.decode(output[0], skip_special_tokens=True)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("visioncaptioning.api:app", host="0.0.0.0", port=5000)
