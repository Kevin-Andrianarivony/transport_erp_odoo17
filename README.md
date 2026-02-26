# INSTALLATION
Creer un utilisateur et une BD sur Postgres

Cloner le projet
sur la racine du projet  : 
                            Creer un fichier odoo.conf avec :
                                [options]
                                admin_passwd = postgres
                                db_host = localhost
                                db_port = 5432
                                db_user = erp2026 (user postgres crée précédemment )
                                db_password = erp2026 (mot de passe de l'user)
                                addons_path = addons

                            executer dans le terminal : .\venv\Scripts\activate
                                                        pip install -r requirements.txt
                            Lancer Odoo : python odoo-bin -c odoo.conf -d ta_base(nom de la base de donnée)

=======
# transport_erp_odoo17
ERP Transport Terrestre + SOA + BI + Data Mining + IA 
# ERP Transport Terrestre

Projet académique : ERP + SOA + BI + Data Mining + IA

## Technologies
- Odoo 17
- PostgreSQL
- Python
- Power BI

## Modules développés
- Gestion Véhicules
- Gestion Chauffeurs
- Gestion Trajets
- Réservations
- Maintenance
<<<<<<< HEAD
- Facturation
=======
- Facturation
>>>>>>> dec2290533bdd13030994ce2e2aca840cf2b70ee
