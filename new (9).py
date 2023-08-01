from msilib.schema import ComboBox
from tkinter import *
from tkinter import messagebox
import tkinter as tk
from tkinter.tix import Tree
import tkinter.ttk as ttk
import sqlite3



# Function to destroy current top frame
def show_frame(frame_type):

    for child in root.winfo_children():
        if isinstance(child, tk.Toplevel):
            child.destroy()

    # Condition to create new top frame
    if frame_type == "Customer":
        customerClick()
    elif frame_type == "Product":
        productClick()
    elif frame_type == "Sale":
        saleClick()
    elif frame_type == "CusUp":
        customerUpdate()
    elif frame_type == "ProUp":
        productUpdate()
    elif frame_type == "SaleUp":
        saleUpdate()
    elif frame_type == "CusDel":
        customerDelete()
    elif frame_type == "ProDel":
        productDelete()
    elif frame_type == "SaleDel":
        saleDelete()

def check_duplicate(table, column, value):
    # Function to check if the given value exists in the specified column of the table
    cursor.execute(f"SELECT {column} FROM {table} WHERE {column} = ?", (value,))
    result = cursor.fetchone()
    return result is not None

# Function to refresh the Customer and Product function
def refreshTree(tree, data_type):
    if data_type == "Customer":
        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()

        tree.delete(*tree.get_children())

        for row in rows:
            tree.insert("", tk.END, values=row)

    elif data_type == "Product":
        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()

        tree.delete(*tree.get_children())

        for row in rows:
            tree.insert("", tk.END, values=row)


# Function to refresh the Update and Delete of Customer, Product, and Sales Function
def refreshUpDel(tree, combo_box, data_type):
    if data_type == "Customer":
        tree.delete(*tree.get_children()) 

        cursor.execute("SELECT * FROM Customer")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.execute("SELECT CustomerNumber FROM Customer")
        data = cursor.fetchall()
        combo_box['values'] = [item[0] for item in data]

    elif data_type == "Product":
        
        tree.delete(*tree.get_children()) 

        cursor.execute("SELECT * FROM Product")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

        cursor.execute("SELECT ProductID FROM Product")
        data = cursor.fetchall()
        combo_box['values'] = [item[0] for item in data]
    # I specifically used this for delete because I deleted the whole row
    elif data_type == "Sale":
        tree.delete(*tree.get_children()) 
        cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID ")
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)
        
        cursor.execute("SELECT SaleID FROM Sales")
        sale = cursor.fetchall()
        combo_box['values'] = [item[0] for item in sale]

# Function specifically used to refresh the combo box list for Customer and Product in saleClick
def saleRefresh(tree, cus_combox, pro_combobox):
    tree.delete(*tree.get_children())

    cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID ")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)

    cursor.execute("SELECT CustomerNumber FROM Customer")
    data = cursor.fetchall()
    cus_combox['values'] = [item[0] for item in data]

    cursor.execute("SELECT ProductID FROM Product")
    data2 = cursor.fetchall()
    pro_combobox['values'] = [item[0]for item in data2]


# Function specifically used to refresh the combo box list for Customer, Product, and Sales in saleUpdate
def saleUpRefresh(tree, sale_combobox, cus_combox, pro_combobox):
    tree.delete(*tree.get_children())

    cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID ")
    rows = cursor.fetchall()

    for row in rows:
        tree.insert("", tk.END, values=row)
    
    cursor.execute("SELECT SaleId FROM Sales")
    sale = cursor.fetchall()
    sale_combobox['values'] = [item[0] for item in sale]

    cursor.execute("SELECT CustomerNumber FROM Customer")
    customer = cursor.fetchall()
    cus_combox['values'] = [item[0] for item in customer]

    cursor.execute("SELECT ProductID FROM Product")
    product = cursor.fetchall()
    pro_combobox['values'] = [item[0] for item in product]

   
# This function is called when we click "Customer"
def customerClick():
    # We use the TopLevel frame so that It apeears outside of the root frame
    CUSTOMER = tk.Toplevel(root)
    CUSTOMER.title("Customer Details")
    CUSTOMER.geometry("615x500")
    CUSTOMER.resizable(False, False)

    screen_width = CUSTOMER.winfo_screenwidth()
    screen_height = CUSTOMER.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    CUSTOMER.geometry("+%d+%d" % (x_position, y_position))

    label_entry_frame = tk.Frame(CUSTOMER)
    label_entry_frame.pack(padx=10, pady=10)

    customerNumber_label = tk.Label(label_entry_frame, text="Customer Number:")
    customerNumber_label.grid(row=0, column=0, padx=5, pady=5)

    customerNumber_entry = tk.Entry(label_entry_frame)
    customerNumber_entry.grid(row=0, column=1, padx=5, pady=5)

    customerName_label = tk.Label(label_entry_frame, text="Customer Name:")
    customerName_label.grid(row=1, column=0, padx=5, pady=5)

    customerName_entry = tk.Entry(label_entry_frame)
    customerName_entry.grid(row=1, column=1, padx=5, pady=5)

    customerAddress_label = tk.Label(label_entry_frame, text="Customer Address:")
    customerAddress_label.grid(row=2, column=0, padx=5, pady=5)

    customerAddress_entry = tk.Entry(label_entry_frame)
    customerAddress_entry.grid(row=2, column=1, padx=5, pady=5)

    # Function to Insert data to the Customer table
    def add():
        customer_number = customerNumber_entry.get()
        customer_name = customerName_entry.get()
        customer_address = customerAddress_entry.get()

        if not customer_number.isdigit and customer_number():
            messagebox.showerror("Invalid", "Customer Number should contain numbers only")
            return
        
        if check_duplicate("Customer", "CustomerNumber", customer_number):
            messagebox.showerror("Invalid", "Customer Number already exists")
            return
        
        if check_duplicate("Customer", "Name", customer_name):
            messagebox.showerror("Invalid","Customer Name already exists")
            return

        # We are using a tuple of values here
        cursor.execute("INSERT INTO Customer (CustomerNumber, Name, Address) VALUES (?, ?, ?)",
                       (customer_number, customer_name, customer_address))
        conn.commit()
        customerNumber_entry.delete(0, tk.END)
        customerName_entry.delete(0, tk.END)
        customerAddress_entry.delete(0, tk.END)
        refreshTree(tree, "Customer")
        root.event_generate("<<RefreshTotal>>")

    # This is the add button
    customerButton = tk.Button(label_entry_frame, text="Add", command=add)
    customerButton.grid(row=3, column=0, padx=5, pady=5)

    # This function destroys the toplevel frame
    def cancel():
        CUSTOMER.destroy()  # Close the CUSTOMER frame

    cancelButton = tk.Button(label_entry_frame, text="Cancel", command=cancel)
    cancelButton.grid(row=3, column=1, padx=5, pady=5)

    customertree_frame = tk.Frame(CUSTOMER)
    customertree_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Fetch all rows from the database
    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()

    # Pakiayos to hanggang sa dulo ng function nato Mariel, wag moto gamiting ang panget pala nito
    screen_frame = tk.Frame(customertree_frame, bg="white", highlightthickness=1, highlightbackground="black")
    screen_frame.pack(fill=tk.BOTH, expand=True)

    # Create a Treeview widget, this is a table like JTable
    tree = ttk.Treeview(screen_frame, columns=("Customer Number", "Name", "Address"), show="headings", style="Custom.Treeview")
    tree.pack(fill=tk.BOTH, expand=True)

    # Define column headings and set anchor to 'center'
    tree.heading("Customer Number", text="Customer Number", anchor=tk.CENTER)
    tree.heading("Name", text="Name", anchor=tk.CENTER)
    tree.heading("Address", text="Address", anchor=tk.CENTER)


    # Mariel take note eto yung logic para ma center align yung mga data
    for row in rows:
        tree.insert("", tk.END, values=row)
    for column in tree['columns']:
        tree.column(column, anchor=tk.CENTER)


    # This is specifically used to refresh the table after every click
    # Initially populate the Treeview with data
    refreshTree(tree, "Customer")


