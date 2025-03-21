import os
import dotenv

dotenv.load_dotenv()

class EnvMeta(type):
    _variables = {}

    def __call__(cls, key: str):
        if key not in cls._variables:
            env_value = os.environ.get(key)
            if env_value is None:
                raise ValueError(f"Missing required environment variable: {key}")
            cls._variables[key] = env_value

        return cls._variables[key]

class Env(metaclass=EnvMeta):
    pass