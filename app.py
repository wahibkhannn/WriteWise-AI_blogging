from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
import  requests
import os
import re
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv
import secrets 
import markdown
load_dotenv()

app = Flask(__name__)
api_key = os.getenv("GEMINI_API_KEY")
app.secret_key = os.getenv("SECRET_KEY")
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

if not api_key:
    # This provides a clear error message if the key is missing
    raise ValueError("Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
genai.configure(api_key=api_key)

# Initialize the Generative Model
# model = genai.GenerativeModel(model_name='models/gemini-2.5-flash')

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',"sqlite:///blog.db")

db = SQLAlchemy(app)

class Blogpost(db.Model):
    __tablename__ = 'blogposts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

@app.route('/')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', datetime=datetime)

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    #Blogpost.query: This starts a query on the Blogpost model.Think as saying:"I want to search in the Blogpost table."
    # .filter_by(id=post_id):
    #This adds a filter condition to the query.It narrows down the results to only the blog post where the id equals post_id.
    # .one():executes the query and expects exactly one result.It's strict —ensures that the result is unambiguous & exactly one.
    # If the query returns:
    # Exactly one row → It returns that row as a Python object.
    # No rows → It raises a NoResultFound exception.
    # More than one row → It raises a MultipleResultsFound exception.
    post_html_content = markdown.markdown(
        post.content, 
        extensions=["fenced_code", "codehilite", "extra"]
    )
    return render_template('post.html', post=post, html_content=post_html_content, now=datetime.now())

@app.route('/add')
def add():
    
    return render_template('add.html')

@app.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    
    post = Blogpost(title=title, 
                    subtitle=subtitle, 
                    author=author, 
                    content=content, 
                    date_posted=datetime.now()
                     )
    flash("Blog post added successfully!", "success")
    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))


@app.route('/models')
def models():
    try:
        return jsonify([m.name for m in genai.list_models()])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/generate_ai', methods=['POST'])
def generate_ai():
    data = request.get_json()
    prompt = data.get('prompt')
    model_name = data.get('model')

    if not prompt or not model_name:
        return jsonify({"error": "No prompt or model provided"}), 400

    try:
        print(f"Using model: {model_name}")
        print(f"Prompt: {prompt}")

        model = genai.GenerativeModel(model_name=model_name)
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(max_output_tokens=650)
        )
        # generated_text = response.candidates[0].content.parts[0].text.strip()
        try:
            raw_text = response.text.strip()
        except:
            try:
                raw_text = response.candidates[0].content.parts[0].text.strip()
            except (IndexError, AttributeError):
                return jsonify({'error': 'Model did not return any content'}), 500
        generated_text = insert_unsplash_images(raw_text)
        # Insert Unsplash images into the raw AI-generated content


        return jsonify({'generated_content': generated_text})
    except Exception as e:
        print("AI generation error:", e)
        return jsonify({'error': f'Failed to generate content: {str(e)}'}), 500


# @app.route('/generate_ai', methods=['POST'])
# def generate_ai():
#     data= request.get_json()
#     prompt = data.get('prompt')
#     model_name = data.get('model') 
#     if not prompt or not model_name:
#         return jsonify({"error": "No prompt or model provided"}), 400
    
#     try:
#         # yha ham dynamically load kar rahe hain our choice of model
#         model = genai.GenerativeModel(model_name=model_name)
#         response = model.generate_content(prompt,
#                         generation_config=genai.types.GenerationConfig(
#                         max_output_tokens=500
#                                           ))
#         generated_text = response.text.strip()
#         return jsonify({'generated_content': generated_text})
#     except Exception as e:
#         print("AI generation error:", e)
#         return jsonify({'error': 'Failed to generate content'}), 500

@app.route('/deletepost', methods=['DELETE','POST'])
def deletepost():
    post_id = request.form.get("post_id")

    post = Blogpost.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    
    return redirect(url_for('index'))

def insert_unsplash_images(text):
    image_prompts = re.findall(r'[\(\[]Image:\s*(.*?)[\)\]]', text)

    for prompt_img in image_prompts:
        query = simplify_prompt(prompt_img)
        print(f"[IMAGE PROMPT FOUND]: '{prompt_img}' → simplified: '{query}'")

        # query = prompt_img.strip() #Clean the prompt — remove any leading/trailing whitespace for safe querying.
        image_url = fetch_unsplash_image_url(query) # This is the Key Call
        #Fetch the image URL from Unsplash API using the cleaned query.
        print(f"[UNSPLASH URL]: {image_url}")
        
        if image_url:
            img_tag = f'<img src="{image_url}" alt="{query}" class="img-fluid my-3 rounded shadow" loading="lazy">'
        else:
            img_tag = f'<div class="alert alert-warning">[Image: {query} — Not Found]</div>'

        pattern = re.compile(r'[\(\[]Image:\s*' + re.escape(prompt_img) + r'[\)\]]', flags=re.IGNORECASE)
        # This regex pattern matches the image prompt in the text, allowing for case-insensitivity and extra whitespace.
        text = pattern.sub(img_tag, text, count=1)
        # for case-insensitive and extra-whitespace handling

    return text

def simplify_prompt(query):
    query = query.lower().strip()
    stopwords = ['the', 'of', 'in', 'his', 'her', 'their', 'with', 'and', 'a', 'an', 'on', 'at', 'for']
    words = [word for word in query.split() if word not in stopwords]
    return ' '.join(words[:5])  # only top 5 meaningful words


def fetch_unsplash_image_url(query):
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "per_page": 2, # Fetch 2 images to ensure we have at least one result
        # and - for random pick among top images
        "client_id": UNSPLASH_ACCESS_KEY
    }

    try:
        response = requests.get(url, params=params)
        #Sends the HTTP GET request to Unsplash.
        if response.status_code == 200:
            # If the request was successful and returned at least 1 result-
            data = response.json()
            if data["results"]:
                return data["results"][0]["urls"]["regular"] # Returns the URL of the first image in the results.
    except Exception as e:
        print("Unsplash API error:", e)

    return None  # fallback image can be used

# def insert_unsplash_images(text):
#     # Match (Image: ...) or [Image: ...]
#     image_prompts = re.findall(r'[\(\[]Image:\s*(.*?)[\)\]]', text)

#     for prompt_img in image_prompts:
#         # Clean up the image prompt
#         prompt_cleaned = " ".join(prompt_img.split()[:5])  # limit to 5 words
#         # Remove extra punctuation and stop words
#         keyword = re.sub(r'\b(?:a|the|and|or|in|on|at|by|with|of)\b', '', prompt_cleaned, flags=re.IGNORECASE)
#         keyword = re.sub(r'[^a-zA-Z0-9 ]+', '', keyword).strip()
#         keyword = "-".join(keyword.lower().split())

#         # Final Unsplash URL
#         unsplash_url = f"https://source.unsplash.com/800x400/?{keyword}"

#         # Final <img> tag
#         img_tag = f'<img src="{unsplash_url}" alt="{prompt_img}" class="img-fluid my-3 rounded shadow" loading="lazy">'

#         # Replace the original image tag
#         text = re.sub(r'[\(\[]Image:\s*' + re.escape(prompt_img) + r'[\)\]]', img_tag, text, count=1)

#     return text




with app.app_context():  
    #used to push the application context manually in Flask
     db.create_all()
if __name__ == '__main__':
    app.run(debug=True)