# This will be called if we click the "Product" button
def productClick():

    # Take note it almost have the same structure as the customerClick function
    # But it inserts data for Product table instead
    PRODUCT = tk.Toplevel(root)
    PRODUCT.title("Product Details")
    PRODUCT.geometry("615x500") 
    PRODUCT.resizable(False, False)

    screen_width = PRODUCT.winfo_screenwidth()
    screen_height = PRODUCT.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    PRODUCT.geometry("+%d+%d" % (x_position, y_position))

    productName_label = tk.Label(PRODUCT, text="Product Name:")
    productName_label.grid(row=1, column=0, padx=0, pady=0)

    productName_entry = tk.Entry(PRODUCT)
    productName_entry.grid(row=1, column=1, padx=0, pady=0)

    productPrice_label = tk.Label(PRODUCT, text="Price:")
    productPrice_label.grid(row=2, column=0, padx=0, pady=0)

    productPrice_entry = tk.Entry(PRODUCT)
    productPrice_entry.grid(row=2, column=1, padx=0, pady=0)

    label_entry_frame = tk.Frame(PRODUCT)
    label_entry_frame.pack(padx=10, pady=10)
    
def is_valid_product_name(product_name, product_name_list):
    if not product_name:
        return False, "Product Name cannot be empty."
    elif product_name.isdigit():
        return False, "Product Name cannot be an integer."
    elif product_name in product_names_list:
        return False, "Product Name is duplicated."
    return True, "Product Name is valid."
    
def is_valid_product_price(product_price, product_prices_list):
    if not product_price:
        return False, "Product Price cannot be empty."
    try:
        float(product_price)
    except ValueError:
        return False, "Product Price cannot contain characters."
    if product_price in product_prices_list:
        return False, "Product Price is duplicated."
    return True, "Product Price is valid."

product_names_list = []  # List to store already entered product names
product_prices_list = []

def add():
    product_name = productName_entry.get()
    product_price = productPrice_entry.get()
        
    is_valid_name, name_message = is_valid_product_name(product_name, product_names_list)
    is_valid_price, price_message = is_valid_product_price(product_price, product_prices_list)

    if is_valid_name and is_valid_price:
        # Add the product to the lists if both name and price are valid
        product_names_list.append(product_name)
        product_prices_list.append(product_price)
        # Do something with the valid product entry here
        print("Product added successfully!")
    else:
        # Show an error message if either name or price is invalid
        print(f"Error: {name_message} {price_message}")
        
        cursor.execute("INSERT INTO Product (ProductName, Price) VALUES (?, ?)", (product_name, product_price))
        conn.commit()
        productName_entry.delete(0, tk.END)
        productPrice_entry.delete(0, tk.END)
        refreshTree(tree, "Product")
        root.event_generate("<<RefreshTotal>>")


    customerButton = tk.Button(PRODUCT, text="Add", command=add)
    customerButton.grid(row=3, column=0, padx=0, pady=5)

    def cancel():
        PRODUCT.destroy()

    cancelButton = tk.Button(PRODUCT, text="Cancel", command=cancel)
    cancelButton.grid(row=3, column=1, padx=0, pady=5)

    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()

    tree = ttk.Treeview(PRODUCT, columns=("Product ID", "Product Name", "Price"), show="headings", style="Custom.Treeview")
    tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")
    
    for row in rows:
        tree.insert("", tk.END, values=row)
    
    refreshTree(tree, "Product")

