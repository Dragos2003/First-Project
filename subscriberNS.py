from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from uuid import uuid4
from ..model.agency import Agency
from ..model.newspaper import Newspaper
from ..model.issue import Issue

subscriber_NS = Namespace("subscriber", description="subscriber related operations")

subscriber_model = subscriber_NS.model('SubscriberModel', {
    'subscriber_id': fields.Integer(required=True, help='The unique identifier of a subscriber'),
    'address': fields.String(required=True, help='The address of the subscriber'),
    'name': fields.String(required=True, help='The name of the subscriber')
})

@subscriber_NS.route('')
class SubscriberAPI(Resource):
    @subscriber_NS.marshal_list_with(subscriber_model, envelope='subscribers')
    def get(self):
        return jsonify(Agency.get_instance().all_subscribers())
    
    @subscriber_NS.expect(subscriber_model, validate=True)
    @subscriber_NS.marshal_with(subscriber_model, envelope='subscriber')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name of the subscriber')
        parser.add_argument('address', type=str, required=True, help='Address of the subscriber')
        args = parser.parse_args()
        
        new_subscriber = Agency.get_instance().add_subscriber(
            Agency.get_instance().create_subscriber(subscriber_id=uuid4().int % 100000000,
                                                     name=args['name'],
                                                     address=args['address'])
        )
        return new_subscriber
    
@subscriber_NS.route('/<int:subscriber_id>/issues/<issue_id>/deliver')
class DeliverIssues(Resource):
    def post(self, subscriber_id, issue_id):
        subscriber = Agency.get_instance().get_subscriber(subscriber_id)
        if subscriber is None:
            subscriber_NS.abort(404, "Subscriber {} not found".format(subscriber_id))
        issue = Agency.get_instance().get_issue(issue_id)
        if issue is None:
            subscriber_NS.abort(404, "Issue {} not found".format(issue_id))
        subscriber.deliver_issue(issue)
        return jsonify(subscriber.issues)
    

@subscriber_NS.route('/<int:subscriber_id>/subscribe')
class Subscribe(Resource):
    def post(self, subscriber_id):
        parser = reqparse.RequestParser()
        parser.add_argument('paper_id', type=int, required=True, help='Paper ID')
        args = parser.parse_args()

        success = Agency.get_instance().get_subscriber(subscriber_id).subscribe(Agency.get_instance().get_newspaper(args['paper_id']))
        if success:
            return jsonify("Subscription successful")
        else:
            return jsonify("Subscription failed")
