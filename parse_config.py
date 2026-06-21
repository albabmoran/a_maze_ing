import sys
from typing import Optional

class InvalidValue(Exception):
    pass

class Config:
    def __init__(self) -> None:
        self.width: int
        self.height: int
        self.entry: tuple[int, int]
        self.exit: tuple[int, int]
        self.output_file: str
        self.perfect: bool
        self.seed: Optional[int] = None
    
    def read_and_validate_format(self) -> list[str]:
        if len(sys.argv) != 2:
            print("ERROR: invalid number of arguments. "
                  "<Usage: python3 a_maze_ing.py config.txt>", file=sys.stderr)
            sys.exit(2) # Error por mal uso de los comandos en terminal

        try:
            with open("config.txt", "r") as file:
                content = file.read()
        except OSError as e: # Captura todos los errores del sistema
            print(f"ERROR reading file: {e}", file=sys.stderr) # strerror te da una frase bonita de error, se puede poner tambien si, da un poco igual
            sys.exit(e.errno) # da el código exacto del error
        
        valid_keys = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT", "SEED"
        ]
        keys: list[str] = []
        content = content.split('\n')
        for line in content: # aquí compruebo formato y valores
            if not line.strip() or line.startswith("#"): # comentario y que exista la línea
                continue
            index = line.find("=") # espacios y = // esto devuelve pos de =
            if (
                index < 0
                or index != line.rfind("=")
                or " " in line
                or not line[:index]
                or not line[index + 1:]
            ):
                print("ERROR: config.txt should have lines with KEY=VALUE and no spaces", file=sys.stderr)
                sys.exit(1)

            k, v = line.split("=") # a partir de aquí comprobar ya contenido como tal
            if k not in valid_keys:
                print(f"ERROR: invalid parameter {k}", file=sys.stderr)
                sys.exit(1)
            if k in keys:
                print(f"ERROR: duplicated key {k}", file=sys.stderr)
                sys.exit(1)

            if k == "WIDTH" or k == "HEIGHT": # comprobar si el valor es +
                try:
                    value = int(v)
                    if value <= 0:
                        raise InvalidValue(f"{v} is an invalid value for {k}")
                    if k == "WIDTH":
                        self.width = value
                    if k == "HEIGHT":
                        self.height = value
                    keys.append(k)
                except ValueError:
                    print(f"ERROR: {k} must be an int: <{v}>", file=sys.stderr)
                    sys.exit(1)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "ENTRY" or k =="EXIT": # comprobar que sea + y guardo
                try:
                    v1, v2 = v.split(",")
                    x = int(v1)
                    y = int(v2)
                    if x < 0 or y < 0:
                        raise InvalidValue(f"both coordinates ({x},{y}) must be positive")
                    coord = (x, y)
                    if k == "ENTRY":
                        self.entry = coord
                    if k == "EXIT":
                        self.exit = coord
                    keys.append(k)
                except ValueError:
                    print(f"ERROR: {k} must be an int: <{v}>", file=sys.stderr)
                    sys.exit(1)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "OUTPUT_FILE": # comprueba que sea un archivo .txt
                try:
                    if not v.endswith(".txt"):
                        raise InvalidValue("output file must be of format '.txt'")
                    self.output_file = v
                    keys.append(k)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "PERFECT":
                try:
                    if v == "True":
                        value = True
                    elif v == "False":
                        value = False
                    else:
                        raise InvalidValue("perfect should be 'True' or 'False'")
                    self.perfect = value
                    keys.append(k)
                except InvalidValue as e:
                    print(f"ERROR: {e}", file=sys.stderr)
                    sys.exit(1)

            elif k == "SEED": # cuando averigüemos cómo pues ya lo hago jiji porque no sé qué valor es
                keys.append(k)
        
        if self.height == 1 and self.width == 1:
            print("ERROR: invalid values, cannot generate an 1x1 maze", file=sys.stderr)
            sys.exit(1)
        return keys
    
    def check_mandatory_keys(self, keys: list[str]) -> None: # comprueba sin están todas las obligatorias. Lo hago aparte porque se necesita haber terminado de ver
        mandatory_keys = [
            "WIDTH", "HEIGHT", "ENTRY", "EXIT",
            "OUTPUT_FILE", "PERFECT"
        ]
        dif = set(mandatory_keys) - set(keys)
        if dif:
            missing= ", ".join(sorted(dif))
            print(f"ERROR: not all keys present. Missing: {missing}", file=sys.stderr)
            sys.exit(1)

    def check_entry_and_exit(self) -> None: # comprueba si entrada y salida son distintas y están en el laberinto. Aparte porque tienen que estar registrados los datos
        if self.entry == self.exit:
            print("ERROR: entry and exit must be different", file=sys.stderr)
            sys.exit(1)
        coord = [self.entry, self.exit]
        for c in coord:
            x, y = c[0], c[1]
            if x >= self.width or y >= self.height:
                print(f"ERROR: {c} is outside the maze", file=sys.stderr)
                sys.exit(1)


config = Config()
keys = config.read_and_validate_format()
config.check_mandatory_keys(keys)
config.check_entry_and_exit()