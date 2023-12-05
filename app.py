from flask import *
import mysql.connector
from auth_decorator import *
import re



app = Flask(__name__)
complaint_email=""
app.secret_key = 'your secret key'
# Replace with your MySQL database connection details
config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Bookish@132755',
    'database': 'reviews',
}


# Create a connection
connection = mysql.connector.connect(**config)

cursor = connection.cursor()


def create_database():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Replace 'your_database' with your desired database name
    database_name = 'reviews'

    # Check if the database exists
    cursor.execute(f"SHOW DATABASES LIKE '{database_name}'")
    result = cursor.fetchone()

    if not result:
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE DATABASE {database_name}")

    cursor.close()
    connection.close()

def create_relations():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    review_realtion = 'review'
    cursor.execute(f"SHOW TABLES LIKE '{review_realtion}'")
    result = cursor.fetchone()
    if not result:
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE TABLE {review_realtion} (id INT AUTO_INCREMENT PRIMARY KEY, brewery_name VARCHAR(255), review VARCHAR(255), rating INT)")
    review_realtion = 'user'
    cursor.execute(f"SHOW TABLES LIKE '{review_realtion}'")
    result = cursor.fetchone()
    if not result:
        # Create the database if it doesn't exist
        cursor.execute(f"CREATE TABLE {review_realtion} (id INT AUTO_INCREMENT PRIMARY KEY, user_id varchar(255), password varchar(255))")
    cursor.close()






@app.route('/search', methods =['GET', 'POST'])
@login_required
def home():
    return render_template('search.html')
    


@app.route('/', methods =['GET', 'POST'])
def login():
    msg = ''
    connection = mysql.connector.connect(**config)
    config['database'] = 'reviews'
    cursor = connection.cursor()
    if request.method == 'POST':
        username = request.form['Email_id']
        password = request.form['password']
        
        cursor.execute("SELECT * FROM user WHERE Email_id = %s AND password = %s", (username, password,))
        account = cursor.fetchone()
        login = False
        if account:
            global complaint_email
            login=True
            complaint_email = username
            msg = 'Logged in successfully !'
            session['user'] = username		
            #print(session['user'])	
            return redirect('/search')
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg = msg)









@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    connection = mysql.connector.connect(**config)
    config['database'] = 'reviews'
    cursor = connection.cursor()
    if request.method == 'POST':
        user_details = request.form
        user_id = user_details['User']
        password = user_details['pas1']
        confirm_password = user_details['pas2']
        contact_no = user_details['number']

        

        cursor.execute('SELECT * FROM User WHERE email_id = %s', (user_id, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', user_id):
            msg = 'Invalid email address !'
        else:
            cursor.execute('INSERT INTO User(Email_ID,name,Contact_No,password) VALUES(%s,%s,%s,%s)', ( user_id,'user',contact_no,password, ))
        msg = 'You have successfully registered !'
        cursor.close()
        return redirect('/')
    #elif request.method == 'POST':
    #	msg = 'Please fill out the form !'
    return render_template('register.html',msg=msg)

 





@app.route('/logout', methods = ['post','get'])
def logout():
    session.pop('user')
    #print(session)
    return redirect('/')
    return redirect('/')

@app.route('/review_change')
def review_change():
    return render_template('review.html')


# Route to display the brewery's current rating and reviews
@app.route('/review', methods=['GET','POST'])
def review(*kwargs):
    # Fetch the current rating and reviews from the database
    connection = mysql.connector.connect(**config)
    config['database'] = 'reviews'
    cursor = connection.cursor()
    try:
        brewery_name = request.form.get('breweryName')
    except:
        brewery_name = kwargs[0]
    print(brewery_name)
    cursor.execute("SELECT AVG(rating) AS avg_rating, COUNT(*) AS num_reviews FROM review where brewery_name = %s", (brewery_name, ))
    result = cursor.fetchone()
    avg_rating = result[0] if result[0] else 0
    num_reviews = result[1]

    # Fetch existing reviews
    cursor.execute("SELECT * FROM review where brewery_name = %s", (brewery_name, ))
    reviews = cursor.fetchall()
    
    return render_template('review.html', brewery_name=brewery_name,avg_rating=avg_rating, num_reviews=num_reviews, reviews=reviews)

# Route to handle new review submissions
@app.route('/submit_review', methods=['POST','GET'])
def submit_review():
    # Get the new review and rating from the form
    connection = mysql.connector.connect(**config)
    config['database'] = 'reviews'
    cursor = connection.cursor()
    review_description = request.form['review_description']
    brewery_name = request.form['breweryName']
    #print(brewery_name)
    rating = int(request.form['rating'])
    
    # Insert the new review into the database
    cursor.execute("INSERT INTO review (brewery_name, review, rating) VALUES (%s, %s,%s)", (brewery_name,review_description, rating))
    connection.commit()
    #review(brewery_name)
    # Redirect back to the main page
    return review(brewery_name)


if __name__ == "__main__":
    # app.run(host ="localhost", port = int("5000"))
    create_database()
    config['database'] = 'reviews'
    create_relations()
    app.run(debug=True)