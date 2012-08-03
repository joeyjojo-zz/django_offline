import sys

__author__ = 'jond'

def main():
    import django_offline
    import mysite.settings
    sys.exit(django_offline.run(mysite.settings.MAIN_URL))

if __name__ == '__main__':
    main()