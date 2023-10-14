from flask import Flask, render_template, request
import numpy as np
import pickle

popular_books = pickle.load(open('./model/popular_books.pkl', 'rb'))
data = pickle.load(open('./model/data.pkl', 'rb'))
similarity_scores = pickle.load(open('./model/similarity_scores.pkl', 'rb'))
books = pickle.load(open('./model/books.pkl', 'rb'))
agg_rating_of_all_books = pickle.load(open('./model/agg_rating_of_all_books.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'index.html',
        book_title = list(popular_books['Book-Title']),
        book_author = list(popular_books['Book-Author']),
        image = list(popular_books['Image']),
        votes = list(popular_books['num_ratings']),
        rating = list(popular_books['avg_ratings'])
    )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form['user_input']
    
    index_ar = np.where(data.index == user_input)[0]
    if index_ar.shape[0] == 0:
        df =  popular_books.sample(6)
        recommendation =  df[['Book-Title', 'Book-Author', 'Image', 'num_ratings', 'avg_ratings']].values.tolist()
        return render_template('/recommend.html', data=recommendation)
    index = index_ar[0]
    similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x:x[1], reverse=True)[1:7]

    recommendation = []
    for i in similar_items:
        item = []
        temp = books[books['Book-Title'] == data.index[i[0]]]
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp.drop_duplicates('Book-Title')['Image'].values))

        temp = agg_rating_of_all_books[agg_rating_of_all_books['Book-Title'] == data.index[i[0]]]
        item.append(temp.values[0][1])
        item.append(temp.values[0][2])
        
        recommendation.append(item)
    print( recommendation)


    return render_template('/recommend.html', data=recommendation)

if __name__ == '__main__':
    app.run()