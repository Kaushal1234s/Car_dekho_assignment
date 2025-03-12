import gradio as gr
from components import create_ui

# Create the UI app
app = create_ui()

# Launch the app
app.launch(share=True)
