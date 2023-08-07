import panel as pn
import emoji
import re
import nltk
import joblib
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# model

lemma = WordNetLemmatizer()
stp_words = stopwords.words('english')
vector = joblib.load('model\\vectorizer.pkl')

def clean(text):
  text = re.sub(r'[^\w\s]','', text, re.UNICODE)
  text = text.lower()
  text = [lemma.lemmatize(token) for token in text.split(' ')]
  text = [lemma.lemmatize(token, 'v') for token in text]
  text = " ".join(word for word in text if word not in stp_words)
  X = vector.transform([text])
  return X

def prediction(text):
    loaded_model = joblib.load('model\\model.joblib')
    X = clean(text)
    Y = loaded_model.predict(X)
    return Y

# app

review_input = pn.widgets.TextInput(placeholder = 'Type here your review (English only)',
                                    value = '')

button = pn.widgets.Button(name = 'Let\'s go!',
                        button_type = 'success',
                        button_style = 'outline')

sentiment = {1: 'positive!', 0: 'negative!'}
static_text = pn.widgets.StaticText(value = 'let me think...')
picture = {1: emoji.emojize(':thumbs_up:'), 0: emoji.emojize(':thumbs_down:')}
emojis = pn.widgets.StaticText(value = emoji.emojize(':thinking_face:'))

def but(event):
    review = review_input.value
    static_text.value = sentiment[prediction(review)[0]]
    emojis.value = picture[prediction(review)[0]]
button.on_click(but)

mainpart = [pn.Column(
            pn.pane.Markdown("### Type your film review (you can write about any film you want). \n My task is to guess which sentiment you implied in your review (positive or negative)."),
            review_input,
            button,
            pn.Spacer(width = 90),
            pn.pane.Markdown('### I think your sentiment was... '),
            pn.Row(static_text, emojis))]

pic = 'neutral_pic.png'

template = pn.template.FastListTemplate(
    logo = pic,
    theme_toggle = False,
    title = 'Film Review Guesser',
    main = mainpart,
    accent_base_color = '#045D5D',
    header_background = '#40E0D0',
    header_color = '#000000',
    collapsed_sidebar = True)

template.servable()

