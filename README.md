Steps to run and test the application locally.

1. Project Setup

	•	Clone the repository:

		git clone <repository_url>
		cd grocery_delivery_app


	•	Set up a virtual environment (optional but recommended):

		python3 -m venv env
		source env/bin/activate  # On macOS/Linux
		env\Scripts\activate  # On Windows


	•	Install dependencies:

		pip install -r requirements.txt



2. Database Setup

	•	Configure the database:
	•	Open settings.py in the Django project folder.
	•	Update the DATABASES setting with your local database configuration (e.g., using SQLite or MySQL).
	•	Create database migrations:

		python manage.py makemigrations
		python manage.py migrate


	•	Create a superuser (optional, for admin access):

		python manage.py createsuperuser



3. Running the Application

	•	Start the Django development server:

		python manage.py runserver


	•	Access the application:
	•	Visit http://127.0.0.1:8000/ in your browser to view the frontend.
	•	Access the Django Admin at http://127.0.0.1:8000/admin to manage items, users, and orders if logged in as a superuser.

4. Testing the API

	•	Using Postman for API Testing:
	•	GET Groceries: Send a GET request to http://127.0.0.1:8000/ to retrieve a list of available grocery items.
	•	POST Add to Cart: Send a POST request to http://127.0.0.1:8000/cart/ with item details 
	•	POST Place Order: Send a POST request to http://127.0.0.1:8000/orders/ to place an order.

5. Testing the Frontend

	•	Interact with the application:
	•	Use the grocery list, add items to the cart, and simulate an order placement.
	•	Verify that all frontend interactions (adding, updating, and removing items from the cart) are functioning properly.
