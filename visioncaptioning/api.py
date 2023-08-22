from PIL import Image
import io
from fastapi import FastAPI, UploadFile, File
from transformers import AutoProcessor, AutoModelForCausalLM

# Create FastAPI instance
app = FastAPI(title="Vision Captioning API", version="0.1.0")


@app.get("/")
async def root() -> dict:
    """
    Root of the API
    """
    return {"message": "This is the Vision Captioning API"}


# Load model and processor
processor = AutoProcessor.from_pretrained(
    "microsoft/git-base-coco", cache_dir="visioncaptioning/models/"
)
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/git-base-coco", cache_dir="visioncaptioning/models/"
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

    # Preprocess image
    pixel_values = processor(
        images=image_data, return_tensors="pt"
    ).pixel_values

    # Generate caption
    generated_ids = model.generate(pixel_values=pixel_values, max_length=50)
    generated_caption = processor.batch_decode(
        generated_ids, skip_special_tokens=True
    )[0]
    return generated_caption


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("visioncaptioning.api:app", host="0.0.0.0", port=5000)
