from odoo import models, fields

class Chauffeur(models.Model):
    _name = "transport.chauffeur"
    _description = "Chauffeur"

    name = fields.Char(string="Nom", required=True)
    phone = fields.Char(string="Téléphone")
    email = fields.Char(string="Email")
    numero_permis = fields.Char(string="Numéro de permis")
    date_embauche = fields.Date(string="Date d'embauche")

    actif = fields.Boolean(string="Actif", default=True)

    vehicule_id = fields.Many2one(
        "transport.vehicule",
        string="Véhicule assigné"
    )