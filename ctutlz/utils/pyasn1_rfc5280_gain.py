from pyasn1.codec.der.encoder import encode as der_encoder
from pyasn1_modules import rfc5280
from utlz import flo, namedtuple

from ctutlz.utils.logger import logger
from ctutlz.utils.string import string_without_prefix


RelativeDistinguishedName = namedtuple(
   typename='RelativeDistinguishedName',
    field_names='pyasn1',
    lazy_vals={
        '_attr_type_and_val': lambda self:
            self.pyasn1.getComponentByPosition(0),
        'type': lambda self: str(self._attr_type_and_val['type']),
        'value': lambda self:
            # string_without_prefix('\x13\x02',
            #                       str(self._attr_type_and_val['value'])),
            str(self._attr_type_and_val['value'])[2::],

        'type_str': lambda self:
            # https://tools.ietf.org/html/rfc4514#section-3
            # commonName
            'CN'     if self.type == '2.5.4.3'  else  # noqa: E272
            # localityName
            'L'      if self.type == '2.5.4.7'  else  # noqa: E272
            # stateOrProvinceName
            'ST'     if self.type == '2.5.4.8'  else  # noqa: E272
            # organizationName
            'O'      if self.type == '2.5.4.10' else  # noqa: E272
            # organizationalUnitName
            'OU'     if self.type == '2.5.4.11' else  # noqa: E272
            # countryName
            'C'      if self.type == '2.5.4.6'  else  # noqa: E272
            # streetAddress
            'STREET' if self.type == '2.5.4.9'  else  # noqa: E272
            # domainComponent
            'DC'     if self.type == '0.9.2342.19200300.100.1.25' else  # noqa: E272
            # userId
            'UID'    if self.type == '0.9.2342.19200300.100.1.1' else  # noqa: E272

            (logger.error(flo('unknown type {self.type}')), self.type)[-1],

        'str': lambda self: flo('{self.type_str}={self.value}'),

        '__str__': lambda self: lambda: self.str,  # __str__ returns a callable
    }
)


Name = namedtuple(
    typename='Name',
    field_names=['pyasn1'],
    lazy_vals={
        'str': lambda self: ','.join([str(RelativeDistinguishedName(rdn))
                                      for rdn
                                      in self.pyasn1['rdnSequence']]),

        '__str__': lambda self: lambda: self.str,  # __str__ returns a callable
    }
)