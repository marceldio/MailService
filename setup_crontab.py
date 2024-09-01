import os


def setup_crontab():
    # путь к crontab_config.txt файлу
    crontab_file = "/home/md/Django/course_w_mail_sevice/crontab_config.txt"

    # Чтение файла конфигурации
    with open(crontab_file, 'r') as f:
        crontab_content = f.read()

    # Применение конфигурации через crontab
    os.system(f'(echo "{crontab_content}") | crontab -')

if __name__ == "__main__":
    setup_crontab()
