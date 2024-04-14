
from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from uuid import uuid4
from .issuesNS import issue_model
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue
from ..model.editors import Editor
editor_NS = Namespace("editor", description="Editor related operations")

editor_model = editor_NS.model('EditorModel', {
    'editor_id': fields.Integer(required=False,
            help='The unique identifier of an editor'),
    'adress': fields.String(required=True,
            help='The adress of the editor'),
    'name': fields.String(required=True,
            help='The name of the editor')
   })


@editor_NS.route('')
class EditorAPI(Resource):

    @editor_NS.doc(editor_model, description="Add a new editor")
    @editor_NS.expect(editor_model, validate=True)
    @editor_NS.marshal_with(editor_model, envelope='editor')
    def post(self):
        editor_id = uuid4().int % 100000000

        new_editor = Editor(editor_id=editor_id,
                          adress=editor_NS.payload['adress'],
                          name=editor_NS.payload['name'])
        Agency.get_instance().add_editor(new_editor)
        return new_editor
    
    @editor_NS.marshal_list_with(editor_model, envelope='editors')
    def get(self):
        return Agency.get_instance().all_editors()
    
@editor_NS.route('/<int:editor_id>')
class Add_editor_info(Resource):
    @editor_NS.marshal_with(editor_model, envelope='editor')
    def get(self, editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor is None:
            editor_NS.abort(404, "Editor {} not found".format(editor_id))
        return editor

    @editor_NS.expect(editor_model, validate=True)
    @editor_NS.marshal_with(editor_model, envelope='editor')
    def post(self, editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor is None:
            editor_NS.abort(404, "Editor {} not found".format(editor_id))
        editor.adress = editor_NS.payload['adress']
        editor.name = editor_NS.payload['name']
        return editor

    @editor_NS.response(204, "Editor deleted")
    def delete(self, editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor is None:
            editor_NS.abort(404, "Editor {} not found".format(editor_id))
        Agency.get_instance().del_editor(editor)
        return None, 204

@editor_NS.route('/<int:editor_id>/issues')
class EditorIssues(Resource):
    @editor_NS.marshal_list_with(issue_model, envelope='issues')
    def get(self, editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor is None:
            editor_NS.abort(404, "Editor {} not found".format(editor_id))
        return editor.issues