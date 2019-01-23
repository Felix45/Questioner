from flask import Blueprint, Flask, jsonify, request

from app.api.v2.models.comments_model import CommentsModel

commentV2 = Blueprint('comments_v2', __name__, url_prefix='/api/v2')

comments_model = CommentsModel()


@commentV2.route('/comments', methods=['POST'])
def add_comment():
    return comments_model.add_comment(request)