def saleClick():
    SALE = tk.Toplevel(root)
    SALE.title("Insert Data")
    SALE.geometry("875x525")  
    SALE.resizable(False, False)

    screen_width = SALE.winfo_screenwidth()
    screen_height = SALE.winfo_screenheight()
    x_position = (screen_width - 800) // 2
    y_position = (screen_height - 500) // 2
    SALE.geometry("+%d+%d" % (x_position, y_position))

    customerNumber_label = tk.Label(SALE, text="Customer Number:")
    customerNumber_label.grid(row=1, column=0, padx=10, pady=5)

    customerNumber_label = tk.Label(SALE, text="Customer Name:")
    customerNumber_label.grid(row=2, column=0, padx=10, pady=5)

    productID_label = tk.Label(SALE, text="Product ID:")
    productID_label.grid(row=3, column=0, padx=10, pady=5)

    productName_label = tk.Label(SALE, text="Product Name:")
    productName_label.grid(row=4, column=0, padx=10, pady=5)

    price_label = tk.Label(SALE, text="Price:")
    price_label.grid(row=5, column=0, padx=10, pady=5)

    quantity_label = tk.Label(SALE, text="Quantity:")
    quantity_label.grid(row=6, column=0, padx=10, pady=5)

    # I specifically used combo box to list all data we got from Customer and Product

    customerNumber_combo = ttk.Combobox(SALE, state="readonly")
    customerNumber_combo.grid(row=1, column=1, padx=10, pady=5)

    ProductID_combo = ttk.Combobox(SALE, state="readonly")
    ProductID_combo.grid(row=3, column=1, padx=10, pady=5)

    customerName_entry = tk.Entry(SALE)
    customerName_entry.grid(row=2, column=1, padx=10, pady=5)

    productName_entry = tk.Entry(SALE)
    productName_entry.grid(row=4, column=1, padx=10, pady=5)

    price_entry = tk.Entry(SALE)
    price_entry.grid(row=5, column=1, padx=10, pady=5)

    quantity_entry = tk.Entry(SALE)
    quantity_entry.grid(row=6, column=1, padx=10, pady=5)

    cursor.execute("SELECT CustomerNumber FROM Customer")
    customerNumbers = cursor.fetchall()
    customerNumber_combo['values'] = [item[0] for item in customerNumbers]

    cursor.execute("SELECT ProductID FROM Product")
    productIDs = cursor.fetchall()
    ProductID_combo['values'] = [item[0] for item in productIDs]

    # This function is responsible to autofill the entries based on the results of the combo box 
    def updateBegins():
        selected_customer_number = customerNumber_combo.get()
        selected_product_ID = ProductID_combo.get()

        # Fetch the corresponding customer name and address from the database based on the selected customer number
        cursor.execute("SELECT Name FROM Customer WHERE CustomerNumber = ?", (selected_customer_number,))
        customer_data = cursor.fetchone()

        cursor.execute("SELECT ProductName, Price FROM Product WHERE ProductID = ?", (selected_product_ID,))
        product_data = cursor.fetchone()

        if customer_data:
            # If customer data is found, autofill the entry widgets
            customerName_entry.delete(0, tk.END)
            customerName_entry.insert(0, customer_data[0])  # Insert the customer name

        if product_data:
            productName_entry.delete(0, tk.END)
            productName_entry.insert(0, product_data[0])
            price_entry.delete(0, tk.END)
            price_entry.insert(0, product_data[1])

    beginButton = tk.Button(SALE, text="Fill", command=updateBegins)
    beginButton.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

    # This is specifically used to insert the data to the Sales table, but this doesn't represent the
    # sales display yet
    def add():
        customer_number = customerNumber_combo.get()
        product_ID = ProductID_combo.get()
        quantity = quantity_entry.get()

        # Fetch customer name and product name from the database based on the selected CustomerNumber and ProductID
        cursor.execute("SELECT Customer.Name FROM Customer WHERE CustomerNumber = ?", (customer_number,))
        customer_name = cursor.fetchone()

        cursor.execute("SELECT Product.ProductName, Product.Price FROM Product WHERE ProductID = ?", (product_ID,))
        product_data = cursor.fetchone()

        if customer_name and product_data:
            customer_name = customer_name[0]  # Extract the customer name from the fetched data
            product_name, price = product_data  # Extract product name and price from the fetched data

            # Insert the fetched data into the respective entry widgets
            
            customerName_entry.insert(0, customer_name)
            customerName_entry.delete(0, tk.END)

            
            productName_entry.insert(0, product_name)
            productName_entry.delete(0, tk.END)

            
            price_entry.insert(0, price)
            price_entry.delete(0, tk.END)

            quantity_entry.insert(0, price)
            quantity_entry.delete(0, tk.END)

            # Insert the data into the Sale table
            cursor.execute("INSERT INTO Sales (CustomerNumber, ProductID, Quantity) VALUES (?, ?, ?)",
                        (customer_number, product_ID, quantity))
            conn.commit()

            # Refresh the treeview with the updated data
            saleRefresh(tree, customerNumber_combo, ProductID_combo)
            customerNumber_combo.set("")
            ProductID_combo.set("")
            root.event_generate("<<RefreshTotal>>")

    addButton = tk.Button(SALE, text="Add", command=add)
    addButton.grid(row=7, column=1, columnspan=2, padx=10, pady=10)

    def cancel():
        SALE.destroy()
        
    cancelButton = tk.Button(SALE, text="Cancel", command=cancel)
    cancelButton.grid(row=7, column=2, columnspan=2, padx=10, pady=10)

    # I used the JOIN clause to represent the sales display
    cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID ")
    rows = cursor.fetchall()

    # Mariel from this spot hanggang sa dulo ng saleClick eto yung gagamitin mo para sa lahat
    # maganda gamitin to for me
    frame = tk.Frame(SALE)
    frame.grid(row=8, column=0, columnspan=2, padx=5, pady=5)

    canvas = tk.Canvas(frame, width=780, height=250)  # Adjust the size as needed
    canvas.grid(row=0, column=0, sticky="news")

    # Create vertical scrollbar and attach it to the canvas
    y_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=y_scrollbar.set)

    # Create horizontal scrollbar and attach it to the canvas
    x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    x_scrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")
    canvas.configure(xscrollcommand=x_scrollbar.set)

    # Create a Treeview widget to display the Sale table data
    tree = ttk.Treeview(canvas, columns=("Sale ID", "Customer Number", "Customer Name","Product Name", "Price", "Quantity"),
                        show="headings", style="Custom.Treeview")
    tree.grid(row=0, column=0, sticky="news")

    # Define column headings
    tree.heading("Sale ID", text="Sale ID")
    tree.heading("Customer Number", text="Customer Number")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    # Insert data into the Treeview widget, as you can see we use for-loop to insert data
    for row in rows:
        tree.insert("", tk.END, values=row)

    # Set anchor to 'center' for all columns
    for column in tree['columns']:
        tree.column(column, anchor=tk.CENTER)
    # Create vertical scrollbar

    # Set the Treeview as the scrollable window's child
    canvas.create_window(0, 0, anchor="nw", window=tree)

    # Configure the canvas to scroll with the mouse wheel
    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    # Function to update the horizontal scrollbar
    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    # Bind the function to canvas configure event
    canvas.bind("<Configure>", on_canvas_configure)

