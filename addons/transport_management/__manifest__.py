{
    'name': 'Transport Management ERP',
    'version': '1.0',
    'summary': 'ERP pour gestion transport terrestre',
    'description': 'Gestion flotte, trajets, réservations, maintenance et facturation',
    'author': 'Groupe 3',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/vehicule_views.xml',
        'views/chauffeur_views.xml',
        'views/reservation_views.xml',
        'data/sequence.xml',
        'views/route_views.xml',
        'views/trip_views.xml',
        'views/menu.xml',
        #'views/trajet_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'transport_management/static/src/css/seats.css',
         ],
    },
    'installable': True,
    'application': True,
}