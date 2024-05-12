from flask import Flask, request, send_file
from flasgger import Swagger
import subprocess
import os

app = Flask(__name__)
swagger = Swagger(app)


@app.route('/get_page', methods=['GET'])
def get_page():
    """
    Сохранение веб-страницы по заданному URL и отправка файла клиенту.

    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
        description: URL веб-страницы для сохранения
    responses:
      200:
        description: Файл успешно сохранен и отправлен
      400:
        description: Необходимо предоставить URL
      500:
        description: Ошибка сервера
    """
    url = request.args.get('url')
    if url:
        try:
            # Создаем имя файла на основе URL
            file_name = url.split("//")[1].replace("/", "_") + ".html"
            # Запускаем SingleFile CLI для сохранения страницы по заданному URL
            subprocess.run(["single-file", url, file_name])
            # Проверяем, существует ли файл
            if os.path.exists(file_name):
                # Отправляем файл обратно клиенту, указывая явно путь к файлу
                return send_file(os.path.abspath(file_name), as_attachment=True)
            else:
                return "Не удалось сохранить файл", 500
        except Exception as e:
            return str(e), 500
    else:
        return "Необходимо предоставить URL", 400


if __name__ == "__main__":
    app.run(debug=True)
