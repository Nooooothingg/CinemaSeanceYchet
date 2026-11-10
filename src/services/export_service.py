import csv
import json
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path
from typing import Any

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

from src.database.database import get_conn
from src.repositories import schedule_rep, film_rep, cinema_rep, users_rep


OUT_DIR = Path("out")


def _ensure_out_dir() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def _fetch_schedule_data() -> list[dict[str, Any]]:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            s.Schedule_ID,
            s.date_time,
            f.Film_ID,
            f.Film_name,
            f.Film_descr,
            f.Film_time,
            c.Cinema_ID,
            c.name,
            c.description,
            c.link,
            u.User_ID,
            u.username,
            u.login
        FROM Schedule s
        JOIN Film f ON s.Film_ID = f.Film_ID
        JOIN Cinema c ON s.Cinema_ID = c.Cinema_ID
        JOIN Users u ON s.admin_id = u.User_ID
        ORDER BY s.Schedule_ID
    """)
    rows = cur.fetchall()
    conn.close()

    result: list[dict[str, Any]] = []
    for row in rows:
        result.append({
            "schedule_id": row[0],
            "date_time": str(row[1]),
            "film": {
                "film_id": row[2],
                "film_name": row[3],
                "film_descr": row[4],
                "film_time": row[5],
            },
            "cinema": {
                "cinema_id": row[6],
                "name": row[7],
                "description": row[8],
                "link": row[9],
            },
            "admin": {
                "user_id": row[10],
                "username": row[11],
                "login": row[12],
            },
        })
    return result


def _fetch_schedule_flat() -> list[dict[str, Any]]:

    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            s.Schedule_ID,
            s.date_time,
            f.Film_ID,
            f.Film_name,
            f.Film_descr,
            f.Film_time,
            c.Cinema_ID,
            c.name,
            c.description,
            c.link,
            u.User_ID,
            u.username,
            u.login
        FROM Schedule s
        JOIN Film f ON s.Film_ID = f.Film_ID
        JOIN Cinema c ON s.Cinema_ID = c.Cinema_ID
        JOIN Users u ON s.admin_id = u.User_ID
        ORDER BY s.Schedule_ID
    """)
    rows = cur.fetchall()
    conn.close()

    columns = [
        "schedule_id", "date_time",
        "film_id", "film_name", "film_descr", "film_time",
        "cinema_id", "cinema_name", "cinema_description", "cinema_link",
        "admin_id", "admin_username", "admin_login",
    ]
    return [dict(zip(columns, row)) for row in rows]


def export_json(data: list[dict[str, Any]]) -> None:
    path = OUT_DIR / "data.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def export_csv(data: list[dict[str, Any]]) -> None:
    path = OUT_DIR / "data.csv"
    if not data:
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write("")
        return

    fieldnames = list(data[0].keys())
    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def _xml_escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def _dict_to_xml_element(tag: str, value: Any) -> ET.Element:
    elem = ET.Element(tag)
    if isinstance(value, dict):
        for k, v in value.items():
            child = _dict_to_xml_element(k, v)
            elem.append(child)
    elif isinstance(value, list):
        for item in value:
            child = _dict_to_xml_element("item", item)
            elem.append(child)
    else:
        elem.text = _xml_escape(str(value))
    return elem


def export_xml(data: list[dict[str, Any]]) -> None:
    path = OUT_DIR / "data.xml"
    root = ET.Element("data")
    for item in data:
        root.append(_dict_to_xml_element("record", item))

    rough_string = ET.tostring(root, encoding="unicode")
    reparsed = minidom.parseString(rough_string)
    pretty = reparsed.toprettyxml(indent="  ", encoding="utf-8")

    with open(path, "wb") as f:
        f.write(pretty)


def export_yaml(data: list[dict[str, Any]]) -> None:
    if not HAS_YAML:
        print("[ПРЕДУПРЕЖДЕНИЕ] Модуль yaml не установлен, файл data.yaml не будет создан")
        return
    path = OUT_DIR / "data.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, default_flow_style=False)


def export_all() -> None:
    """
    Экспортирует данные сеансов со связанными сущностями в 4 формата.
    """
    _ensure_out_dir()

    nested = _fetch_schedule_data()
    flat = _fetch_schedule_flat()

    export_json(nested)
    export_csv(flat)
    export_xml(nested)
    export_yaml(nested)

    print(f"\n[ЭКСПОРТ] Данные сохранены в папку '{OUT_DIR}/':")
    print(f"  - data.json  ({len(nested)} записей, вложенная структура)")
    print(f"  - data.csv   ({len(flat)} записей, плоская структура)")
    print(f"  - data.xml   ({len(nested)} записей, вложенная структура)")
    print(f"  - data.yaml  ({len(nested)} записей, вложенная структура)")
