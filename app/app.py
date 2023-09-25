from flask import Flask, request, render_template
app = Flask(__name__)

posts = []


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
    content = request.form["content"]
    posts.append(content)

    return render_template('index.html', posts=posts)


@app.route("/post/<post_id>", methods=['PUT'])
def update_post(post_id):
    index = int(post_id)
    content = request.json['content']
    posts[index] = content

    return 'ok'


@app.route("/post/<post_id>", methods=['DELETE'])
def delete_post(post_id):
    index = int(post_id)
    del posts[index]

    return 'ok'


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000)
