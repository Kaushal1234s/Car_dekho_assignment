import pandas as pd
import matplotlib.pyplot as plt
import uuid
import os
from pydantic import BaseModel, ValidationError
import ollama
import gradio as gr

# Global dataframe to store uploaded data
df = pd.DataFrame()

# Create a graphs directory if not exists
os.makedirs("graphs", exist_ok=True)

# ✅ Upload CSV
def upload_csv(file):
    global df
    try:
        df = pd.read_csv(file.name)
        columns = df.columns.tolist()

        default_value = columns[0] if columns else None

        return (
            "✅ Upload successful!",
            gr.Dropdown(choices=columns, value=default_value),
            gr.Dropdown(choices=columns, value=default_value)
        )

    except Exception as e:
        return (
            f"❌ Upload failed: {str(e)}",
            gr.Dropdown(choices=[], value=None),
            gr.Dropdown(choices=[], value=None)
        )

# ✅ Question Answering
class QueryModel(BaseModel):
    question: str

def answer_question(question):
    if df.empty:
        return "❌ Please upload a CSV first."

    try:
        query = QueryModel(question=question)

        data_sample = df.head(50).to_string(index=False)

        prompt = f"""You are a data analyst. Here is a sample dataset:\n{data_sample}\n\nAnswer this question based on the dataset: {query.question}"""

        response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])

        return response['message']['content']

    except ValidationError as e:
        return f"❌ Invalid input: {e}"

# ✅ Graph Generator
def generate_graph(x_column, y_column, graph_type):
    try:
        if df.empty:
            return "❌ CSV not loaded. Please upload a CSV file first.", None

        fig, ax = plt.subplots()

        if graph_type == 'Line':
            ax.plot(df[x_column], df[y_column])
        elif graph_type == 'Bar':
            ax.bar(df[x_column], df[y_column])
        elif graph_type == 'Scatter':
            ax.scatter(df[x_column], df[y_column])
        else:
            return "❌ Invalid graph type selected.", None

        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.set_title(f"{graph_type} graph of {y_column} vs {x_column}")

        plt.tight_layout()

        unique_filename = f"graph_{uuid.uuid4().hex}.png"
        file_path = os.path.join("graphs", unique_filename)

        plt.savefig(file_path)
        plt.close(fig)

        return "✅ Graph Generated Successfully", file_path

    except Exception as e:
        return f"❌ Error: {str(e)}", None
