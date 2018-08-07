from collections import OrderedDict
import json
from graphenebase.types import (
    Uint8, Int16, Uint16, Uint32, Uint64,
    Varint32, Int64, String, Bytes, Void,
    Array, PointInTime, Signature, Bool,
    Set, Fixed_array, Optional, Static_variant,
    Map, Id, VoteId, ObjectId,
    JsonObj
)
from .chains import known_chains
from .objecttypes import object_type
from .account import PublicKey
from .chains import default_prefix
from .operationids import operations, ops


class Operation():
    """ The superclass for an operation. This class i used to instanciate an
        operation, identify the operationid/name and serialize the operation
        into bytes.
    """
    def __init__(self, op):
        self.op = GrapheneObject()

        # Are we dealing with an actual operation as list of opid and payload?
        if isinstance(op, list) and len(op) == 2:
            self._setidanename(op[0])
            self.set(**op[1])

        # Here, we allow to only load the Operation as Template without data
        elif isinstance(op, str) or isinstance(op, int):
            self._setidanename(op)

        else:
            raise ValueError("Unknown format for Operation()")

    def set(self, **data):
        try:
            klass = self.klass()
        except Exception:
            raise NotImplementedError("Unimplemented Operation %s" % self.name)
        self.op = klass(**data)

    def _setidanename(self, identifier):
        if isinstance(identifier, int):
            self.id = int(identifier)
            assert len(ops) > self.id
            self.name = ops[self.id]
        else:
            assert identifier in self.operations()
            self.id = self.operations()[identifier]
            self.name = identifier

    @property
    def opId(self):
        return self.id

    @property
    def klass_name(self):
        return self.name[0].upper() + self.name[1:]  # klassname

    def operations(self):
        # This returns the 'operations' as loaded into global namespace
        # which is ugly like shit!
        return operations

    def _getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in self.operations():
            if int(self.operations()[key]) is int(i):
                return key
        return "Unknown Operation ID %d" % i

    def klass(self):
        module = __import__("graphenebase.operations", fromlist=["operations"])
        class_ = getattr(module, self.klass_name)
        return class_

    def __bytes__(self):
        return bytes(Id(self.id)) + bytes(self.op)

    def __str__(self):
        return json.dumps(self.__json__())

    def __json__(self):
        return [self.id, self.op.json()]

    toJson = __json__
    json = __json__


class GrapheneObject(OrderedDict):
    """ Core abstraction class

        This class is used for any JSON reflected object in Graphene.

        * ``instance.__json__()``: encodes data into json format
        * ``bytes(instance)``: encodes data into wire format
        * ``str(instances)``: dumps json object as string

    """
    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], dict):
            if hasattr(self, "detail"):
                super().__init__(self.detail(**args[0]))
            else:
                OrderedDict.__init__(self, args[0])
            return

        elif len(args) == 1 and isinstance(args[0], OrderedDict):
            if hasattr(self, "detail"):
                super().__init__(self.detail(**args[0]))
            else:
                OrderedDict.__init__(self, args[0])
            return

        elif kwargs and hasattr(self, "detail"):
            # If I receive kwargs, I need detail() implemented!
            super().__init__(self.detail(*args, **kwargs))

    def __bytes__(self):
        if len(self) is 0:
            return bytes()
        b = b""
        for name, value in self.items():
            if isinstance(value, str):
                b += bytes(value, 'utf-8')
            else:
                b += bytes(value)
        return b

    def __json__(self):
        if len(self) is 0:
            return {}
        d = {}  # JSON output is *not* ordered
        for name, value in self.items():
            if isinstance(value, Optional) and value.isempty():
                continue

            if isinstance(value, String):
                d.update({name: str(value)})
            else:
                try:
                    d.update({name: JsonObj(value)})
                except Exception:
                    d.update({name: value.__str__()})
        return d

    def __str__(self):
        return json.dumps(self.__json__())

    @property
    def data(self):
        return self

    toJson = __json__
    json = __json__


# Legacy
def isArgsThisClass(self, args):
    return (len(args) == 1 and type(args[0]).__name__ == type(self).__name__)
