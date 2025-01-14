<a name="models.metaclass"></a>
# models.metaclass

<a name="models.metaclass.ModelMeta"></a>
## ModelMeta Objects

```python
class ModelMeta()
```

Class used for type hinting.
Users can subclass this one for convenience but it's not required.
The only requirement is that ormar.Model has to have inner class with name Meta.

<a name="models.metaclass.add_cached_properties"></a>
#### add\_cached\_properties

```python
add_cached_properties(new_model: Type["Model"]) -> None
```

Sets cached properties for both pydantic and ormar models.

Quick access fields are fields grabbed in getattribute to skip all checks.

Related fields and names are populated to None as they can change later.
When children models are constructed they can modify parent to register itself.

All properties here are used as "cache" to not recalculate them constantly.

**Arguments**:

- `new_model` (`Model class`): newly constructed Model

<a name="models.metaclass.add_property_fields"></a>
#### add\_property\_fields

```python
add_property_fields(new_model: Type["Model"], attrs: Dict) -> None
```

Checks class namespace for properties or functions with __property_field__.
If attribute have __property_field__ it was decorated with @property_field.

Functions like this are exposed in dict() (therefore also fastapi result).
Names of property fields are cached for quicker access / extraction.

**Arguments**:

- `new_model` (`Model class`): newly constructed model
- `attrs` (`Dict[str, str]`): 

<a name="models.metaclass.register_signals"></a>
#### register\_signals

```python
register_signals(new_model: Type["Model"]) -> None
```

Registers on model's SignalEmmiter and sets pre defined signals.
Predefined signals are (pre/post) + (save/update/delete).

Signals are emitted in both model own methods and in selected queryset ones.

**Arguments**:

- `new_model` (`Model class`): newly constructed model

<a name="models.metaclass.verify_constraint_names"></a>
#### verify\_constraint\_names

```python
verify_constraint_names(base_class: "Model", model_fields: Dict, parent_value: List) -> None
```

Verifies if redefined fields that are overwritten in subclasses did not remove
any name of the column that is used in constraint as it will fail in sqlalchemy
Table creation.

**Arguments**:

- `base_class` (`Model or model parent class`): one of the parent classes
- `model_fields` (`Dict[str, BaseField]`): ormar fields in defined in current class
- `parent_value` (`List`): list of base class constraints

<a name="models.metaclass.update_attrs_from_base_meta"></a>
#### update\_attrs\_from\_base\_meta

```python
update_attrs_from_base_meta(base_class: "Model", attrs: Dict, model_fields: Dict) -> None
```

Updates Meta parameters in child from parent if needed.

**Arguments**:

- `base_class` (`Model or model parent class`): one of the parent classes
- `attrs` (`Dict`): new namespace for class being constructed
- `model_fields` (`Dict[str, BaseField]`): ormar fields in defined in current class

<a name="models.metaclass.copy_and_replace_m2m_through_model"></a>
#### copy\_and\_replace\_m2m\_through\_model

```python
copy_and_replace_m2m_through_model(field: ManyToManyField, field_name: str, table_name: str, parent_fields: Dict, attrs: Dict, meta: ModelMeta, base_class: Type["Model"]) -> None
```

Clones class with Through model for m2m relations, appends child name to the name
of the cloned class.

Clones non foreign keys fields from parent model, the same with database columns.

Modifies related_name with appending child table name after '_'

For table name, the table name of child is appended after '_'.

Removes the original sqlalchemy table from metadata if it was not removed.

**Arguments**:

- `base_class` (`Type["Model"]`): base class model
- `field` (`ManyToManyField`): field with relations definition
- `field_name` (`str`): name of the relation field
- `table_name` (`str`): name of the table
- `parent_fields` (`Dict`): dictionary of fields to copy to new models from parent
- `attrs` (`Dict`): new namespace for class being constructed
- `meta` (`ModelMeta`): metaclass of currently created model

<a name="models.metaclass.copy_data_from_parent_model"></a>
#### copy\_data\_from\_parent\_model

```python
copy_data_from_parent_model(base_class: Type["Model"], curr_class: type, attrs: Dict, model_fields: Dict[str, Union[BaseField, ForeignKeyField, ManyToManyField]]) -> Tuple[Dict, Dict]
```

Copy the key parameters [database, metadata, property_fields and constraints]
and fields from parent models. Overwrites them if needed.

Only abstract classes can be subclassed.

Since relation fields requires different related_name for different children


