from flask_apscheduler import APScheduler
import synchronisation as synchro


scheduler = APScheduler()  # créer un objet Scheduler pour une tâche programmée

# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de la BDD)
def start_scheduler(app):
    scheduler.init_app(app)
    @scheduler.task('interval', id='do_job', days=1)
    def job():
        print("Synchronisation...")
        # Si la BDD est vide 🐽🐽🐽🐽🐽🐽
        #synchro.init_full_bdd()
        # Pour mettre à jour la base existante
        with app.app_context():
            synchro.differ_maj_bdd()
        print("...synchronisation terminée")
    scheduler.start()
