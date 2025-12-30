
import json
from functools import lru_cache
from jsonschema import validate, ValidationError, SchemaError


# Schema loader (cached)
@lru_cache(maxsize=16)
def _load_schema(schema_path):
    """Load and cache a JSON schema from disk."""
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load schema '{schema_path}': {e}")


# Public Validation Function
def validate_json(data, schema_path):
    """Validate JSON data against a schema file."""
    try:
        schema = _load_schema(schema_path)
    except RuntimeError as e:
        return False, str(e)

    try:
        validate(instance=data, schema=schema)
        return True, None

    except ValidationError as e:
        # Standard validation failure
        return False, f"ValidationError: {e.message}"

    except SchemaError as e:
        # Schema itself invalid
        return False, f"SchemaError: {e}"

    except Exception as e:
        # Catch unexpected issues
        return False, f"Unexpected validation error: {e}"
