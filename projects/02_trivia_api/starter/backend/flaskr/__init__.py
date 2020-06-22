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
    response.headers.add("Access-Control-Allow-Methods",'GET, , PUT, POST, DELETE, OPTIONS,')
    response.headers.add("Access-Control-Allow-Headers","Content-Type,Authorization, True")

    return response

  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.order_by(Category.id).all()
    if categories is None:
      abort(404)
      return jsonify({
        'success': False
      })
    categories = { category.id:category.type for category in categories}
    return jsonify({
      'success':True,
      'categories': str(categories)
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


 
  app.route('/questions', methods=['POST'])
  def create_question():
      body = request.get_json()

      if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
          abort(422)

      new_question = body.get('question')
      new_answer = body.get('answer')
      new_difficulty = body.get('difficulty')
      new_category = body.get('category')

      try:
          question = Question(question=new_question, answer=new_answer,
                              difficulty=new_difficulty, category=new_category)
          question.insert()

          return jsonify({
              'success': True,
              'created': question.id,
          })

      except:
          abort(422)
  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  
  @app.route('/questions', methods=['POST'])
  def search_question():
    body = request.get_json()
    search_term = body.get('searchTerm',None)
    if search_term is not None:
      search_questions = Question.query.filter(Question.question.ilike('%'+{search_term}+'%')).all()
      formatted_questions = [question.format() for question in search_questions]
      current_questions = pagination_helper(request, formatted_questions)

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
        'questions': str(current_questions),
        'total_questions': len(current_questions),
        'current_category': None
      })



  
  @app.route('/quizzes', methods=['POST'])
  def quiz():
    body = request.get_json()
    previous_questions = body.get('previous_questions', None)
    cat_id = body['quiz_category']['id']
    if cat_id == 0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category == cat_id).all()
      questions = [question.format() for question in questions]
    if questions is None:
      abort(422)

    else:
      selected = []
      for question in questions:
        if question.id not in previous_questions:
          selected.append(question)
      question = random.choice(selected)
      return jsonify({
        'success':True,
        'question': question
      })

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

    