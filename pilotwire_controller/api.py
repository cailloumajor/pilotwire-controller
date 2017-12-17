from flask import Flask, jsonify, request
from flask.views import MethodView
from marshmallow import fields, Schema, validates, ValidationError

from .piface import PiFaceController


app = Flask(__name__)
controller = PiFaceController()


class PilotwireSchema(Schema):
    modes = fields.String(required=True)
    version = fields.String(dump_only=True)

    @validates('modes')
    def validate_modes(self, value):
        if not len(value) > 0:
            raise ValidationError("Must have at least one character.")
        if not len(value) <= 4:
            raise ValidationError("Must have at most four characters.")
        if not all([m in ['C', 'E', 'H', 'A'] for m in value]):
            raise ValidationError(
                "Each mode must be one of 'C', 'E', 'H', 'A'."
            )


pilotwire_schema = PilotwireSchema()


class PilotwireAPI(MethodView):

    def get(self):
        result = pilotwire_schema.dump(controller)
        return jsonify(result.data)

    def put(self):
        data, errors = pilotwire_schema.load(request.form)
        if errors:
            return jsonify({'errors': errors}), 400
        controller.modes = data['modes']
        return jsonify({
            'message': "Modes successfully set on pilotwire controller.",
            'modes': controller.modes,
        })


app.add_url_rule('/pilotwire', view_func=PilotwireAPI.as_view('pilotwire'))
