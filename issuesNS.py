from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from uuid import uuid4

from ..model.agency import Agency
from ..model.issue import Issue
from .newspaperNS import newspaper_ns


issues_ns = Namespace("issue", description="Issue related operations")
newspaper_ns = Namespace("newspaper", description="Newspaper related operations")
editor_id_ns = Namespace('editor', description='Edit issue')

issue_model = issues_ns.model('IssueModel', {
    'issue_id': fields.Integer(required=False,
            help='The unique identifier of an issue'),
    'releasedate': fields.String(required=True,
            help='The release date of the issue, e.g. 2020-12-31'),
    'num_pages': fields.Integer(required=True,
            help='The number of pages in the issue'),
    'released': fields.Boolean(required=False,
            help='The release status of the issue')
   })

editor_id_model = issues_ns.model('EditorId', {
    'editor_id': fields.Integer(required=True ,
                                help='Editor Id')
})


@issues_ns.route('/issue')
class IssueAPI(Resource):

    @issues_ns.doc(issue_model, description="Add a new issue")
    @issues_ns.expect(issue_model, validate=True)
    @issues_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id):
        issue_id = uuid4().int % 100000000

        new_issue = Issue(issue_id=issue_id,
                          releasedate=issues_ns.payload['releasedate'],
                          num_pages=issues_ns.payload['num_pages'],
                          released=issues_ns.payload['released'])
        Agency.get_instance().get_newspaper(paper_id).add_issue(new_issue)
        return new_issue
    
    @issues_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, paper_id):
        return Agency.get_instance().get_newspaper(paper_id).issues

@issues_ns.route('/issue/<int:issue_id>')
class IssueID(Resource):

    @issues_ns.doc(description="Get a new issue")
    @issues_ns.marshal_with(issue_model, envelope='issue')
    def get(self, paper_id, issue_id):
        search_result = Agency.get_instance().get_newspaper(paper_id).get_issue(issue_id)
        return search_result

@issues_ns.route('/issue/<int:issue_id>/release')
class IssueRelease(Resource):
    @issues_ns.doc(description="Release a new issue")
    @issues_ns.marshal_with(issue_model, envelope='issue')
    def post(self, paper_id, issue_id):
        issue = Agency.get_instance().get_newspaper(paper_id).get_issue(issue_id)
        issue.release_issue()
        return issue

@issues_ns.route('/issue/<int:issue_id>/editor')
class IssueEditor(Resource):
    @issues_ns.doc(description="Specify an editor for an issue")
    @issues_ns.marshal_with(issue_model, envelope='issue')

    def  post(self, paper_id, issue_id):
        issue = Agency.get_instance().get_newspaper(paper_id).get_issue(issue_id)
        issue.set_editor(issues_ns.payload['editor_id'])
        editor = Agency.get_instance().get_editor(issues_ns.payload['editor_id'])
        editor.add_issue(issue)
        return issue
    
@issues_ns.route('/editor/<int:editor_id>/issues')
class EditorIssues(Resource):
    @issues_ns.doc(params={'editor_id': 'An integer representing the editor ID'})
    @issues_ns.marshal_list_with(issue_model, envelope='issues')
    def get(self, editor_id):
        editor = Agency.get_instance().get_editor(editor_id)
        if editor is None:
            issues_ns.abort(404, "Editor {} not found".format(editor_id))
        return editor.issues
    
