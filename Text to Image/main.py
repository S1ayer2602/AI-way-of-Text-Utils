from diffusers import StableDiffusionPipeline
import torch
from torch import autocast
import transformers
from flask import Flask, render_template, request
from PIL import Image


app = Flask(__name__)

model_id = "runwayml/stable-diffusion-v1-5"


def image_grid(images, rows, cols):
    assert len(images) == rows * cols

    w, h = images[0].size
    grid = Image.new('RGB', size=(cols * w, rows * h))
    grid_w, grid_h = grid.size

    for i, img in enumerate(images):
        grid.paste(img, box=(i % cols * w, i // cols * h))
    return grid


@app.route('/', methods=['GET', 'POST'])
def generate_image():

    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    prompt = request.form['prompt_input']
    negative_prompt = request.form['negative_prompt_input']
    guidance_scale = request.form['guidance_scale_input']
    inference_steps = request.form['inference_steps_input']
    num_images = request.form['num_images_input']
    num_rows = request.form['rows_input']
    num_cols = request.form['cols_input']
    height = request.form['height_input']
    width = request.form['width_input']

    prompt = "art of a hand showing index finger, 4K, high resolution"
    generator = torch.Generator("cuda").manual_seed(1024)
    images = pipe(
        prompt,
        guidance_scale=float(guidance_scale),
        num_inference_steps=int(inference_steps),
        height=int(height),
        width=int(width),
        negative_prompt=negative_prompt

    ).images
    grid = image_grid(images, rows=num_rows, cols=num_cols)

    grid.save("output.png")


if __name__ == "__main__":
    app.run(debug=True)