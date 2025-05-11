![PrediTexr-Image-WallPaper](PrediText/Flask/static/image-app/wall.png)
# PrediText

**PrediText** is a multilingual, AI-powered project designed to enhance and automate text translation, grammar correction, word prediction, and autocomplete functionalities. Built with a graphical user interface using **Flask**, this application provides an interactive and intelligent platform for text processing in five major world languages.

## Features

- 🌍 **Translation of sentences into five major world languages**
- 📝 **Grammar correction using advanced AI models**
    - English grammar is corrected using a **text-to-text transformer model** (e.g., T5 or similar).
    - For other languages, grammar correction is performed via the **Sapling API**.
- 🔤 **Smart word autocomplete while typing**
- 🤖 **Next-word prediction using pre-trained GPT models**
- 🖥️ **Web-based graphical user interface with Flask**

## Technologies Used

- Python
- Flask
- Hugging Face Transformers
- OpenAI GPT Models
- Sapling Grammar Correction API
- **`translators` Python library** (for multilingual text translation)
- HTML/CSS (for UI)

## Getting Started

1. Clone the repository:
    ```bash
    git clone https://github.com/mojikarimi/PrediText.git
    cd PrediText
    ```

2. Create a virtual environment and install dependencies:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    pip install -r requirements.txt
    ```
3. Go to the `jupyter-notebook` directory and run the notebook files to train or generate the required models:
    ```bash
    cd jupyter-notebook
    ```

    After running the notebooks, make sure to place the generated model files in their correct locations. For example:

    - The autocomplete suggestion file for Swedish should be placed at:
      ```
      Flask/datasets/auto_word_complete/swedish_words.sug
      ```

    - The Swedish language model (e.g., for prediction or grammar) should be placed at:
      ```
      Flask/models/swedish_model.pkl
      ```

    To verify the exact filenames and directory paths required for each model, refer to the **model loading section** in the `__init__.py` file.
4. Run the application:
    ```bash
   cd PrediText
   flask --app Flask run
    ```

5. Open your browser and go to `http://localhost:5000`.


## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
