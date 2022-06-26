import os
import logging

def get_logger(name="root"):
    logger = logging.getLogger(name)
    logging.basicConfig(
        level=getattr(
            logging,
            os.environ.get("LOGLEVEL", "info").upper()
        )
    )
    return logger

logger = get_logger()

def get_mongo():
    try:
        import pymongo
        client = pymongo.MongoClient(
            os.environ.get("MONGO_HOSTNAME"),
            connect=False,
            w=1
        )
        logger.debug(f"MongoDB: Connected to \'{os.environ.get('MONGO_HOSTNAME')}\'")
        db_name = os.environ.get("MONGO_DATABASE") or "stabox"
        if client[db_name]:
            logger.debug(f"MongoDB: Using \'{db_name}\'")
            return client[db_name]
        else:
            logger.error(f"MongoDB: Connection error to \'{db_name}\'")
    except:
        logger.error(f"MongoDB: Connection error")
        #raise
    return


def get_mysql():
    try:
        import mysql.connector
        port = int(os.environ.get("MYSQL_PORT", 3306))
        host = os.environ.get("MYSQL_HOSTNAME", "localhost")
        database = os.environ.get("MYSQL_DATABASE") or "internettv_sta"
        client = mysql.connector.connect(
            host = host,
            port = port,
            user = os.environ.get("MYSQL_USERNAME", "root"),
            password = os.environ.get("MYSQL_PASSWORD", ""),
            database = database,
            pool_size = int(os.environ.get("WORKERS", 100)),
            autocommit = True)
        if client:
            logger.debug(f"MySQL: Connected to \'{host}:{port}\'")
            logger.debug(f"MySQL: Using \'{database}\'")
            return client
        else:
            logger.error(f"MySQL: Connection error to \'{database}\'")
    except:
        logger.error(f"MySQL: Connection error")
#        raise
    return


from google.protobuf.json_format import MessageToDict, ParseDict

def to_dict(message):
    message = message or {}
    return MessageToDict(message, preserving_proto_field_name=True)

def from_dict(dict_obj, message_type):
    return ParseDict(dict_obj, message_type(), ignore_unknown_fields=False)
