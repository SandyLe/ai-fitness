from app import create_app

app = create_app()

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=1005)
        # app.run(host='0.0.0.0', port=1005, ssl_context=('/etc/ssl/certs/founderbulusi.icu_bundle.crt', '/etc/ssl/private/founderbulusi.icu.key'))