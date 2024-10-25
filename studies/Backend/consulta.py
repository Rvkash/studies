import sqlite3
import base64


def fetch_data():
    # Conectar ao banco de dados
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()

    # Executar a consulta para obter usuários e suas fotos
    cursor.execute('''
        SELECT users.id, users.username, users.login, users.start_date, photos.photo
        FROM users
        LEFT JOIN photos ON users.id = photos.user_id
    ''')

    # Obter todos os resultados
    rows = cursor.fetchall()

    # Fechar a conexão
    conn.close()

    return rows


if __name__ == "__main__":
    data = fetch_data()
    for row in data:
        photo_display = row[4]  # Isso é o BLOB da foto

        if photo_display is not None:s
            # Converte o BLOB da foto para Base64
            photo_base64 = base64.b64encode(photo_display).decode('utf-8')
            # Você pode formatar a string para ser usada em uma tag <img> no HTML
            photo_display = f"data:image/jpeg;base64,{photo_base64}"
        else:
            photo_display = 'Nenhuma foto disponível'

        print(f'ID: {row[0]}, Username: {row[1]}, Login: {
              row[2]}, Start Date: {row[3]}, Photo: {photo_display}')
        # Verifique se há fotos no banco de dados
        if not any(row[4] for row in data):
            print("Nenhuma foto encontrada no banco de dados.")
