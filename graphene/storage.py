from graphenestorage import (
    InRamConfigurationStore,
    InRamPlainKeyStore,
    InRamEncryptedKeyStore,
    SqliteConfigurationStore,
    SqlitePlainKeyStore,
    SqliteEncryptedKeyStore,
    SQLiteFile
)


# default_url = wss://default.example.com
# InRamConfigurationStore.setdefault("node", default_url)
# SqliteConfigurationStore.setdefault("node", default_url)


def get_default_config_store(*args, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "graphene"
    return SqliteConfigurationStore(*args, **kwargs)


def get_default_key_store(*args, config, **kwargs):
    if "appname" not in kwargs:
        kwargs["appname"] = "graphene"
    return SqliteEncryptedKeyStore(
        config=config, **kwargs
    )
