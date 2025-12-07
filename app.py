#Webpage built in python built to handle html pages deployed by a docker-compose file, the main webpage is a simple blog that uses post requests to make submissions, all submissions are visible no matter what gets posted. The button that sends the post request will have weak security which will allow website wide defacement. To restore the page simply redeploy the docker compose file.

from flask import Flask, request, render_template_string, redirect

app = Flask(__name__)

posts = []


@app.route('/', methods=['GET', 'POST'])
def blog():
    source_ip = request.remote_addr
    if request.method == 'POST':
        content = request.form.get('content', '')
        admin_tools = '''
            <form method="POST" action="/">
            <input type="hidden" name="action" value="reset">
            <input type="submit" value="Reset Blog">
            </form>
            '''
        ip = request.form.get('ip', '')
        action = request.form.get('action', '')
        
        if action == 'reset' and ip == "127.0.0.1":
            posts.clear()
            return redirect('/')
        elif content != '':
            if ip == "127.0.0.1":
                posts.append("<h1>admin mode</h1>" + admin_tools)
                return redirect('/')
            else:
                posts.append(content)
                return redirect('/')
        else:
            return redirect('/')
        
    
    #Simple blog post web page with a title, text box, and submit button.
    #The page will display all submitted posts below the submission form, which are handled by a Flask backend built in python.
    #Posts are submitted via POST requests and displayed without sanitization, allowing for potential defacement.
    blog_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Simple Blog</title>
    </head>
    <body>
        <h1>Blog Blog Blog...</h1>
        <h3>Author: Hank Vandesteeg</h3>
        <form method="POST" action="/">
            <label for="postContent">Write your post:</label><br>
            <textarea id="postContent" name="content" rows="4" cols="50"></textarea><br>
            <input type="submit" value="Submit Post">
            <input type="hidden" id="ip" name="ip" value="{{ source_ip }}">
        </form>
        <h2>Blog Posts:</h2>
        <br/>
        <div id="posts">
            {% for post in posts %}
                <hr>
                <div class="post">
                    {{ post|safe }}
                </div>
                <hr>
                <br/>
            {% endfor %}
        </div>
    </body>
    </html>
    '''
    return render_template_string(blog_html, posts=posts, source_ip=source_ip)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
