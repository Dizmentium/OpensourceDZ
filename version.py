import requests
import json
import time
from datetime import datetime

DATA_FILE = "packages.json"

PACKAGES = ["requests", "numpy", "pandas"]


def load_versions():
    "Загрузка сохранённых версий"
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def save_versions(versions):
    "Сохранение текущих версий"
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(versions, f, indent=4, ensure_ascii=False)


def get_latest_version(package_name):
    "Получение последней версии пакета с PyPI"
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["info"]["version"]
    else:
        print(f"Не удалось получить данные о пакете {package_name}")
        return None


def check_updates():
    "Проверка обновлений"
    saved_versions = load_versions()
    updated_packages = []

    for pkg in PACKAGES:
        latest = get_latest_version(pkg)
        if latest is None:
            continue

        old_version = saved_versions.get(pkg)
        if old_version != latest:
            updated_packages.append((pkg, old_version, latest))
            saved_versions[pkg] = latest

    if updated_packages:
        print("\nНайдены обновления:")
        for pkg, old, new in updated_packages:
            print(f" - {pkg}: {old} → {new}")
        save_versions(saved_versions)
    else:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Всё актуально.")


def main():
    print("Система отслеживания версий запущена\n")
    while True:
        check_updates()
        time.sleep(3600)


if __name__ == "__main__":
    main()
