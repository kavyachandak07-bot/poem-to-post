import os
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from huggingface_hub import InferenceClient

from moods import MOOD_WORDS


def analyze_poem(poem_text):
    mood_list = ", ".join(MOOD_WORDS)

    prompt = f"""Read this poem carefully.

Choose EXACTLY ONE dominant mood from this list:
{mood_list}

Then create:
1. A short Instagram caption.
2. Exactly 5 relevant hashtags.
3. A detailed visual description for an AI image generator.

The visual description should describe ONLY the visual scene/image.
It should NOT contain text, letters, words, typography, quotes, captions, or watermarks.

The visual concept should be based on the poem's meaning, imagery, context, metaphors, and emotional tone.
Do NOT assume that the image must be a natural landscape or scenery.

The visual could be:
- a natural landscape
- an urban environment
- an interior
- an abstract or surreal composition
- a symbolic scene
- an object or collection of objects
- a human-centered scene
- a cinematic moment
- or any other visual concept that best represents the poem

Think about:
- setting or visual environment
- lighting and time of day
- colors
- atmosphere
- weather, if relevant
- important objects or details
- metaphorical or symbolic elements
- people or figures, if appropriate
- foreground, middle ground, background
- composition and framing
- artistic or photographic style
- depth and texture

The image should feel like a thoughtful visual interpretation of THIS specific poem,
rather than a generic aesthetic image.

Respond in EXACTLY this format:

MOOD: <one mood from the list>
CAPTION: <1-2 sentence Instagram caption>
HASHTAGS: <exactly 5 hashtags separated by spaces>
VISUAL_PROMPT: <detailed image-generation prompt>

Poem:
{poem_text}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma3:4b",
            "prompt": prompt,
            "stream": False
        }
    )

    response.raise_for_status()
    return response.json()["response"]


def parse_result(result_text):
    mood = ""
    caption = ""
    hashtags = ""
    visual_prompt = ""

    for line in result_text.splitlines():
        line = line.strip()

        if line.startswith("MOOD:"):
            mood = line.replace("MOOD:", "", 1).strip().lower()

        elif line.startswith("CAPTION:"):
            caption = line.replace("CAPTION:", "", 1).strip()

        elif line.startswith("HASHTAGS:"):
            hashtags = line.replace("HASHTAGS:", "", 1).strip()

        elif line.startswith("VISUAL_PROMPT:"):
            visual_prompt = line.replace(
                "VISUAL_PROMPT:", "", 1
            ).strip()

    if mood not in MOOD_WORDS:
        mood = MOOD_WORDS[0]

    return mood, caption, hashtags, visual_prompt


def generate_ai_image(visual_prompt):
    token = os.environ.get("HF_TOKEN")

    if not token:
        raise RuntimeError("HF_TOKEN is not set.")

    client = InferenceClient(api_key=token)

    return client.text_to_image(
        visual_prompt,
        model="black-forest-labs/FLUX.1-schnell"
    )


def get_font(size):
    path = "/System/Library/Fonts/Supplemental/Georgia.ttf"

    if os.path.exists(path):
        return ImageFont.truetype(path, size)

    return ImageFont.load_default()


def wrap_line(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        test = word if not current else current + " " + word
        bbox = draw.textbbox((0, 0), test, font=font)

        if bbox[2] - bbox[0] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)

            current = word

    if current:
        lines.append(current)

    return lines


def create_final_post(background, poem_text):

    # Keep the AI image high quality while fitting the Instagram canvas.
    img = background.convert("RGB").resize(
        (1080, 1080),
        Image.Resampling.LANCZOS
    )

    # Subtle sharpening to compensate for the AI model's soft output.
    img = img.filter(
        ImageFilter.UnsharpMask(
            radius=1.2,
            percent=120,
            threshold=3
        )
    )

    # Slight darkening so the poem remains readable.
    dark = Image.new(
        "RGBA",
        img.size,
        (0, 0, 0, 30)
    )

    img = Image.alpha_composite(
        img.convert("RGBA"),
        dark
    )

    draw = ImageDraw.Draw(img)

    font_size = 48

    while font_size >= 24:

        font = get_font(font_size)
        lines = []

        for original_line in poem_text.splitlines():

            if original_line.strip():

                lines.extend(
                    wrap_line(
                        draw,
                        original_line.strip(),
                        font,
                        760
                    )
                )

        spacing = 14

        total_height = sum(
            draw.textbbox(
                (0, 0),
                line,
                font=font
            )[3]
            -
            draw.textbbox(
                (0, 0),
                line,
                font=font
            )[1]
            +
            spacing
            for line in lines
        )

        if total_height <= 650:
            break

        font_size -= 2

    panel_top = max(
        80,
        (1080 - total_height) // 2 - 45
    )

    panel_bottom = min(
        1000,
        panel_top + total_height + 90
    )

    # Text panel.
    # No Gaussian blur here — keeping everything crisp.
    panel = Image.new(
        "RGBA",
        img.size,
        (0, 0, 0, 0)
    )

    panel_draw = ImageDraw.Draw(panel)

    panel_draw.rounded_rectangle(
        (
            90,
            panel_top,
            990,
            panel_bottom
        ),
        radius=35,
        fill=(0, 0, 0, 105)
    )

    img = Image.alpha_composite(
        img,
        panel
    )

    draw = ImageDraw.Draw(img)

    y = panel_top + 45

    for line in lines:

        bbox = draw.textbbox(
            (0, 0),
            line,
            font=font
        )

        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]

        x = (1080 - width) // 2

        # Text shadow
        draw.text(
            (x + 2, y + 2),
            line,
            font=font,
            fill=(0, 0, 0, 180)
        )

        # Main text
        draw.text(
            (x, y),
            line,
            font=font,
            fill=(255, 255, 255, 245)
        )

        y += height + spacing

    return img.convert("RGB")


def generate_post(poem_text):

    if not poem_text or not poem_text.strip():
        raise ValueError("Please enter a poem.")

    print("Analyzing poem...")

    result = analyze_poem(poem_text)

    mood, caption, hashtags, visual_prompt = parse_result(
        result
    )

    print("Mood:", mood)
    print("Generating AI image...")

    background = generate_ai_image(
        visual_prompt
    )

    final_post = create_final_post(
        background,
        poem_text
    )

    final_post.save(
        "final_post.png"
    )

    with open(
        "post_info.txt",
        "w"
    ) as file:

        file.write(
            f"MOOD: {mood}\n"
        )

        file.write(
            f"CAPTION: {caption}\n"
        )

        file.write(
            f"HASHTAGS: {hashtags}\n"
        )

        file.write(
            f"VISUAL_PROMPT: {visual_prompt}\n"
        )

    return (
        final_post,
        mood,
        caption,
        hashtags
    )