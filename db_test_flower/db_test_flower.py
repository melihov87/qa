import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Получение переменных окружения
def get_db_config():
    """Получает параметры подключения к базе данных из переменных окружения."""
    user = os.getenv("FL_USER")
    password = os.getenv("FL_PASSWORD")
    host = os.getenv("FL_HOST")
    database = os.getenv("FL_DATABASE")
    port = os.getenv("FL_PORT")

    # Проверка, что все параметры заданы
    if not all([user, password, host, database, port]):
        logger.error("Недостающие параметры для подключения к базе данных.")
        raise ValueError("Не все параметры подключения заданы.")

    return {
        "user": user,
        "password": password,
        "host": host,
        "database": database,
        "port": port
    }


# Формирование строки подключения
def create_database_url(config):
    """Формирует строку подключения к базе данных MySQL."""
    return f"mysql+pymysql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"


# Инициализация подключения к базе данных
def create_engine_connection(database_url):
    """Создает подключение к базе данных MySQL."""
    try:
        engine = create_engine(
            database_url,
            echo=False,
            pool_size=5,
            max_overflow=10,
        )
        return engine
    except SQLAlchemyError as e:
        logger.error(f"Ошибка подключения к базе данных: {e}")
        raise


# Получение версии MySQL
def get_mysql_version(engine):
    """Получает версию MySQL."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT VERSION()"))
            version = result.fetchone()
            logger.info(f"MySQL version: {version[0]}")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении версии MySQL: {e}")


# Получение всех таблиц
def get_all_tables(engine):
    """Получает все таблицы в базе данных."""
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES"))
            table_names = [row[0].replace(",", "") for row in result]
            logger.info(f"Список таблиц: {table_names}")
            for name in table_names:
                logger.info(f"Таблица: {name}")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка таблиц: {e}")


# Получение информации о цветах из магазина
def get_flower_shop_info(engine):
    """Получает информацию о товарах из магазина 'Магазин 1'."""
    try:
        with engine.connect() as conn:
            query = text(
                "SELECT product_name, price, shops, purchase_price, points_percent FROM "
                "flower_shop_flower WHERE shops = 'Магазин 1'")
            result = conn.execute(query)
            for row in result:
                logger.info(
                    f"Продукт: {row.product_name}, Цена: {row.price}, Магазин: {row.shops}, Закупочная цена: "
                    f"{row.purchase_price}, Скидка: {row.points_percent}")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении данных о цветах: {e}")


# Получение информации о клиентах
def get_clients_info(engine):
    """Получает информацию о клиентах и их бонусных баллах."""
    try:
        with engine.connect() as conn:
            query = text("SELECT first_name, last_name, loyalty_points FROM clients")
            result = conn.execute(query)
            for client in result:
                logger.info(f"Клиент: {client.first_name} {client.last_name}, Бонусные баллы: {client.loyalty_points}")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении данных о клиентах: {e}")


def main():
    """Главная функция для выполнения всех операций."""
    try:
        db_config = get_db_config()
        database_url = create_database_url(db_config)
        engine = create_engine_connection(database_url)

        # Выполнение операций с базой данных
        get_mysql_version(engine)
        get_all_tables(engine)
        get_flower_shop_info(engine)
        get_clients_info(engine)

    except Exception as e:
        logger.error(f"Ошибка при выполнении основного процесса: {e}")


if __name__ == "__main__":
    main()
