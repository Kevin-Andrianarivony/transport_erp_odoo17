#from odoo import models, fields

#class Seat(models.Model):
#    _name = 'transport.seat'
 #   _description = 'Seat'

 #   name = fields.Char(string="Place")
 #   reservation_id = fields.Many2one('transport.reservation')
 #   is_reserved = fields.Boolean(string="Réservée")
from odoo import models, fields
from odoo.exceptions import UserError

class TransportSeat(models.Model):
    _name = "transport.seat"
    _description = "Seat"

    reservation_id = fields.Many2one("transport.reservation", string="Réservation", ondelete="cascade")
    name = fields.Char(string="Siège", required=True)  # ex: A1, A2...
    state = fields.Selection([
        ("free", "Libre"),
        ("reserved", "Réservé"),
        ("driver", "Chauffeur"),
    ], default="free", string="Statut")
    passenger_name = fields.Char(string="Passager")

    def action_open_reserve_wizard(self):
        self.ensure_one()
        if not self.id:
            raise UserError("Veuillez d'abord enregistrer la réservation (Save) avant de réserver une place.")
        return {
            "type": "ir.actions.act_window",
            "name": "Réserver une place",
            "res_model": "transport.seat.reserve.wizard",
            "view_mode": "form",
            "target": "new",
            "context": {
                "default_seat_id": self.id,
                "default_passenger_name": self.env.user.name,
            },
        }