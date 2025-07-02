# ✍️ WriteWise AI

**WriteWise AI** is a modern Flask-based blogging platform powered by Gemini AI and Unsplash API. It allows users to generate creative blog posts using AI prompts, automatically render context-specific images, and share articles via social media. The application features a responsive dark/light mode UI, rich typography, and a beautifully animated design.

---

## 🚀 Features

- 🧠 AI-powered content generation (Gemini models)
- 🖼️ Dynamic image rendering via Unsplash API
- 🌓 Toggleable Dark/Light Mode
- 📱 Mobile responsive with custom UI/UX
- 🔗 Social sharing (Instagram, Twitter, WhatsApp, LinkedIn)
- ⏱️ Reading time estimation
- ✨ Animated loaders and interactive elements
- 🧠 AI model selection via dropdown
- 🧾 Clean, readable typography for blog content

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, Bootstrap, JavaScript
- **AI Integration:** Gemini API (Google Generative AI)
- **Image Integration:** Unsplash Developer API
- **Deployment:** Render

---

## 📂 Project Structure

```
📦 WriteWise-AI/
├── app.py
├── templates/
│   ├── index.html
│   ├── post.html
│   ├── add.html
│   └── ...
├── static/
│   ├── style.css
│   ├── script.js
│   └── bootstrap.min.css
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Setup Instructions

```bash
# Clone the repository
$ git clone https://github.com/your-username/WriteWise-AI.git
$ cd WriteWise-AI

# Create a virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt

# Add your API keys in a `.env` file:
UNSPLASH_ACCESS_KEY=your_unsplash_key
GEMINI_API_KEY=your_gemini_key

# Run the application
$ python app.py
```

---

## 💡 Usage

- Go to `/add` to create a new blog.
- Enter title, subtitle, author, and AI prompt.
- Click on **Generate with AI✨** to auto-fill content.
- Insert prompts like `(Image: Franz Kafka)` into the content to auto-generate related Unsplash images.
- View blog on homepage with estimated reading time and styled layout.
- Share via built-in social buttons.

---


## 📌 TODO / Future Features

-

---

## 🙌 Acknowledgments

- [Gemini API](https://ai.google.dev/) by Google
- [Unsplash API](https://unsplash.com/developers)
- Bootstrap & Animate.css for design

---

## 👨‍💻 Author

**Mohammad Wahib Ashraf Khan**\
*Developer, Learner, Data Science Aspirant*

Connect with me on [LinkedIn](https://linkedin.com/in/your-profile) | [GitHub](https://github.com/wahibkhannn)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