# This will be called if you click the "Customer" button of "Update Confimation"
def customerUpdate():
    UPDATE = tk.Toplevel(root)
    UPDATE.title("Customer Update Form")
    UPDATE.geometry("615x500") 
    UPDATE.resizable(False, False)

    screen_width = UPDATE.winfo_screenwidth()
    screen_height = UPDATE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    UPDATE.geometry("+%d+%d" % (x_position, y_position))

    updateCTitle_label = tk.Label(UPDATE, text="UPDATE CUSTOMER")
    updateCTitle_label.grid(row=0, column=0, padx=0, pady=5)

    combo_box = ttk.Combobox(UPDATE, state="readonly")
    combo_box.grid(row=1, column=0, padx=0, pady=5)

    def updateBegins():
        selected_customer_number = combo_box.get()


        cursor.execute("SELECT Name, Address FROM Customer WHERE CustomerNumber = ?", (selected_customer_number,))
        customer_data = cursor.fetchone()

        if customer_data:
            customerName_entry.delete(0, tk.END)
            customerName_entry.insert(0, customer_data[0])
            customerAddress_entry.delete(0, tk.END)
            customerAddress_entry.insert(0, customer_data[1])

    beginUpdate = tk.Button(UPDATE, text="Update", command=updateBegins)
    beginUpdate.grid(row=2, column=0, padx=0, pady=5)

    customerName_label = tk.Label(UPDATE, text="Customer Name:")
    customerName_label.grid(row=4, column=0, padx=0, pady=5)

    customerName_entry = tk.Entry(UPDATE)
    customerName_entry.grid(row=4, column=1, padx=0, pady=5)

    customerAddress_label = tk.Label(UPDATE, text="Customer Address:")
    customerAddress_label.grid(row=5, column=0, padx=0, pady=5)

    customerAddress_entry = tk.Entry(UPDATE)
    customerAddress_entry.grid(row=5, column=1, padx=0, pady=5)

    def update():
        customer_number = combo_box.get()

        customer_name = customerName_entry.get()
        customer_address = customerAddress_entry.get()

        cursor.execute("UPDATE Customer SET Name = ?, Address = ? WHERE CustomerNumber = ?", (customer_name, customer_address, customer_number))
        conn.commit()

        customerName_entry.delete(0, tk.END)
        customerAddress_entry.delete(0, tk.END)
        refreshUpDel(tree, combo_box, "Customer")
        combo_box.set("")
        root.event_generate("<<RefreshTotal>>")
    

    confirmUpdate = tk.Button(UPDATE, text="Confirm", command=update)
    confirmUpdate.grid(row=6, column=0, padx=0, pady=5)

    def cancel():
        UPDATE.destroy()

    cancelUpdate = tk.Button(UPDATE, text="Cancel", command=cancel)
    cancelUpdate.grid(row=6, column=1, padx=0, pady=5)

    cursor.execute("SELECT CustomerNumber FROM Customer")
    data = cursor.fetchall()

    combo_box['values'] = [item[0] for item in data]

    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()

    
    tree = ttk.Treeview(UPDATE, columns=("Customer Number", "Name", "Address"), show="headings", style="Custom.Treeview")
    tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)


    tree.heading("Customer Number", text="Customer Number")
    tree.heading("Name", text="Name")
    tree.heading("Address", text="Address")


    for row in rows:
        tree.insert("", tk.END, values=row)
    
    refreshUpDel(tree, combo_box, "Customer")
    



# This function will be called if we click the "Product" button of "Update Confirmation"
def productUpdate():


    UPDATE = tk.Toplevel(root)
    UPDATE.title("Product Update Form")
    UPDATE.geometry("615x500") 
    UPDATE.resizable(False, False)

    screen_width = UPDATE.winfo_screenwidth()
    screen_height = UPDATE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    UPDATE.geometry("+%d+%d" % (x_position, y_position))

    updateCTitle_label = tk.Label(UPDATE, text="UPDATE PRODUCT")
    updateCTitle_label.grid(row=0, column=0, padx=0, pady=5)

    combo_box = ttk.Combobox(UPDATE, state="readonly")
    combo_box.grid(row=1, column=0, padx=0, pady=5)

    def updateBegins():
        selected_product_ID = combo_box.get()

        cursor.execute("SELECT ProductName, Price FROM Product WHERE ProductID = ?", (selected_product_ID,))
        customer_data = cursor.fetchone()

        if customer_data:
            productName_entry.delete(0, tk.END)
            productName_entry.insert(0, customer_data[0])
            productPrice_entry.delete(0, tk.END)
            productPrice_entry.insert(0, customer_data[1])

    beginUpdate = tk.Button(UPDATE, text="Update", command=updateBegins)
    beginUpdate.grid(row=2, column=0, padx=0, pady=5)


    productName_label = tk.Label(UPDATE, text="Product Name:")
    productName_label.grid(row=4, column=0, padx=0, pady=5)

    productName_entry = tk.Entry(UPDATE)
    productName_entry.grid(row=4, column=1, padx=0, pady=5)

    productPrice_label = tk.Label(UPDATE, text="Price:")
    productPrice_label.grid(row=5, column=0, padx=0, pady=5)

    productPrice_entry = tk.Entry(UPDATE)
    productPrice_entry.grid(row=5, column=1, padx=0, pady=5)

    def update():
        product_ID = combo_box.get()

        product_name = productName_entry.get()
        product_price = productPrice_entry.get()

        cursor.execute("UPDATE Product SET ProductName = ?, Price = ? WHERE ProductID = ?", (product_name, product_price, product_ID))
        conn.commit()
        productName_entry.delete(0, tk.END)
        productPrice_entry.delete(0, tk.END)
        refreshUpDel(Tree, combo_box, "Product")
        combo_box.set("")
        root.event_generate("<<RefreshTotal>>")
    
    confirmUpdate = tk.Button(UPDATE, text="Confirm", command=update)
    confirmUpdate.grid(row=6, column=0, padx=0, pady=5)

    def cancel():
        UPDATE.destroy()

    cancelUpdate = tk.Button(UPDATE, text="Cancel", command=cancel)
    cancelUpdate.grid(row=6, column=1, padx=0, pady=5)

    cursor.execute("SELECT ProductID FROM Product")
    data = cursor.fetchall()

    combo_box['values'] = [item[0] for item in data]

    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()

    tree = ttk.Treeview(UPDATE, columns=("Product ID", "Product Name", "Price"), show="headings", style="Custom.Treeview")
    tree.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")

    for row in rows:
        tree.insert("", tk.END, values=row, tags="center")

    refreshUpDel(tree, ComboBox, "Product")

