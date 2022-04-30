from flask import Flask, request, render_template, make_response
app = Flask(__name__)

tweets = []
@app.route("/")
def form():
	return render_template("tweet.html")

# vulnerable a XSS
@app.route('/tweet_feed_insecure', methods=['GET', 'POST'])
def tweet_feed_insecure():
	if request.method == 'POST':
		tweet = request.form['tweet']
		tweets.append(tweet)
		html = "<title>Aquí están tus mensajes</title>"
		for tweet in tweets:
			html = html + "<h1>" + tweet + "</h1>"
			html = html + "<a href='" + tweet + "'>&#128147;</a>" 
			return html
# XSS mitigado usando Jinja2 @app.route('/tweet_feed', methods=['GET', 'POST']) def tweet_feed():
	if request.method == 'POST': tweet = request.form['tweet'] 
	tweets.append(tweet)
	response = make_response(render_template('tweet_feed.html', tweets=tweets)) 
	response.headers['Content-Security-Policy'] = "default-src 'self'"
	return response

if   name   == '  main  ':
	app.run(host='0.0.0.0', port=5000, debug=True)