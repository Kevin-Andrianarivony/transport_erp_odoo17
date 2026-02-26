from odoo import models, fields
from odoo.exceptions import UserError

class SeatReserveWizard(models.TransientModel):
    _name = "transport.seat.reserve.wizard"
    _description = "Reserve Seat Wizard"

    seat_id = fields.Many2one("transport.seat", required=True, readonly=True)
    passenger_name = fields.Char(string="Passager", required=True)

    def action_confirm(self):
        self.ensure_one()
        seat = self.seat_id

      #  if seat.state == "driver":
       #     raise UserError("Impossible de réserver la place chauffeur.")
       # if seat.state == "reserved":
       #     raise UserError("Cette place est déjà réservée.")

        seat.write({
            "state": "reserved",
            "passenger_name": self.passenger_name,
        })
        return {"type": "ir.actions.client", "tag": "reload"}