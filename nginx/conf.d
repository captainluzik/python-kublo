server {
    listen 80;
    server_name python-kublo_django_1;

    location / {
        proxy_pass http://python-kublo_django_1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
    }

    location static { alias /app/static/; }

    location media { alias /app/media/; }

}
