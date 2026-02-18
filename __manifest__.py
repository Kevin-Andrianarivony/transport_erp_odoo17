{
    'name': 'Transport Management ERP',
    'version': '1.0',
    'summary': 'ERP pour gestion transport terrestre',
    'description': 'Gestion flotte, trajets, réservations, maintenance et facturation',
    'author': 'Groupe 3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        #'views/menu.xml',
        #'views/vehicule_views.xml',
        #'views/chauffeur_views.xml',
        #'views/trajet_views.xml',
       # 'views/reservation_views.xml',
    ],
    'installable': True,
    'application': True,
}