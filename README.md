PROJECT TITLE: Eduzi Enterprise Inventory and Order Management System

VIDEO DEMO:

DESCRIPTION:

In Cs50s final project, I have built a web based inventory and management system with separate interfaces for customers and administrators.

I built this application using Python, Flask, SQLite, HTML, CSS and Jinja.

The system allows customers to browse available products, place orders and receive an order summary.

it also provides an administrator dashboard for managing products and viewing business information.

Unlike a simple ordering website, this project demonstrates database design, session management, CRUD operations, dynamic template and form processing using Flask and SQLite.


                PROBLEM SOLVED

Many small beverage distributors still manage orders manually using notebooks or spreadsheets. This process is slow, error-prone and makes it difficullt to keep track of available products and customer purchases.

This project provides a simple web-based solution that allows products to be managed through an administrator interface while enabling customers to place orders quickly and accurately.


                USER FEATURES

Customer Login using name
View all available products.
Enter quantities for multiple products.
Supports decimal quantities.
Automatic order total calculation.
Live order summary while ordering.
View Complete order summary after submission
Orders stored permanently in SQLite database


                ADMINISTRATOR FEATURES

Secure administrator login.
Dasshboard.
Add new products.
Admin can edit existing product.
Delete products.
Search products.
Products automatically appear on the customer order page.
Customer orders are stored in the database.


                TECHNOLOGIES USED

Python.
Flask.
SQLite.
Cs50 SQLite library.
HTML5.
CSS3.
Jinja2 Template
Flask-Session

                    DATABASE DESIGN

The application uses SQLite with the following tables:

1. Customer table that has an id(integer) and a name(text) column.

2. Products table that stores all available products. It has an id(integer), product_name and price column.

3. Order table  that stores each customers order. It has an id, customer_id, total and order_date column.

4. The order items table that stores every product contained in an order. It has an id, order_id, product_name, unit_price, quantity and subtotal columns.

5. The admins table stores administrator login credentials. Has an id, username and password columns.


                    HOW THIS APPLICATION WORKS

A customer enters their name.

The customer is redirected to the order page.

All products are loaded dynamically from the SQLite database.

The customer enters  quantities for desired products.

The application calculates the total price.

The order is stored in the database.

An order summary is displayed to the customer.


Administrator can log into the dashboard

Add products
Update products
Delete products.
Search products.


 All products changes immidiately appear on the customer order page.


                        FUTURE IMPROVEMENT

POTENTIAL ENHANCEMENT INCLUDE:

Customer authentication with password.
Admiministrator password hashing.
View customer order history.
Generate pdf invoices.
Export sales report to CSV.
Sales analytics dashboard.
Product Categories
Stock quantity management.
Low stock notifications.
Search customer orders.
Sales charts and graphs.
Responsive mobile interface improvement.


                            WHAT I LEARNED


This project strengthened my understanding of:

Flask routing.

Session Management.

SQLite database design.

CRUD operations.
SQLIte Queries.
Jinja Templating.
HTML forms.
CSS styling and responsive layouts.
Building a complete web application from scratch.


                            ACKNOWLEDGEMENTS

This project was developed as my Cs50 Final project using the knowledge and concepts learned throughout Harvard Universitys cs50 course.
