from flask import Blueprint, redirect, render_template, request, url_for

from gainful.onereach import *
from gainful.helpers import *
from gainful.model_cloudsql import *

search = Blueprint('search', __name__)

@search.route('/', methods=['GET'])
def view():
    """Search for a matching question/answer, given a searchString"""
    query = request.args.get('query')
    result = search_answers(query)
    return ret_ok(data=result)

def search_answers(query):
    """Search for Answer whose question or answer matches the query param

    Args:
        query(string): search string

    Returns:
        dict: answers
    """
    query = "%" + query + "%"
    print "search query %s" % query
    answers = Answer.query.filter((Answer.question.like(query)) | (Answer.answer.like(query))).all()
    results = map(lambda answer: answer.to_dict(), answers)
    multi = False
    questions = ""
    if len(answers) > 1:
        multi = True
        ind = 1
        for result in results:
            questions += "%s) %s\n" % (ind, result['question'])
            result.pop('question', None)
            result.pop('org_id', None)
            result.pop('id', None)
            ind += 1

    response = { 
        'answers' : results,
        'multi': multi,
        'questions': questions
    }

    print "search result %s " % response
    return response