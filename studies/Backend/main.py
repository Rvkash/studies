from flask import Flask, request, jsonify
from database import UserOperations
import base64
from datetime import datetime

app = Flask(__name__)
user_ops = UserOperations()


@app.route('/register', methods=['POST'])
def register_user():
    try:
        data = request.form
        username = data.get('username')
        login = data.get('login')
        user_id = data.get('user_id')
        # Se não for passado, usa a data atual
        start_date = data.get('start_date')
        photo = request.files.get('photo')  # Captura o arquivo da foto

        if not username or not login:
            return jsonify({"error": "Username and login are required!"}), 400
        
        user_ops.add_user(username, login, start_date)
        user_id = user_ops.get_user_id(username)  
        
        if user_id:
            user_id = user_id[0]

        if photo:
            # Armazena a foto no banco de dados
            # Armazena a foto como BLOB
            user_ops.add_photo(user_id, photo.read())
            # Alternativamente, você pode querer usar `photo.save(...)` se estiver salvando em um arquivo

        return jsonify({"message": "User added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_ops.get_user(user_id)
    if user:
        return jsonify({"user": user}), 200
    else:
        return jsonify({"error": "User not found!"}), 404


# Adicionei a rota para obter fotos
@app.route('/photos/<int:user_id>', methods=['GET'])
def get_photos(user_id):
    photos = user_ops.get_photos(user_id)
    if photos:
        # Converte as fotos em formato base64
        formatted_photos = [
            {"id": photo[0], "photo": base64.b64encode(photo[2]).decode(
                'utf-8')}  # Supondo que photo[2] seja o BLOB
            for photo in photos
        ]
        return jsonify({"photos": formatted_photos}), 200
    else:
        return jsonify({"error": "No photos found for this user!"}), 404


if __name__ == "__main__":
    app.run(debug=True)
