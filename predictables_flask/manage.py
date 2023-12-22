def deploy():
    """Run deployment tasks."""
    from flask_migrate import init, migrate, stamp, upgrade

    from predictables_flask.app import create_app, db

    app = create_app()
    app.app_context().push()
    db.create_all()

    # migrate database to latest revision
    init()
    stamp()
    migrate()
    upgrade()
    return app, db


# deploy()
