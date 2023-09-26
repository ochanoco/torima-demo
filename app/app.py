from flask import Flask, request, render_template
app = Flask(__name__)

posts = []

TOKEN = '<proxy_token>'


def authenticate():
    token = request.headers.get('X-Ochanoco-Proxy-Token', '')

    if token != TOKEN:
        return None

    user_id = request.headers.get('X-Ochanoco-UserID', '')
    return user_id


@app.route("/", methods=['GET'])
def show_posts():
    return render_template('index.html', posts=posts)


@app.route("/post/<post_id>", methods=['GET'])
def show_post(post_id):
    index = int(post_id)
    post = posts[index]

    return render_template('post.html', post=post)


@app.route("/post", methods=['POST'])
def create_post():
    user_id = authenticate()
    if not user_id:
        return 'ng'

    content = request.form["content"]
    posts.append({
        'content': content,
        'user_id': user_id
    })

    return render_template('index.html', posts=posts)


@app.route("/post/<post_id>", methods=['PUT'])
def update_post(post_id):
    user_id = authenticate()
    index = int(post_id)

    if posts[index]['user_id'] != user_id:
        return 'ng'

    content = request.json['content']

    posts[index]['content'] = content

    return 'ok'


@app.route("/post/<post_id>", methods=['DELETE'])
def delete_post(post_id):
    user_id = authenticate()
    index = int(post_id)

    if posts[index]['user_id'] != user_id:
        return 'ng'

    del posts[index]

    return 'ok'


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000)
