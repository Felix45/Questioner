from flask import Blueprint, Flask, jsonify, request
from app.api.v2.models.meetups_model import UsersModel
from app.api.v2.models.comments_model import CommentsModel

commentV2 = Blueprint('comments_v2', __name__, url_prefix='/api/v2')


comments_model = CommentsModel()
users_model = UsersModel()


@commentV2.route('/comments', methods=['POST'])
@users_model.token_required
def add_comment():
    return comments_model.add_comment(request)