# This function is used to update the sales table
def saleUpdate():
    UPDATE = tk.Toplevel(root)
    UPDATE.title("Sale Update Form")
    UPDATE.geometry("615x500")
    UPDATE.resizable(False, False)

    screen_width = UPDATE.winfo_screenwidth()
    screen_height = UPDATE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    UPDATE.geometry("+%d+%d" % (x_position, y_position))

    updateSTitle_label = tk.Label(UPDATE, text="UPDATE SALE")
    updateSTitle_label.grid(row=0, column=0, padx=0, pady=5)

    # This is combo box for SaleID, to select which sale to update
    saleID_combo = ttk.Combobox(UPDATE, state="readonly")
    saleID_combo.grid(row=1, column=0, padx=0, pady=5)

    def updateBegins():
        selected_sale_id = saleID_combo.get()

        cursor.execute("SELECT CustomerNumber, ProductID, Quantity FROM Sales WHERE SaleID = ?", (selected_sale_id,))
        sale_data = cursor.fetchone()

        # to autofill the combo box, as of the moment di ko pa alam paano gawing unclickable yung loob
        if sale_data:
            customerNumber_combo.set(sale_data[0])  
            ProductID_combo.set(sale_data[1])
            quantity_entry.delete(0, tk.END)
            quantity_entry.insert(0, sale_data[2])

    beginUpdate = tk.Button(UPDATE, text="Update", command=updateBegins)
    beginUpdate.grid(row=2, column=0, padx=0, pady=5)

    customerNumber_combo = ttk.Combobox(UPDATE, state="readonly")
    customerNumber_combo.grid(row=3, column=0, padx=0, pady=5)


    ProductID_combo = ttk.Combobox(UPDATE, state="readonly")
    ProductID_combo.grid(row=4, column=0, padx=0, pady=5)

    quantity_entry = tk.Entry(UPDATE)
    quantity_entry.grid(row=5, column=0, padx=0, pady=5)

    cursor.execute("SELECT SaleID FROM Sales")
    saleIDs = cursor.fetchall()
    saleID_combo['values'] = [item[0] for item in saleIDs]

    cursor.execute("SELECT CustomerNumber FROM Customer")
    customerNumbers = cursor.fetchall()
    customerNumber_combo['values'] = [item[0] for item in customerNumbers]

    cursor.execute("SELECT ProductID FROM Product")
    productIDs = cursor.fetchall()
    ProductID_combo['values'] = [item[0] for item in productIDs]


    def update():
        sale_id = saleID_combo.get()

        customer_number = customerNumber_combo.get()
        product_id = ProductID_combo.get()

        quantity = quantity_entry.get()

        cursor.execute("UPDATE Sales SET CustomerNumber = ?, ProductID = ?, Quantity = ? WHERE SaleID = ?",
                       (customer_number, product_id, quantity, sale_id))
        conn.commit()

        quantity_entry.delete(0, tk.END)

        saleUpRefresh(tree, saleID_combo, customerNumber_combo, ProductID_combo)
        saleID_combo.set("")
        customerNumber_combo.set("")
        ProductID_combo.set("")
        root.event_generate("<<RefreshTotal>>")

    confirmUpdate = tk.Button(UPDATE, text="Confirm", command=update)
    confirmUpdate.grid(row=6, column=0, padx=0, pady=5)

    def cancel():
        UPDATE.destroy()

    cancelUpdate = tk.Button(UPDATE, text="Cancel", command=cancel)
    cancelUpdate.grid(row=6, column=1, padx=0, pady=5)

    cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID")
    rows = cursor.fetchall()

    frame = tk.Frame(UPDATE)
    frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    canvas = tk.Canvas(frame, width=580, height=250)
    canvas.grid(row=0, column=0, sticky="news")

    y_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    x_scrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")
    canvas.configure(xscrollcommand=x_scrollbar.set)

    tree = ttk.Treeview(canvas, columns=("Sale ID", "Customer Number", "Customer Name","Product Name", "Price", "Quantity"),
                        show="headings", style="Custom.Treeview")
    tree.grid(row=0, column=0, sticky="news")

    tree.heading("Sale ID", text="Sale ID")
    tree.heading("Customer Number", text="Customer Number")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    for row in rows:
        tree.insert("", tk.END, values=row)

    for column in tree['columns']:
        tree.column(column, anchor=tk.CENTER)

    canvas.create_window(0, 0, anchor="nw", window=tree)

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)


