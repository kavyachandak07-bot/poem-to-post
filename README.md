# ✨ Poem to Post

> Turn poetry into visual stories.

**Poem to Post** is an AI-powered web app that transforms a poem into a complete, shareable visual post.

I built it for a friend who writes poetry but finds it difficult to turn her poems into visual social-media content. The goal was to take the creative work she already has, her poem, and help turn it into something she can share visually.

---

## 💡 What It Does

Give Poem to Post a poem, and it:

- 🧠 Understands the poem's emotional tone
- 🎭 Identifies its dominant mood
- ✍️ Generates an Instagram caption
- #️⃣ Generates relevant hashtags
- 🎨 Creates a detailed visual concept inspired by the poem
- 🖼️ Generates an AI image based on that concept
- 📜 Places the original poem over the generated artwork
- 📱 Produces a square, shareable visual post

The visual interpretation isn't restricted to landscapes. Depending on the poem, the AI can create an interior, urban scene, symbolic composition, surreal image, human-centered scene, or another visual representation that fits the poem.

---

## 🔄 How It Works

```text
                      POEM
                        │
                        ▼
               ┌─────────────────┐
               │   Gemma 3 4B    │
               │   via Ollama    │
               └────────┬────────┘
                        │
           ┌────────────┼────────────┐
           ▼            ▼            ▼
         Mood        Caption      Hashtags
                        │
                        ▼
                  Visual Prompt
                        │
                        ▼
               ┌─────────────────┐
               │ FLUX.1-schnell  │
               │ Image Generator │
               └────────┬────────┘
                        │
                        ▼
                 AI Background
                        │
                        ▼
               ┌─────────────────┐
               │     Pillow      │
               │ Image + Poetry  │
               └────────┬────────┘
                        │
                        ▼
                    FINAL POST
```

---

## 🤖 AI at the Core

The project uses two open-weight AI models for different parts of the creative pipeline.

### Gemma 3 4B

Gemma runs locally through Ollama and handles language understanding and creative text generation. It generates:

- The poem's dominant mood
- An Instagram caption
- Five relevant hashtags
- A detailed visual prompt for the image generator

### FLUX.1-schnell

FLUX.1-schnell turns Gemma's visual concept into the actual artwork. The image is then combined with the original poem using Pillow.

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Gemma 3 4B | Poem analysis and creative text generation |
| Ollama | Local Gemma inference |
| FLUX.1-schnell | AI image generation |
| Hugging Face Inference Providers | Hosted image inference |
| Python | Application logic |
| Pillow | Image composition and typography |
| Gradio | Web interface |

---

## 🖥️ Interface

The project has a simple Gradio interface:

1. Paste a poem
2. Click **Generate Post**
3. Receive the generated visual post
4. View the mood, caption, and hashtags alongside it

No code needs to be changed to try a different poem.

---

## 🔐 Local + Hosted AI

The language-model portion of the project runs locally through Ollama. Poem analysis, mood detection, caption generation, hashtag generation, and visual prompt generation all happen locally rather than being sent to a hosted language-model API.

The image-generation step uses FLUX.1-schnell through Hugging Face Inference Providers. An `HF_TOKEN` environment variable is required for image generation and is **not** stored in the repository.

---

## 🚀 Running the Project

### Requirements

- Python 3
- [Ollama](https://ollama.com)
- Gemma 3 4B
- A Hugging Face account and token (for image generation)

### Install

Clone the repository and install the Python dependencies:

```bash
git clone https://github.com/kavyachandak07-bot/poem-to-post.git
cd poem-to-post

python3 -m venv .venv
source .venv/bin/activate

pip install requests pillow gradio huggingface_hub
```

Pull Gemma through Ollama:

```bash
ollama pull gemma3:4b
```

Start Ollama:

```bash
ollama serve
```

Set your Hugging Face token:

```bash
export HF_TOKEN="your_token_here"
```

Start the application:

```bash
python app.py
```

Open the local Gradio interface at:

```text
http://127.0.0.1:7860
```

> ⚠️ Never commit your Hugging Face token to the repository.

---

## 🎨 Example Workflow

A poem such as:

> *"It was many and many a year ago,*
> *In a kingdom by the sea..."*

can be interpreted by Gemma as having a nostalgic emotional tone. Gemma then creates:

- A caption
- Relevant hashtags
- A visual concept inspired by the poem

FLUX turns that visual concept into artwork, and the application places the original poem over the generated image.

The result is a complete visual interpretation of the poem rather than simply a generic background with text.

---

## 🌱 Why Open Innovation?

Open-weight models made it possible to experiment with different parts of the creative pipeline independently.

Instead of depending on one closed API for everything, Poem to Post combines:

- A locally running language model
- An open-weight image-generation model
- Local image processing
- An open web interface framework

This makes the architecture more transparent and gives each model a specific role.

Most importantly, it made it possible to build around a real person's creative workflow rather than simply making another generic AI chatbot.

---

## 👤 Built for a Friend

This project was built for a friend who writes poetry.

The problem wasn't that she couldn't write. It was that turning a finished poem into something visual and shareable required an entirely different creative process.

Poem to Post is meant to bridge that gap:

**poem → interpretation → artwork → shareable post**

The idea is to preserve the poem as the heart of the post while using AI to help with the visual and social-media aspects.

---

## 📂 Project Structure

```text
poem-to-post/
│
├── app.py          # Gradio web interface
├── generate.py     # AI pipeline and post generation
├── moods.py        # Mood vocabulary
├── styles.py       # Mood/style relationships
├── .gitignore
└── README.md
```

---

## 🔮 Future Ideas

- Multiple visual styles for the same poem
- User-selectable art styles
- Editable captions and hashtags
- Download/share buttons
- More control over typography and layouts
- Support for multiple poems in one session
- Optional voice narration for generated posts

---

## 🏆 Hacktoberfest 2026

Built for the **Hacktoberfest Weekend Challenge: Build for a Friend**.

The project focuses on using open-source/open-weight AI to solve a small but real creative problem for someone close to me.

---

## 📜 License

This project is open source and available for experimentation and learning.