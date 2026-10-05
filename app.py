import gradio as gr
from generate import generate_post


def run(poem):
    return generate_post(poem)


with gr.Blocks(title="Poem to Post") as demo:

    gr.Markdown(
        """
        # ✨ Poem to Post
        ### Turn your poem into an AI-generated visual post
        """
    )

    poem = gr.Textbox(
        label="Your poem",
        placeholder="Paste your poem here...",
        lines=12
    )

    button = gr.Button(
        "✨ Generate Post",
        variant="primary",
        size="lg"
    )

    with gr.Row():

        image = gr.Image(
            label="Generated Post",
            format="png"
        )

        with gr.Column():

            mood = gr.Textbox(
                label="Mood"
            )

            caption = gr.Textbox(
                label="Caption",
                lines=3
            )

            hashtags = gr.Textbox(
                label="Hashtags",
                lines=2
            )

    button.click(
        fn=run,
        inputs=poem,
        outputs=[image, mood, caption, hashtags]
    )


if __name__ == "__main__":
    demo.launch()