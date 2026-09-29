from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from html import escape

from app.services.gemini_flash import generate_image
router = APIRouter()

PANEL_COUNT = 2


@router.get("/", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Comic Craft</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background: #f4f4f4;
                margin: 0;
                padding: 40px;
            }

            .container {
                max-width: 900px;
                margin: auto;
                background: white;
                padding: 30px;
                border-radius: 20px;
                box-shadow: 0 5px 25px rgba(0,0,0,0.1);
            }

            h1 {
                text-align: center;
            }

            label {
                display: block;
                font-weight: bold;
                margin-top: 20px;
                margin-bottom: 8px;
            }

            textarea, select {
                width: 100%;
                box-sizing: border-box;
                padding: 14px;
                font-size: 16px;
                border: 2px solid #ccc;
                border-radius: 10px;
            }

            textarea {
                height: 180px;
                resize: vertical;
            }

            button {
                width: 100%;
                margin-top: 25px;
                padding: 16px;
                border: none;
                border-radius: 10px;
                background: #24245c;
                color: white;
                font-size: 17px;
                cursor: pointer;
            }
        </style>
    </head>

    <body>
        <div class="container">
            <h1>🎨 AI Comic Craft</h1>

            <form method="post" action="/generate">

                <label>Enter your story</label>

                <textarea
                    name="story"
                    placeholder="Write your comic story here..."
                    required
                ></textarea>

                <label>Art Style</label>

                <select name="art_style">
                    <option value="comic book">Comic Book</option>
                    <option value="cartoon">Cartoon</option>
                    <option value="manga">Manga</option>
                    <option value="anime">Anime</option>
                    <option value="realistic">Realistic</option>
                </select>

                <button type="submit">
                    🎨 Generate Comic
                </button>

            </form>
        </div>
    </body>
    </html>
    """


@router.post("/generate", response_class=HTMLResponse)
async def generate_comic(
    story: str = Form(...),
    art_style: str = Form("comic book")
):

    story = story.strip()

    if not story:
        return """
        <h2>Please enter a story.</h2>
        <a href="/">← Go Back</a>
        """

    # EXACTLY 2 PANELS
    panel_descriptions = [
        f"""
        Panel 1: Beginning of the story.

        Create the first important scene from this story:
        {story}

        Show the main character, the setting and the beginning
        of the adventure.
        """,

        f"""
        Panel 2: Continuation and ending of the story.

        Create the second important scene from this story:
        {story}

        Show the main action, ending or final moment of the story.
        """
    ]

    panels = []

    for index, description in enumerate(panel_descriptions, start=1):

        try:
            image_filename = generate_image(description)
            
        except Exception as e:
            print("IMAGE GENERATION ERROR:", e)
            import traceback
            traceback.print_exc()
            image_filename = None

        panels.append({
            "title": f"Panel {index}",
            "description": description,
            "image": image_filename
        })
    panel_html = ""

    for panel in panels:

        if panel["image"]:
            image_html = f"""
            <img
                src="/generated_images/{escape(panel['image'])}"
                alt="{escape(panel['title'])}"
                class="comic-image"
            >
            """
        else:
            image_html = """
            <div class="image-error">
                 Image generation failed
            </div>
            """

        panel_html += f"""
        <div class="panel">

            <h2>{escape(panel["title"])}</h2>

            {image_html}

            <div class="description">
                <strong>Description:</strong>
                <p>{escape(panel["description"])}</p>
            </div>

        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>

    <head>
        <title>Your AI Comic</title>

        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #eeeeee;
                margin: 0;
                padding: 30px;
            }}

            .container {{
                max-width: 950px;
                margin: auto;
            }}

            h1 {{
                text-align: center;
            }}

            .panel {{
                background: white;
                margin-bottom: 30px;
                padding: 25px;
                border-radius: 18px;
                box-shadow: 0 4px 18px rgba(0,0,0,0.12);
            }}

            .panel h2 {{
                color: #24245c;
            }}

            .comic-image {{
                width: 100%;
                max-height: 600px;
                object-fit: contain;
                border-radius: 12px;
                display: block;
                margin-bottom: 20px;
            }}

            .image-error {{
                min-height: 250px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #f3f3f3;
                border: 2px dashed #aaa;
                border-radius: 12px;
                margin-bottom: 20px;
            }}

            .description {{
                font-size: 16px;
                line-height: 1.6;
            }}

            .back {{
                display: block;
                text-align: center;
                background: #24245c;
                color: white;
                text-decoration: none;
                padding: 15px;
                border-radius: 10px;
            }}
        </style>
    </head>

    <body>

        <div class="container">

            <h1>🎨 Your AI Comic</h1>

            {panel_html}

            <a class="back" href="/">
                ← Create Another Comic
            </a>

        </div>

    </body>
    </html>
    """