from flask import Flask
from flask_restful import Resource, Api, reqparse
import werkzeug
import os
from os.path import dirname, abspath
import sqlite3



class PointCloud(Resource):
    TABLE_NAME = 'pointclouds'
    CURRENT_DIR = dirname(abspath(__file__)))
    UPLOAD_DIR = os.path.join(CURRENT_DIR, 'plane-detection-in-point-cloud-data/data/raw')
    FINAL_DIR = os.path.join(CURRENT_DIR, 'plane-detection-in-point-cloud-data/data/final')

    parser = reqparse.RequestParser()
    parser.add_argument('filename',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('file',
        type=werkzeug.datastructures.FileStorage,
        required=True,
        location='files',
        help="This field cannot be left blank!"
    )
    
    def get(self, name):
        item = self.find_by_name(name)
        if item:
            # Copy file from database to file dst
            try:
                self.writeTofile(os.path.join(self.UPLOAD_DIR, item['filename']), item['file'])
                # Run the plane removal script
                exec(open(f"./main.py").read())
                item['file'] = os.path.join(self.FINAL_DIR, item['filename'])
            except:
                {'message': 'Item could not be processed!'}, 500
            return item
        return {'message': 'Item not found'}, 404


    @classmethod
    def writeTofile(cls, filename, data):
        # Convert binary data to proper format and write it on Hard Disk
        with open(filename, 'wb') as file:
            file.write(data)
        print("Stored blob data into: ", filename, "\n")


    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"SELECT * FROM {cls.TABLE_NAME} WHERE name=?"
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'item': {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}

        data = PointCloud.parser.parse_args()

        item = {'filename': name, 'file': data['file']}

        try:
            Item.insert(item)
        except:
            return {"message": "An error occurred inserting the item."}

        return item


    @classmethod
    def convertToBinaryData(cls, filename):
        # Convert digital data to binary format
        with open(filename, 'rb') as file:
            blobData = file.read()
        return blobData
    

    @classmethod
    def insert(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"INSERT INTO {cls.TABLE_NAME} VALUES(?, ?)"
        item['file'] = convertToBinaryData(item['file'])
        cursor.execute(query, (item['filename'], item['file']))

        connection.commit()
        connection.close()


    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"DELETE FROM {self.TABLE_NAME} WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}


    @classmethod
    def update(cls, item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = f"UPDATE {cls.TABLE_NAME} SET price=? WHERE name=?"
        cursor.execute(query, (item['filename'], item['file']))

        connection.commit()
        connection.close()


