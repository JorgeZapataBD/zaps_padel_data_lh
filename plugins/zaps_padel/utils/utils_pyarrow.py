import importlib

import pyarrow as pa


def schema_to_dict(schema: pa.Schema) -> dict:
    """Convert PyArrow Scheme in serializable dictionary"""
    def field_to_dict(field: pa.Field) -> dict:
        return {
            'name': field.name,
            'type': type_to_dict(field.type)
        }

    def type_to_dict(data_type: pa.DataType):
        if isinstance(data_type, pa.ListType):
            return {'list': type_to_dict(data_type.value_type)}
        elif isinstance(data_type, pa.StructType):
            return {'struct': [field_to_dict(f) for f in data_type]}
        elif isinstance(data_type, pa.DictionaryType):
            return {
                'dictionary': {
                    'index_type': type_to_dict(data_type.index_type),
                    'value_type': type_to_dict(data_type.value_type)
                }
            }

        else:
            return str(data_type)

    return {'fields': [field_to_dict(field) for field in schema]}


def dict_to_schema(schema_dict: dict) -> pa.Schema:
    """Convert serializabled schema to PyArrow Scheme"""

    def dict_to_field(field_dict: dict) -> pa.Field:
        return pa.field(field_dict["name"], dict_to_type(field_dict["type"]))

    def dict_to_type(type_dict):
        if isinstance(type_dict, str):  # Tipos básicos (int32, string, etc.)
            type_mapping = {
                'bool': pa.bool_(),
                'int8': pa.int8(),
                'int16': pa.int16(),
                'int32': pa.int32(),
                'int64': pa.int64(),
                'uint8': pa.uint8(),
                'uint16': pa.uint16(),
                'uint32': pa.uint32(),
                'uint64': pa.uint64(),
                'float': pa.float32(),
                'double': pa.float64(),
                'string': pa.string(),
                'binary': pa.binary(),
                'null': pa.null()
            }
            if type_dict not in type_mapping:
                raise ValueError(f"Tipo no soportado: {type_dict}")
            return type_mapping[type_dict]
        elif "list" in type_dict:  # Tipo Lista
            return pa.list_(dict_to_type(type_dict["list"]))
        elif "struct" in type_dict:  # Tipo Struct
            return pa.struct([dict_to_field(f) for f in type_dict["struct"]])
        elif "dictionary" in type_dict:  # Tipo Diccionario
            return pa.dictionary(
                dict_to_type(type_dict["dictionary"]["index_type"]),
                dict_to_type(type_dict["dictionary"]["value_type"])
            )
        else:
            raise ValueError(f"Tipo no soportado: {type_dict}")

    return pa.schema([dict_to_field(f) for f in schema_dict["fields"]])


def get_pyarrow_schema(catalog: str, schema_name: str) -> pa.Schema:
    """
    Function to get dict schema from python module and convert in pyarrow Schema.

    :param catalog: Origin catalog data to get schema
    :param schema_name: Name of the schema in the module
    :return: pyarrow schema
    """
    # Load schema module
    module_name = f'plugins.zaps_padel.catalogs.{catalog}'
    module = importlib.import_module(module_name)
    d_schema = getattr(module, schema_name)
    # Convert schema to pyarrow object
    pa_schema = dict_to_schema(d_schema)
    return pa_schema


def validate_fields_against_schema(
    data: list[dict],
    schema: pa.Schema
) -> tuple[list[str], list[str]]:
    """
    Validates a list of dictionaries against a PyArrow schema.
    Returns two lists: extra fields and missing fields (with full names, including nested ones).
    :param data: List of dictionaries with data content
    :param schema: pyarrow parquet table schema
    :return tuple(list,list): List of fields extra and missing
    """
    def recurse(entry: dict, schema: pa.Schema, path="") -> tuple[list[str], list[str]]:
        extras = []
        missing = []
        schema_fields = {f.name: f for f in schema}

        entry_keys = set(entry.keys())
        schema_keys = set(schema_fields.keys())

        # Extras
        for key in entry_keys - schema_keys:
            extras.append(f"{path}{key}")

        # Missing and recurse
        for key in schema_keys:
            field = schema_fields[key]
            full_key = f"{path}{key}"
            if key not in entry:
                missing.append(full_key)
            else:
                value = entry[key]
                if pa.types.is_struct(field.type):
                    if isinstance(value, dict):
                        sub_extras, sub_missing = recurse(
                            value, field.type, path=full_key + ".")
                        extras.extend(sub_extras)
                        missing.extend(sub_missing)
                    elif value is None:
                        for subfield in field.type:
                            missing.append(f"{full_key}.{subfield.name}")
        return extras, missing

    all_extras = []
    all_missing = []
    for item in data:
        extras, missing = recurse(item, schema)
        all_extras.extend(extras)
        all_missing.extend(missing)

    return all_extras, all_missing