def customerDelete():
    DELETE = tk.Toplevel(root)
    DELETE.title("Customer Delete Form")
    DELETE.geometry("615x500") 
    DELETE.resizable(False, False)

    screen_width = DELETE.winfo_screenwidth()
    screen_height = DELETE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    DELETE.geometry("+%d+%d" % (x_position, y_position))

    deleteCTitle_label = tk.Label(DELETE, text="DELETE CUSTOMER")
    deleteCTitle_label.grid(row=0, column=0, padx=0, pady=5)

    combo_box = ttk.Combobox(DELETE, state="readonly")
    combo_box.grid(row=1, column=0, padx=0, pady=5)

    # Self explanatory
    def deleteCustomer():
        customer_number = combo_box.get()

        cursor.execute("DELETE FROM Customer WHERE CustomerNumber = ?", (customer_number,))
        conn.commit()

        refreshUpDel(tree, combo_box, "Customer")
        combo_box.set("")
        root.event_generate("<<RefreshTotal>>")

    # This serves as a confirmation before you delete
    def chooseDeleteType():
        chooseDeleteWindow = tk.Toplevel(root)
        chooseDeleteWindow.title("Confimation")
        chooseDeleteWindow.geometry("350x150")
        chooseDeleteWindow.resizable(False, False)

        screen_width = chooseDeleteWindow.winfo_screenwidth()
        screen_height = chooseDeleteWindow.winfo_screenheight()
        x_position = (screen_width - 300) // 2
        y_position = (screen_height - 150) // 2
        chooseDeleteWindow.geometry("+%d+%d" % (x_position, y_position))

        deleteType_label = tk.Label(chooseDeleteWindow, text="Are you sure?", font=("Helvetica", 14))
        deleteType_label.pack(pady=20)

        def chooseYes():
            chooseDeleteWindow.destroy()
            deleteCustomer()

        
        def chooseNo():
            chooseDeleteWindow.destroy()

        customer_button = tk.Button(chooseDeleteWindow, text="Yes", width=10, command=chooseYes)
        customer_button.pack(side=tk.LEFT, padx=20, pady=10)

        product_button = tk.Button(chooseDeleteWindow, text="No", command=chooseNo)
        product_button.pack(side=tk.RIGHT, padx=20, pady=10)

    
    confirmDelete = tk.Button(DELETE, text="Delete", command=chooseDeleteType)
    confirmDelete.grid(row=2, column=0, padx=0, pady=5)

    def cancel():
        DELETE.destroy()
    
    cancelDelete = tk.Button(DELETE, text="Cancel", command=cancel)
    cancelDelete.grid(row=2, column=1, padx=0, pady=5)

    cursor.execute("SELECT CustomerNumber FROM Customer")
    data = cursor.fetchall()

    combo_box['values'] = [item[0] for item in data]

    cursor.execute("SELECT * FROM Customer")
    rows = cursor.fetchall()

    
    tree = ttk.Treeview(DELETE, columns=("Customer Number", "Name", "Address"), show="headings", style="Custom.Treeview")
    tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    tree.heading("Customer Number", text="Customer Number")
    tree.heading("Name", text="Name")
    tree.heading("Address", text="Address")

    for row in rows:
        tree.insert("", tk.END, values=row)
    
    refreshUpDel(tree, combo_box, "Customer")
    

# This function's functionality is to delete a instance/row of product
def productDelete():
    DELETE = tk.Toplevel(root)
    DELETE.title("Product Delete Form")
    DELETE.geometry("615x500") 
    DELETE.resizable(False, False)

    screen_width = DELETE.winfo_screenwidth()
    screen_height = DELETE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    DELETE.geometry("+%d+%d" % (x_position, y_position))

    deleteCTitle_label = tk.Label(DELETE, text="DELETE PRODUCT")
    deleteCTitle_label.grid(row=0, column=0, padx=0, pady=5)

    combo_box = ttk.Combobox(DELETE, state="readonly")
    combo_box.grid(row=1, column=0, padx=0, pady=5)

    def deleteProduct():
        product_ID = combo_box.get()



        cursor.execute("DELETE FROM Customer WHERE CustomerNumber = ?", (product_ID))
        conn.commit()

        refreshUpDel(tree, combo_box, "Product")
        combo_box.set("")
        root.event_generate("<<RefreshTotal>>")

    def chooseDeleteType():
        chooseDeleteWindow = tk.Toplevel(root)
        chooseDeleteWindow.title("Confimation")
        chooseDeleteWindow.geometry("350x150")
        chooseDeleteWindow.resizable(False, False)

        screen_width = chooseDeleteWindow.winfo_screenwidth()
        screen_height = chooseDeleteWindow.winfo_screenheight()
        x_position = (screen_width - 300) // 2
        y_position = (screen_height - 150) // 2
        chooseDeleteWindow.geometry("+%d+%d" % (x_position, y_position))

        deleteType_label = tk.Label(chooseDeleteWindow, text="Are you sure?", font=("Helvetica", 14))
        deleteType_label.pack(pady=20)

        def chooseYes():
            chooseDeleteWindow.destroy()
            deleteProduct()

        
        def chooseNo():
            chooseDeleteWindow.destroy()

        yes_button = tk.Button(chooseDeleteWindow, text="Yes", width=10, command=chooseYes)
        yes_button.pack(side=tk.LEFT, padx=20, pady=10)

        no_button = tk.Button(chooseDeleteWindow, text="No", command=chooseNo)
        no_button.pack(side=tk.RIGHT, padx=20, pady=10)

    
    confirmDelete = tk.Button(DELETE, text="Delete", command=chooseDeleteType)
    confirmDelete.grid(row=2, column=0, padx=0, pady=5)

    def cancel():
        DELETE.destroy()
    
    cancelDelete = tk.Button(DELETE, text="Cancel", command=cancel)
    cancelDelete.grid(row=2, column=1, padx=0, pady=5)

    cursor.execute("SELECT ProductID FROM Product")
    data = cursor.fetchall()

    combo_box['values'] = [item[0] for item in data]

    cursor.execute("SELECT * FROM Product")
    rows = cursor.fetchall()

    
    tree = ttk.Treeview(DELETE, columns=("Product ID", "Product Name", "Price"), show="headings", style="Custom.Treeview")
    tree.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    tree.heading("Product ID", text="Product ID")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")

    for row in rows:
        tree.insert("", tk.END, values=row)

    refreshUpDel(tree, combo_box, "Customer")

