from flask import Flask, jsonify, request
import logging
import psycopg2


import azure.functions as func


DB_CONFIG = {
    'host': "aws-0-ap-south-1.pooler.supabase.com",
    'database': "postgres",
    'user': "postgres.jpechybbeebbfsnwlcjr",
    'password': "@Satwikkr055"
}

connection = psycopg2.connect(**DB_CONFIG)
connection.autocommit = True
cursor = connection.cursor()
app = Flask(__name__)

def get_database_row_count():
        cursor.callproc('get_row_count', ['instance'])
        response = cursor.fetchone()
        return response[0]
    
def divide_into_batches(number_of_batches):
    
    if number_of_batches <= 0:
        raise ValueError("Number of batches must be a positive integer.")
    
    batch_size = 100000000 // number_of_batches
    remainder = 100000000 % number_of_batches

    ranges = []
    start = 10000000

    for i in range(number_of_batches):
        end = start + batch_size + (1 if i < remainder else 0)  # Add 1 to some batches to handle remainder
        ranges.append((start, end - 1))
        start = end

    return ranges

def recalulate_password_ranges():
    pass


@app.route('/register', methods=['POST'])
def register_miner():
    data = request.get_json() 

    try:
        instance_name = data['instance_name']
        

        cursor.callproc('register_instance', [instance_name])
        response = cursor.fetchone()

        return jsonify({
            "status": "Success",
            "data": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World from registry service"


if __name__ == '__main__':
    # app.run()
    
    instances = get_database_row_count()
    print(divide_into_batches(instances))