#!/usr/bin/env python3

from flask import request, jsonify
from flask_restful import Resource

import os
from config import create_app, db, api
from models import Book, BookSchema

env = os.getenv("FLASK_ENV", "dev")
app = create_app(env)

class Books(Resource):
    def get(self):
        # Get query parameters with default values
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 5, type=int)
        
        # Use SQLAlchemy's paginate method
        pagination = Book.query.paginate(
            page=page,
            per_page=per_page,
            error_out=False  # Don't raise an error for invalid page numbers
        )
        
        # Serialize the books using the schema
        book_schema = BookSchema()
        books = [book_schema.dump(book) for book in pagination.items]
        
        # Return structured pagination response
        return {
            'page': pagination.page,
            'per_page': pagination.per_page,
            'total': pagination.total,
            'total_pages': pagination.pages,
            'items': books
        }, 200


api.add_resource(Books, '/books', endpoint='books')


if __name__ == '__main__':
    app.run(port=5555, debug=True)