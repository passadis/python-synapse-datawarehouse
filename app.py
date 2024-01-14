from flask import Flask, render_template, request, redirect, url_for, flash
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
import pyodbc
import os

app = Flask(__name__)
app.secret_key = '1q2w3e4r'  # Required for flashing messages

# For security, consider moving these details to environment variables or use Azure Key Vault
# server = 'xxxxxxx'
# database = 'xxxxxxxxx'
# username = 'xxxxxxxxxxx'
# password = 'xxxxxxxxxxx'

# driver = '{ODBC Driver 18 for SQL Server}'
# connection_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"
key_vault_url = "https://xxxxxxxxx.vault.azure.net/"
credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url=key_vault_url, credential=credential)

server = secret_client.get_secret("server").value
database = secret_client.get_secret("database").value
username = secret_client.get_secret("sqladmin").value
password = secret_client.get_secret("sqlpass").value
driver = '{ODBC Driver 18 for SQL Server}'

connection_str = f"DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        try:
            feline = request.form.get('feline')
            vacation = request.form.get('vacation')
            music = request.form.get('music')
            movement = request.form.get('movement')

            # Insert data into Azure SQL Data Warehouse
            conn = pyodbc.connect(connection_str)
            cursor = conn.cursor()
            query = "INSERT INTO WebPoll (Feline, Vacation, Music, Movement) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (feline, vacation, music, movement))
            conn.commit()
            conn.close()

            flash('Your response has been recorded successfully!', 'success')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')
        
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()
