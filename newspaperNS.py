from flask import jsonify
from flask_restx import Namespace, reqparse, Resource, fields
from uuid import uuid4

from ..model.agency import Agency
from ..model.newspaper import Newspaper

newspaper_ns = Namespace("newspaper", description="Newspaper related operations")

paper_model = newspaper_ns.model('NewspaperModel', {
    'paper_id': fields.Integer(required=False,
            help='The unique identifier of a newspaper'),
    'name': fields.String(required=True,
            help='The name of the newspaper, e.g. The New York Times'),
    'frequency': fields.Integer(required=True,
            help='The publication frequency of the newspaper in days (e.g. 1 for daily papers and 7 for weekly magazines'),
    'price': fields.Float(required=True,
            help='The monthly price of the newspaper (e.g. 12.3)')
   })

@newspaper_ns.route('/')
class NewspaperAPI(Resource):

    @newspaper_ns.doc(paper_model, description="Add a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self):
        paper_id = uuid4().int % 100000000

        # create a new paper object and add it
        new_paper = Newspaper(paper_id=paper_id,
                              name=newspaper_ns.payload['name'],
                              frequency=newspaper_ns.payload['frequency'],
                              price=newspaper_ns.payload['price'])
        Agency.get_instance().add_newspaper(new_paper)

        # return the new paper
        return new_paper

    @newspaper_ns.marshal_list_with(paper_model, envelope='newspapers')
    def get(self):
        return Agency.get_instance().all_newspapers()

@newspaper_ns.route('/<int:paper_id>')
class NewspaperID(Resource):

    @newspaper_ns.doc(description="Get a new newspaper")
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def get(self, paper_id):
        search_result = Agency.get_instance().get_newspaper(paper_id)
        return search_result

    @newspaper_ns.doc(parser=paper_model, description="Update a new newspaper")
    @newspaper_ns.expect(paper_model, validate=True)
    @newspaper_ns.marshal_with(paper_model, envelope='newspaper')
    def post(self, paper_id):
        paper_to_be_updated = Agency.get_instance().get_newspaper(paper_id)
        agency = Agency.get_instance()
        agency.remove_newspaper(paper_to_be_updated)
        if not paper_to_be_updated:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        if 'name' in newspaper_ns.payload:
            paper_to_be_updated.name = newspaper_ns.payload['name']
        if 'frequency' in newspaper_ns.payload:
            paper_to_be_updated.frequency = newspaper_ns.payload['frequency']
        if 'price' in newspaper_ns.payload:
            paper_to_be_updated.price = newspaper_ns.payload['price']

        agency.add_newspaper(paper_to_be_updated)
        return paper_to_be_updated

    @newspaper_ns.doc(description="Delete a new newspaper")
    def delete(self, paper_id):
        targeted_paper = Agency.get_instance().get_newspaper(paper_id)
        if not targeted_paper:
            return jsonify(f"Newspaper with ID {paper_id} was not found")
        Agency.get_instance().remove_newspaper(targeted_paper)
        return jsonify(f"Newspaper with ID {paper_id} was removed")

@newspaper_ns.route('/<int:paper_id>/stats')
class NewspaperStats(Resource):
    def get(self, paper_id):
        # Step 1: Retrieve Newspaper Information
        newspaper = Agency.get_instance().get_newspaper(paper_id)
        if newspaper is None:
            return jsonify({"message": f"Newspaper with ID {paper_id} not found"}), 404

        # Step 2: Calculate Number of Subscribers
        num_subscribers = len(newspaper.subscribers)

        # Step 3: Calculate Revenue
        monthly_revenue = num_subscribers * newspaper.price
        annual_revenue = monthly_revenue * 12

        # Step 4: Return Information
        return jsonify({
            "paper_id": paper_id,
            "num_subscribers": num_subscribers,
            "monthly_revenue": monthly_revenue,
            "annual_revenue": annual_revenue
        })
