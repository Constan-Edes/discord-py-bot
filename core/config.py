from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix=False,
    settings_files=['settings.toml', '.secrets.toml'],
    environments=True,
    load_dotenv=True,
    env_switcher="MYPROGRAM_ENV"
)

COGS_DIR = "./cogs"


# `envvar_prefix` = export envvars with `export DYNACONF_FOO=bar`.
# `settings_files` = Load these files in the order.