def saleDelete():
    DELETE = tk.Toplevel(root)
    DELETE.title("Sale Update Form")
    DELETE.geometry("615x500")
    DELETE.resizable(False, False)

    screen_width = DELETE.winfo_screenwidth()
    screen_height = DELETE.winfo_screenheight()
    x_position = (screen_width - 200) // 2
    y_position = (screen_height - 300) // 2
    DELETE.geometry("+%d+%d" % (x_position, y_position))

    updateSTitle_label = tk.Label(DELETE, text="DELETE SALE")
    updateSTitle_label.grid(row=0, column=0, padx=0, pady=5)

    saleID_combo = ttk.Combobox(DELETE, state="readonly")
    saleID_combo.grid(row=1, column=0, padx=0, pady=5)

    cursor.execute("SELECT SaleID FROM Sales")
    saleIDs = cursor.fetchall()
    saleID_combo['values'] = [item[0] for item in saleIDs]


    def deleteSales():
        sale_id = saleID_combo.get()

        cursor.execute("DELETE FROM Sales WHERE SaleID = ?", (sale_id,))
        conn.commit()

        refreshUpDel(tree, saleID_combo, "Sale")
        root.event_generate("<<RefreshTotal>>")
        saleID_combo.set("")
    
    def chooseDeleteType():
        chooseDeleteWindow = tk.Toplevel(root)
        chooseDeleteWindow.title("Confimation")
        chooseDeleteWindow.geometry("350x150")
        chooseDeleteWindow.resizable(False, False)

        screen_width = chooseDeleteWindow.winfo_screenwidth()
        screen_height = chooseDeleteWindow.winfo_screenheight()
        x_position = (screen_width - 300) // 2
        y_position = (screen_height - 150) // 2
        chooseDeleteWindow.geometry("+%d+%d" % (x_position, y_position))

        deleteType_label = tk.Label(chooseDeleteWindow, text="Are you sure?", font=("Helvetica", 14))
        deleteType_label.pack(pady=20)

        def chooseYes():
            chooseDeleteWindow.destroy()
            deleteSales()

        
        def chooseNo():
            chooseDeleteWindow.destroy()

        customer_button = tk.Button(chooseDeleteWindow, text="Yes", width=10, command=chooseYes)
        customer_button.pack(side=tk.LEFT, padx=20, pady=10)

        product_button = tk.Button(chooseDeleteWindow, text="No", command=chooseNo)
        product_button.pack(side=tk.RIGHT, padx=20, pady=10)

    confirmDelete = tk.Button(DELETE, text="Confirm Delete", command=chooseDeleteType)
    confirmDelete.grid(row=6, column=0, padx=0, pady=5)

    def cancel():
        DELETE.destroy()

    cancelDelete = tk.Button(DELETE, text="Cancel", command=cancel)
    cancelDelete.grid(row=6, column=1, padx=0, pady=5)

    cursor.execute("SELECT Sales.SaleID, Customer.CustomerNumber, Customer.Name, Product.ProductName, Product.Price, Sales.Quantity FROM Sales JOIN Customer ON Sales.CustomerNumber = Customer.CustomerNumber JOIN Product ON Sales.ProductID = Product.ProductID")
    rows = cursor.fetchall()

    frame = tk.Frame(DELETE)
    frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

    canvas = tk.Canvas(frame, width=580, height=250)
    canvas.grid(row=0, column=0, sticky="news")

    y_scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
    y_scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=y_scrollbar.set)

    x_scrollbar = tk.Scrollbar(frame, orient=tk.HORIZONTAL, command=canvas.xview)
    x_scrollbar.grid(row=1, column=0, columnspan=2, sticky="ew")
    canvas.configure(xscrollcommand=x_scrollbar.set)

    tree = ttk.Treeview(canvas, columns=("Sale ID", "Customer Number", "Customer Name","Product Name", "Price", "Quantity"),
                        show="headings", style="Custom.Treeview")
    tree.grid(row=0, column=0, sticky="news")

    tree.heading("Sale ID", text="Sale ID")
    tree.heading("Customer Number", text="Customer Number")
    tree.heading("Customer Name", text="Customer Name")
    tree.heading("Product Name", text="Product Name")
    tree.heading("Price", text="Price")
    tree.heading("Quantity", text="Quantity")

    for row in rows:
        tree.insert("", tk.END, values=row)

    for column in tree['columns']:
        tree.column(column, anchor=tk.CENTER)

    canvas.create_window(0, 0, anchor="nw", window=tree)

    canvas.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-1 * (event.delta / 120)), "units"))

    def on_canvas_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)

