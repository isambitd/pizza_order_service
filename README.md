# Implementing the following logic using the Django REST framework
# Imagine a pizza ordering services with the following functionality:

	## Order pizzas:
		• It can specify the desired flavors of pizza, the number of pizzas and their size.
		• An order contains information regarding the customer.
		• It can track the status of delivery.
		• It can order the same flavor of pizza but with different sizes multiple times
	## Update an order:
		• It can update the details — flavours, count, sizes — of an order
		• It won't update an order for some statutes of delivery (e.g. delivered).
		• It can change the status of delivery.
	## Remove an order.
	## Retrieve an order:
		• It can retrieve the order by its identifier.
	## List orders:
		• It can retrieve all the orders at once.
		• It supports filtering by status / customer.

# How to run the server

Assuming you have docker installed in your system.

Run `sh start.sh` - to start the server

Run `sh stop.sh` -  to stop the server and clean the environment

Finally you can see the apis in `localhost:8080` in your browser

Additionally, You can see the logs while running start.sh file.

At some step it will run 16 test cases.


Thank you :)
