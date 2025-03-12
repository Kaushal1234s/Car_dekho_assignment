import gradio as gr
from handlers import upload_csv, answer_question, generate_graph

def create_ui():
    with gr.Blocks() as app:
        gr.Markdown("# 📊 CSV Question Answering & Visualization (Gradio + Ollama + Pydantic AI)")

        # Section 1: Upload CSV
        with gr.Row():
            file_input = gr.File(label="Upload your CSV file (max 25MB)")
            upload_output = gr.Textbox(label="Upload Status")

        upload_btn = gr.Button("Upload CSV")

        x_col_input = gr.Dropdown(label="X-axis column name", choices=[])
        y_col_input = gr.Dropdown(label="Y-axis column name", choices=[])

        upload_btn.click(
            upload_csv,
            inputs=[file_input],
            outputs=[upload_output, x_col_input, y_col_input]
        )

        gr.Markdown("---")

        # Section 2: Question Answering
        gr.Markdown("## Ask Questions About the Data 📋")
        question_input = gr.Textbox(label="Enter your question")
        answer_btn = gr.Button("Get Answer")
        answer_output = gr.Textbox(label="LLM Answer")

        answer_btn.click(
            answer_question,
            inputs=[question_input],
            outputs=[answer_output]
        )

        gr.Markdown("---")

        # Section 3: Graph Plotting
        gr.Markdown("## Generate Graphs 📈")
        graph_type_input = gr.Dropdown(choices=["Line", "Bar", "Scatter"], label="Select Graph Type")
        graph_btn = gr.Button("Generate Graph")
        graph_output_text = gr.Textbox(label="Graph Status")
        graph_output_img = gr.Image(label="Graph")

        graph_btn.click(
            generate_graph,
            inputs=[x_col_input, y_col_input, graph_type_input],
            outputs=[graph_output_text, graph_output_img]
        )

    return app
