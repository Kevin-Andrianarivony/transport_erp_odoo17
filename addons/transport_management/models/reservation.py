from odoo import models, fields, api
from odoo.exceptions import UserError


class Reservation(models.Model):
    _name = "transport.reservation"
    _description = "Reservation"

    # 1) On réserve sur un TRIP (voyage réel)
    trip_id = fields.Many2one(
        "transport.trip",
        string="Trip",
        required=True,
    )

    # 2) Infos dérivées du trip (read-only, cohérentes)
    route_id = fields.Many2one(related="trip_id.route_id", store=True, readonly=True, string="Route")
    origin = fields.Char(related="trip_id.route_id.origin", store=True, readonly=True, string="Origin")
    destination = fields.Char(related="trip_id.route_id.destination", store=True, readonly=True, string="Destination")

    voiture_id = fields.Many2one(
        related="trip_id.vehicle_id",
        store=True,
        readonly=True,
        string="Voiture",
    )

    chauffeur_id = fields.Many2one(
        related="trip_id.driver_id",
        store=True,
        readonly=True,
        string="Chauffeur",
    )

    date_depart = fields.Datetime(
        related="trip_id.departure_datetime",
        store=True,
        readonly=True,
        string="Date de départ",
    )

    # Capacité de la réservation = capacité du trip (recommandé)
    capacite = fields.Integer(
        related="trip_id.capacity",
        store=True,
        readonly=True,
        string="Capacité",
    )

    seat_ids = fields.One2many(
        "transport.seat",
        "reservation_id",
        string="Places",
    )

    # 3) Génération des places dès qu'on choisit le trip (UI)
    @api.onchange("trip_id")
    def _onchange_trip_id_generate_seats(self):
        for rec in self:
            if not rec.trip_id:
                rec.seat_ids = [(5, 0, 0)]
                return

            cap = rec.trip_id.capacity or 0
            if not cap and rec.trip_id.vehicle_id and hasattr(rec.trip_id.vehicle_id, "capacite"):
                cap = rec.trip_id.vehicle_id.capacite or 0

            cmds = [(5, 0, 0)]
            cmds.append((0, 0, {"name": "Chauffeur", "state": "driver"}))
            for i in range(1, cap + 1):
                cmds.append((0, 0, {"name": f"Place {i}", "state": "free"}))

            rec.seat_ids = cmds

    # 4) Sécurité : à la création, si seat_ids n'est pas fourni (ex: create via RPC),
    # on génère aussi depuis trip.capacity pour éviter une réservation sans places.
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("seat_ids") and vals.get("trip_id"):
                trip = self.env["transport.trip"].browse(vals["trip_id"])
                cap = trip.capacity or 0
                seats_cmds = [(0, 0, {"name": "Chauffeur", "state": "driver"})]
                seats_cmds += [(0, 0, {"name": f"Place {i}", "state": "free"}) for i in range(1, cap + 1)]
                vals["seat_ids"] = seats_cmds
        return super().create(vals_list)