import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  

  CORS(app)
  
  def pagination_helper(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE 
    end = start + QUESTIONS_PER_PAGE 
    return questions[start:end]
 
  
  @app.after_request
  def after_request(response):
    response.headers.add("Access-Control-Allow-Methods",'GET, PUT, POST, DELETE, OPTIONS,')
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization, True")

    return response

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    if len(categories) == 0:
      abort(404)
    categories = { category.id:category.type for category in categories}
    return jsonify({
      'success':True,
      'categories': categories
    })



  @app.route('/questions')
  def get_all_questions():
    questions = Question.query.order_by(Question.id).all()

    formatted_questions = [question.format()for question in questions]
    current_questions = pagination_helper(request, formatted_questions)
    if len(current_questions) == 0:
      abort(404)
    categories = Category.query.all()
    formatted_categries = {cat.id:cat.type for cat in categories}

    return jsonify({
      'success':True,
      'questions': current_questions,
      'total_questions': len(questions),
      'categories': formatted_categries,
      'current_category': None

    })



  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

    deleted_question = Question.query.get(question_id)
    if deleted_question is None:
      abort(404)
    else:
      deleted_question.delete()
      return jsonify({
        'success':True,
        'deleted_question_id': question_id
      })


 
  @app.route('/questions/new', methods=['POST'])
  def create_question():
    body = request.get_json()
    new_question = body.get('question')
    new_answer = body.get('answer')
    new_category = body.get('category')
    new_difficulty = body.get('difficulty')

    try:
      question = Question(
        question = new_question,
        answer = new_answer,
        category = new_category,
        difficulty = new_difficulty
      )
      question.insert()

      return jsonify({
        'success':True,
        'created':question.id
      })
    except:
      abort(422)
  
  @app.route('/questions/search', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm',None)

    if search_term:
      search_questions = Question.query.filter(Question.question.ilike('%'+search_term+'%')).all()
      formatted_questions = [question.format() for question in search_questions]
      current_questions = pagination_helper(request, formatted_questions)

      if len(current_questions) == 0:
        abort(404)
        
      return jsonify({
        'success':True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'current_category': None
      })
    else:
      abort(404)

  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def getByCategory(id):
    questions = Question.query.filter(Question.category == str(id)).all()
    formatted_questions = [question.format() for question in questions]
    current_questions = pagination_helper(request, formatted_questions)
    if len(current_questions) == 0:
      abort(404)
    else:
      return jsonify({
        'success':True,
        'questions': current_questions,
        'total_questions': len(current_questions),
        'current_category': None
      })



  
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    try:

        body = request.get_json()

        if not ('quiz_category' in body and 'previous_questions' in body):
            abort(422)

        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')

        if category['type'] == 'click':
            available_questions = Question.query.filter(
                Question.id.notin_((previous_questions))).all()
        else:
            available_questions = Question.query.filter_by(
                category=category['id']).filter(Question.id.notin_((previous_questions))).all()

        new_question = available_questions[random.randrange(
            0, len(available_questions))].format() if len(available_questions) > 0 else None

        return jsonify({
            'success': True,
            'question': new_question
        })
    except:
        abort(422)

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'error':404,
      'message': "resource not found"
    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'recource unprocessable'
    }),422
  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    