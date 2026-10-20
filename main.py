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
    
    # get max id from existing posts and increment by 1 for new post
    id = max((post['id'] for post in posts), default=0) + 1

    post = {"id": id, "text": data['text'], "author": data['author']}
    posts.append(post)
    return jsonify(post), 201


@app.route('/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)

    if post is None:
        return jsonify({"error": "post not found"}), 404
    
    data = request.get_json(silent=True) or {}

    if not data.get('text') or not data.get('author'):
        return jsonify({"error": "text and author are required"}), 400
    
    post['text'] = data['text']
    post['author'] = data['author']
    return jsonify(post), 200


@app.route('/posts/<int:post_id>', methods=['PATCH'])
def patch_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)

    if post is None:
        return jsonify({"error": "post not found"}), 404
    
    data = request.get_json(silent=True) or {}

    if not data.get('text') and not data.get('author'):
        return jsonify({"error": "text or author is required"}), 400
    
    if data.get('text'):
        post['text'] = data['text']

    if data.get('author'):
        post['author'] = data['author']

    return jsonify(post), 200


@app.route('/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    post = next((post for post in posts if post['id'] == post_id), None)

    if post is None:
        return jsonify({"error": "post not found"}), 404
    
    posts.remove(post)
    return jsonify(post), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
