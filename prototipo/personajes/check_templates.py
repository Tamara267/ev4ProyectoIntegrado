from django.template import engines

django_engine = engines['django']

for template_dir in django_engine.dirs:
    print("DIRS:", template_dir)

print("APP_DIRS está activado:", django_engine.engine.app_dirs)

