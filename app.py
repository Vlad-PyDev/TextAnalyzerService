from flask import Flask, render_template, request
from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import io
import base64

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    analysis = None
    wordcloud = None
    if request.method == 'POST':
        text = request.form['text']
        blob = TextBlob(text)

        sentiment = blob.sentiment
        analysis = {
            'polarity': round(sentiment.polarity, 2),
            'subjectivity': round(sentiment.subjectivity, 2)
        }

        wc = WordCloud(width=800, height=400, background_color='white').generate(text)
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        wordcloud = base64.b64encode(img.getvalue()).decode()

    return render_template('index.html', analysis=analysis, wordcloud=wordcloud)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)