**Raises**:

- `ModelDefinitionError`: if non abstract model is subclassed

**Arguments**:

- `base_class` (`Model or model parent class`): one of the parent classes
- `curr_class` (`Model or model parent class`): current constructed class
- `attrs` (`Dict`): new namespace for class being constructed
- `model_fields` (`Dict[str, BaseField]`): ormar fields in defined in current class

**Returns**:

`Tuple[Dict, Dict]`: updated attrs and model_fields

<a name="models.metaclass.extract_from_parents_definition"></a>
#### extract\_from\_parents\_definition

```python
extract_from_parents_definition(base_class: type, curr_class: type, attrs: Dict, model_fields: Dict[str, Union[BaseField, ForeignKeyField, ManyToManyField]]) -> Tuple[Dict, Dict]
```

Extracts fields from base classes if they have valid ormar fields.

If model was already parsed -> fields definitions need to be removed from class
cause pydantic complains about field re-definition so after first child
we need to extract from __parsed_fields__ not the class itself.

If the class is parsed first time annotations and field definition is parsed
from the class.__dict__.

If the class is a ormar.Model it is skipped.

**Arguments**:

- `base_class` (`Model or model parent class`): one of the parent classes
- `curr_class` (`Model or model parent class`): current constructed class
- `attrs` (`Dict`): new namespace for class being constructed
- `model_fields` (`Dict[str, BaseField]`): ormar fields in defined in current class

**Returns**:

`Tuple[Dict, Dict]`: updated attrs and model_fields

<a name="models.metaclass.update_attrs_and_fields"></a>
#### update\_attrs\_and\_fields

```python
update_attrs_and_fields(attrs: Dict, new_attrs: Dict, model_fields: Dict, new_model_fields: Dict, new_fields: Set) -> Dict
```

Updates __annotations__, values of model fields (so pydantic FieldInfos)
as well as model.Meta.model_fields definitions from parents.

**Arguments**:

- `attrs` (`Dict`): new namespace for class being constructed
- `new_attrs` (`Dict`): related of the namespace extracted from parent class
- `model_fields` (`Dict[str, BaseField]`): ormar fields in defined in current class
- `new_model_fields` (`Dict[str, BaseField]`): ormar fields defined in parent classes
- `new_fields` (`Set[str]`): set of new fields names

<a name="models.metaclass.add_field_descriptor"></a>
#### add\_field\_descriptor

```python
add_field_descriptor(name: str, field: "BaseField", new_model: Type["Model"]) -> None
```

Sets appropriate descriptor for each model field.
There are 5 main types of descriptors, for bytes, json, pure pydantic fields,
and 2 ormar ones - one for relation and one for pk shortcut

**Arguments**:

- `name` (`str`): name of the field
- `field` (`BaseField`): model field to add descriptor for
- `new_model` (`Type["Model]`): model with fields

<a name="models.metaclass.ModelMetaclass"></a>
## ModelMetaclass Objects

```python
class ModelMetaclass(pydantic.main.ModelMetaclass)
```

<a name="models.metaclass.ModelMetaclass.__new__"></a>
#### \_\_new\_\_

```python
 | __new__(mcs: "ModelMetaclass", name: str, bases: Any, attrs: dict) -> "ModelMetaclass"
```

Metaclass used by ormar Models that performs configuration
and build of ormar Models.


Sets pydantic configuration.
Extract model_fields and convert them to pydantic FieldInfo,
updates class namespace.

Extracts settings and fields from parent classes.
Fetches methods decorated with @property_field decorator
to expose them later in dict().

Construct parent pydantic Metaclass/ Model.

If class has Meta class declared (so actual ormar Models) it also:

* populate sqlalchemy columns, pkname and tables from model_fields
* register reverse relationships on related models
* registers all relations in alias manager that populates table_prefixes
* exposes alias manager on each Model
* creates QuerySet for each model and exposes it on a class

**Arguments**:

- `name` (`str`): name of current class
- `bases` (`Tuple`): base classes
- `attrs` (`Dict`): class namespace

<a name="models.metaclass.ModelMetaclass.__getattr__"></a>
#### \_\_getattr\_\_

```python
 | __getattr__(item: str) -> Any
```

Returns FieldAccessors on access to model fields from a class,
that way it can be used in python style filters and order_by.

**Arguments**:

- `item` (`str`): name of the field

**Returns**:

`FieldAccessor`: FieldAccessor for given field