# Used to choose to update between Customer, Product, or Sales
def chooseUpdateType():
    chooseTypeWindow = tk.Toplevel(root)
    chooseTypeWindow.title("Choose Update Type")
    chooseTypeWindow.geometry("350x100")
    chooseTypeWindow.resizable(False, False)

    screen_width = chooseTypeWindow.winfo_screenwidth()
    screen_height = chooseTypeWindow.winfo_screenheight()
    x_position = (screen_width - 300) // 2
    y_position = (screen_height - 150) // 2
    chooseTypeWindow.geometry("+%d+%d" % (x_position, y_position))

    updateType_label = tk.Label(chooseTypeWindow, text="What do you want to update?", font=("Helvetica", 15))
    updateType_label.pack(pady=20)

    def chooseCustomerUpdate():
        chooseTypeWindow.destroy()
        show_frame("CusUp")

    def chooseProductUpdate():
        chooseTypeWindow.destroy()
        show_frame("ProUp")
    
    def chooseSaleUpdate():
        chooseTypeWindow.destroy()
        show_frame("SaleUp")

    def cancel():
        chooseTypeWindow.destroy()

    button_frame = tk.Frame(chooseTypeWindow)
    button_frame.pack()

    customer_button = tk.Button(button_frame, text="Customer", width=10, command=chooseCustomerUpdate)
    customer_button.pack(side=tk.LEFT, padx=5, pady=5)

    product_button = tk.Button(button_frame, text="Product", width=10, command=chooseProductUpdate)
    product_button.pack(side=tk.LEFT, padx=5, pady=5)

    sale_button = tk.Button(button_frame, text="Sale", width=10, command=chooseSaleUpdate)
    sale_button.pack(side=tk.LEFT, padx=5, pady=5)

    cancel_button = tk.Button(button_frame, text="Cancel", width=5, command=cancel)
    cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)


# Same logic but for delete
def chooseDeleteType():
    chooseDeleteWindow = tk.Toplevel(root)
    chooseDeleteWindow.title("Choose Update Type")
    chooseDeleteWindow.geometry("350x100")
    chooseDeleteWindow.resizable(False, False)

    screen_width = chooseDeleteWindow.winfo_screenwidth()
    screen_height = chooseDeleteWindow.winfo_screenheight()
    x_position = (screen_width - 300) // 2
    y_position = (screen_height - 150) // 2
    chooseDeleteWindow.geometry("+%d+%d" % (x_position, y_position))

    deleteType_label = tk.Label(chooseDeleteWindow, text="What do you want to delete?", font=("Helvetica", 15))
    deleteType_label.pack(pady=20)


    def chooseCustomerDelete():
        chooseDeleteWindow.destroy()
        show_frame("CusDel")

    
    def chooseProductDelete():
        chooseDeleteWindow.destroy()
        show_frame("ProDel")
    
    def chooseSaleDelete():
        chooseDeleteWindow.destroy()
        show_frame("SaleDel")

    def cancel():
        chooseDeleteWindow.destroy()
    
    button_frame = tk.Frame(chooseDeleteWindow)
    button_frame.pack()

    customer_button = tk.Button(button_frame, text="Customer", width=10, command=chooseCustomerDelete)
    customer_button.pack(side=tk.LEFT, padx=5, pady=5)

    product_button = tk.Button(button_frame, text="Product", command=chooseProductDelete)
    product_button.pack(side=tk.LEFT, padx=5, pady=5)

    sale_button = tk.Button(button_frame, text="Sale", width=10, command=chooseSaleDelete)
    sale_button.pack(side=tk.LEFT, padx=5, pady=5)

    cancel_button = tk.Button(button_frame, text="Cancel", width=5, command=cancel)
    cancel_button.pack(side=tk.RIGHT, padx=5, pady=5)

# And lastly, for total calculation
def totalDisplay():
    cursor.execute("""
        SELECT
            Product.ProductName,
            SUM(Sales.Quantity) AS TotalQuantity,
            SUM(Sales.Quantity * Product.Price) AS TotalSale
        FROM
            Sales
        JOIN Product ON Sales.ProductID = Product.ProductID
        GROUP BY
            Product.ProductID
    """)

    results = cursor.fetchall()

    # Create a new Tkinter window
    TOTAL = tk.Toplevel(root)
    TOTAL.title("Total Sale")
    TOTAL.geometry("700x300")
    TOTAL.resizable(False, False)

    # Create a Treeview widget
    tree = ttk.Treeview(TOTAL)
    tree["columns"] = ("TotalQuantity", "TotalSale")
    tree.heading("#0", text="Product Name")
    tree.heading("TotalQuantity", text="Total Quantity")
    tree.heading("TotalSale", text="Total Sale")

    def refresh_total():
        nonlocal tree  # Use the same 'tree' variable from the outer function
        tree.delete(*tree.get_children())

        cursor.execute("""
            SELECT
                Product.ProductName,
                SUM(Sales.Quantity) AS TotalQuantity,
                SUM(Sales.Quantity * Product.Price) AS TotalSale
            FROM
                Sales
            JOIN Product ON Sales.ProductID = Product.ProductID
            GROUP BY
                Product.ProductID
        """)
        rows = cursor.fetchall()

        for row in rows:
            product_name, total_quantity, total_sale = row
            tree.insert("", "end", text=product_name, values=(total_quantity, total_sale))

    tree.pack(expand=True, fill=tk.BOTH)

    # Call the refresh_total() function initially after a short delay to populate the Treeview
    TOTAL.after(100, refresh_total)

    # Bind the custom event to the refresh_total() function
    TOTAL.bind("<<RefreshTotal>>", lambda event: refresh_total())

# Connecting the database
conn = sqlite3.connect('DUMMY.db')
cursor = conn.cursor()

# Main application window
root = tk.Tk()
root.geometry("350x450")
root.title("Frame with Button")
root.resizable(False, False)
x = root.winfo_x()
y = root.winfo_y()
root.geometry("+%d+%d" %(x+200,y+200))

main_frame = tk.Frame()
main_frame.pack(fill='both', expand=True, padx=50, pady=50)

customerButton = tk.Button(main_frame, text="Customer", command=lambda: show_frame("Customer"))
customerButton.pack(pady=5)
productButton = tk.Button(main_frame, text="Product", command=lambda: show_frame("Product"))
productButton.pack(pady=5)
saleButton = tk.Button(main_frame, text="Sale", command=lambda: show_frame("Sale"))
saleButton.pack(pady=5)
TotalButton = tk.Button(main_frame, text="Total", command=totalDisplay)
TotalButton.pack(pady=5)
updateButton = tk.Button(main_frame, text="Update", command=chooseUpdateType)
updateButton.pack(pady=5)
deleteButton = tk.Button(main_frame, text="Delete", command=chooseDeleteType)
deleteButton.pack(pady=5)

root.mainloop()

