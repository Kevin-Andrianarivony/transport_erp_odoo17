# transport_management/models/trip.py
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TransportTrip(models.Model):
    _name = "transport.trip"
    _description = "Transport Trip"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "departure_datetime desc"

    name = fields.Char(copy=False, readonly=True, default="New", index=True)
    active = fields.Boolean(default=True)

    route_id = fields.Many2one("transport.route", required=True, tracking=True)
    departure_datetime = fields.Datetime(required=True, tracking=True)
    arrival_datetime = fields.Datetime(tracking=True)

    capacity = fields.Integer(default=0, tracking=True)

    reservation_ids = fields.One2many(
        "transport.reservation", "trip_id", string="Reservations"
    )

    reserved_seats = fields.Integer(compute="_compute_reserved_seats", store=True, tracking=True)
    available_seats = fields.Integer(compute="_compute_available_seats", store=True)

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("confirmed", "Confirmed"),
            ("in_progress", "In progress"),
            ("done", "Done"),
            ("cancelled", "Cancelled"),
        ],
        default="draft",
        tracking=True,
    )

    vehicle_id = fields.Many2one("transport.vehicule", string="Vehicule", tracking=True)
    driver_id = fields.Many2one("transport.chauffeur", string="Chauffeur", tracking=True)

    @api.depends("reservation_ids.seat_ids.state")
    def _compute_reserved_seats(self):
        for trip in self:
            # compte toutes les places 'reserved' de toutes les reservations du trip
            trip.reserved_seats = sum(
                1 for seat in trip.reservation_ids.mapped("seat_ids")
                if seat.state == "reserved"
            )

    @api.depends("capacity", "reserved_seats")
    def _compute_available_seats(self):
        for rec in self:
            rec.available_seats = max(rec.capacity - rec.reserved_seats, 0)

    @api.constrains("departure_datetime", "arrival_datetime")
    def _check_dates(self):
        for rec in self:
            if rec.arrival_datetime and rec.departure_datetime and rec.arrival_datetime <= rec.departure_datetime:
                raise ValidationError("Arrival must be after departure.")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "New") == "New":
                vals["name"] = self.env["ir.sequence"].next_by_code("transport.trip") or "TRIP"
        return super().create(vals_list)
    
    @api.onchange("vehicle_id")
    def _onchange_vehicle_id_set_capacity(self):
        for rec in self:
            if rec.vehicle_id and hasattr(rec.vehicle_id, "capacite"):
                rec.capacity = rec.vehicle_id.capacite or 0

    def action_confirm(self):
        self.write({"state": "confirmed"})
    def action_start(self):
        self.write({"state": "in_progress"})
    def action_done(self):
        self.write({"state": "done"})
    def action_cancel(self):
        self.write({"state": "cancelled"})
    def action_set_draft(self):
        self.write({"state": "draft"})