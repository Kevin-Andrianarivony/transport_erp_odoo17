# transport_management/models/route.py
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TransportRoute(models.Model):
    _name = "transport.route"
    _description = "Transport Route"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(required=True, tracking=True)
    code = fields.Char(copy=False, readonly=True, default="New", index=True)
    active = fields.Boolean(default=True)

    origin = fields.Char(required=True, tracking=True)
    destination = fields.Char(required=True, tracking=True)

    distance_km = fields.Float(string="Distance (km)", tracking=True)
    estimated_duration_min = fields.Integer(string="Estimated duration (min)")

    stop_ids = fields.One2many("transport.route.stop", "route_id", string="Stops")
    note = fields.Text()

    _sql_constraints = [
        ("route_code_uniq", "unique(code)", "Route code must be unique."),
    ]

    @api.constrains("origin", "destination")
    def _check_origin_destination(self):
        for rec in self:
            if rec.origin and rec.destination and rec.origin.strip().lower() == rec.destination.strip().lower():
                raise ValidationError("Origin and destination must be different.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "New") == "New":
                vals["code"] = self.env["ir.sequence"].next_by_code("transport.route") or "ROUTE"
        return super().create(vals_list)


class TransportRouteStop(models.Model):
    _name = "transport.route.stop"
    _description = "Route Stop"
    _order = "sequence, id"

    route_id = fields.Many2one("transport.route", required=True, ondelete="cascade")
    sequence = fields.Integer(default=10)
    name = fields.Char(required=True)
    distance_from_origin_km = fields.Float(string="Distance from origin (km)")
    stop_duration_min = fields.Integer(string="Stop duration (min)", default=0)