from flask import Flask, jsonify, request

app = Flask(__name__)

posts = [
    {"id": 1, "text": "My first blog post!", "author": "Alice"},
    {"id": 2, "text": "Flask is awesome!", "author": "Bob"},
    {"id": 3, "text": "Learning REST APIs", "author": "Charlie"}
]


@app.route('/posts', methods=['GET'])
def get_posts():
    return jsonify(posts), 200


@app.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)
    if post is None:
        return jsonify({"error": "post not found"}), 404
    return jsonify(post), 200


@app.route('/posts', methods=['POST'])
def add_post():
    data = request.get_json(silent=True) or {}
    if not data.get('text') or not data.get('author'):
        return jsonify({"error": "text and author are required"}), 400
    # Generate a new ID for the post
    new_id = max((post['id'] for post in posts), default=0) + 1
    post = {"id": new_id, "text": data['text'], "author": data['author']}
    posts.append(post)
    return jsonify(post), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
