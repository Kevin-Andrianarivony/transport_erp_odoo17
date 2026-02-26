from odoo import models, fields, api

class Vehicule(models.Model):
    _name = "transport.vehicule"
    _description = "Véhicule"
    _rec_name = "immatriculation"

    name = fields.Char(string="Nom du véhicule", required=True)
    immatriculation = fields.Char(string="Immatriculation", required=True)
    marque = fields.Char(string="Marque")
    modele = fields.Char(string="Modèle")
    annee = fields.Integer(string="Année")
    capacite = fields.Integer(string="Capacité (places)")

    etat = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_service', 'En service'),
        ('maintenance', 'En maintenance')
    ], string="État", default='disponible')

    chauffeur_id = fields.Many2one(
        "transport.chauffeur",
        string="Chauffeur principal"
    )

    _sql_constraints = [
        ('immatriculation_unique',
         'unique(immatriculation)',
         'L\'immatriculation doit être unique !')
    ]
