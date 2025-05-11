import os
from flask import Flask
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev',
                            DATABASE=os.path.join(app.instance_path, 'flask.sqlite'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import main,db
    # db
    db.init_app(app)
    # main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')
    # auto complete word
    import pickle
    main.swedish_words = pickle.load(open('Flask/datasets/auto_word_complete/swedish_words.sug', 'rb'))
    main.english_words = pickle.load(open('Flask/datasets/auto_word_complete/english_words.sug', 'rb'))
    main.russian_words = pickle.load(open('Flask/datasets/auto_word_complete/russian_words.sug', 'rb'))
    main.french_words = pickle.load(open('Flask/datasets/auto_word_complete/french_words.sug', 'rb'))
    main.spanish_words = pickle.load(open('Flask/datasets/auto_word_complete/spanish_words.sug', 'rb'))
    main.german_words = pickle.load(open('Flask/datasets/auto_word_complete/german_words.sug', 'rb'))
    # Predictive word
    main.sv_model = pickle.load(open('Flask/models/swedish_model.pkl', 'rb'))
    main.sv_token = pickle.load(open('Flask/models/swedish_tokenizer.pkl', 'rb'))
    main.en_model = pickle.load(open('Flask/models/english_model.pkl', 'rb'))
    main.en_token = pickle.load(open('Flask/models/english_tokenizer.pkl', 'rb'))
    main.ru_model = pickle.load(open('Flask/models/russian_model.pkl', 'rb'))
    main.ru_token = pickle.load(open('Flask/models/russian_tokenizer.pkl', 'rb'))
    main.fr_model = pickle.load(open('Flask/models/french_model.pkl', 'rb'))
    main.fr_token = pickle.load(open('Flask/models/french_tokenizer.pkl', 'rb'))
    main.es_model = pickle.load(open('Flask/models/spanish_model.pkl', 'rb'))
    main.es_token = pickle.load(open('Flask/models/spanish_tokenizer.pkl', 'rb'))
    main.de_model = pickle.load(open('Flask/models/german_model.pkl', 'rb'))
    main.de_token = pickle.load(open('Flask/models/german_tokenizer.pkl', 'rb'))
    # grammar checker
    from happytransformer import TTSettings
    main.happy_tt = pickle.load(open('Flask/models/en_grammar_correction', 'rb'))
    main.args = TTSettings(num_beams=5, min_length=1)
    return app