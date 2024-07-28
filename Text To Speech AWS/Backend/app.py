from flask import Flask
from views.main_views import main
import random

app = Flask(__name__)
app.register_blueprint(main)

# Adding a random filter to the Jinja environment
@app.context_processor
def utility_processor():
    def random_number():
        return str(random.randint(1, 1000000))
    return dict(random=random_number)

if __name__ == '__main__':
    app.run(debug=True)
