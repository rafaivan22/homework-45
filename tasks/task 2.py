class CustomConfigParser:
    def __init__(self):
        self._config = {}

    def read(self, filepath):
        self._config.clear()
        try:
            with open(filepath, 'r') as file:
                section = None
                for line_number, line in enumerate(file, start=1):
                    line = line.strip()
                    if not line:
                        continue  # Пропустить пустые строки, которые не перед заголовком

                    if line.startswith('[') and line.endswith(']'):
                        section = line[1:-1].strip()
                        if not all(c.isalpha() or c.isspace() for c in section):
                            raise ValueError(f"Invalid section name on line {line_number}: {section}")
                        self._config[section] = {}
                    elif '=' in line:
                        if section is None:
                            raise ValueError(f"Invalid line in config file: {line}")
                        key, value = map(str.strip, line.split('=', 1))
                        if not key.isalnum():
                            raise ValueError(f"Invalid key on line {line_number}: {key}")
                        self._config[section][key] = value
                    else:
                        raise ValueError(f"Invalid line in config file: {line}")
        except FileNotFoundError:
            raise FileNotFoundError(f"File {filepath} not found")
        except ValueError as e:
            print(e)

    def get(self, section, key):
        if section not in self._config:
            raise KeyError(f"Section {section} not found")
        if key not in self._config[section]:
            raise KeyError(f"Key {key} not found in section {section}")
        return self._config[section][key]

    def set(self, section, key, value):
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value

    def add_section(self, section):
        if section in self._config:
            raise KeyError(f"Section {section} already exists")
        self._config[section] = {}

    def remove_section(self, section):
        if section not in self._config:
            raise KeyError(f"Section {section} not found")
        del self._config[section]

    def remove_option(self, section, key):
        if section not in self._config:
            raise KeyError(f"Section {section} not found")
        if key not in self._config[section]:
            raise KeyError(f"Key {key} not found in section {section}")
        del self._config[section][key]

    def write(self, filepath):
        with open(filepath, 'w') as file:
            for section, options in self._config.items():
                file.write(f"[{section}]\n")
                for key, value in options.items():
                    file.write(f"{key} = {value}\n")
                file.write("\n")  # добавить пустую строку после каждой секции

# Пример использования:
config_parser = CustomConfigParser()

# Чтение файла
try:
    config_parser.read("config.configus")
except FileNotFoundError as e:
    print(f"File not found: {e}")
except ValueError as e:
    print(f"Value error: {e}")

# Получение значения
try:
    host = config_parser.get("server", "host")
    print(f"Server host: {host}")
except KeyError as e:
    print(e)

# Установка значения
config_parser.set("server", "host", "127.0.0.1")

# Добавление новой секции
try:
    config_parser.add_section("newsection")
except KeyError as e:
    print(e)

# Запись в файл
config_parser.write("new_config.configus")