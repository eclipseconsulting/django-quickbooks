from django_quickbooks import QUICKBOOKS_ENUMS
from django_quickbooks.services.base import Service
from django_quickbooks.utils import xml_setter


class CustomerService(Service):
    complex_fields = ['BillAddress', 'ShipAddress']

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, object)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, object)

    def all(self):
        return self._all(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER)

    def find_by_id(self, id):
        return self._find_by_id(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, id)

    def find_by_full_name(self, full_name):
        return self._find_by_full_name(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, full_name)


class EclipseCustomerService(CustomerService):
    complex_fields = ['BillAddress', 'ShipAddress']
    custom_fields = {'CUSTFLD1': 'billing_preference', 'CUSTFLD4': 'special_instructions', 'CUSTFLD6': 'price_level',
                     'CUSTFLD7': 'id'}

    def _cust_fields(self, object):
        xml = ''
        for custom_field in self.custom_fields:
            if hasattr(object, self.custom_fields[custom_field]):
                xml += f'''<DataExtModRq>
                                    <DataExtMod>
                                        <OwnerID>0</OwnerID>
                                        <DataExtName>{custom_field}</DataExtName>
                                        <ListDataExtType>Customer</ListDataExtType>
                                        <ListObjRef>
                                                <FullName>{object.name}</FullName>
                                        </ListObjRef>
                                        <DataExtValue>{getattr(object, self.custom_fields[custom_field])}</DataExtValue>
                                    </DataExtMod>
                                </DataExtModRq>
                                '''
        return xml

    def _add(self, resource, object):
        qbd = object.to_qbd_obj()
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_ADD + 'Rq', qbd.as_xml(
            opp_type=QUICKBOOKS_ENUMS.OPP_ADD, ref_fields=self.ref_fields, change_fields=self.add_fields,
            complex_fields=self.complex_fields))

        xml += self._cust_fields(object)
        return self._prepare_request(xml)

    def add(self, object):
        return self._add(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, object)

    def _update(self, resource, object):
        qbd = object.to_qbd_obj()
        xml = ''
        xml += xml_setter(resource + QUICKBOOKS_ENUMS.OPP_MOD + 'Rq', qbd.as_xml(
            opp_type=QUICKBOOKS_ENUMS.OPP_MOD, ref_fields=self.ref_fields, change_fields=self.mod_fields,
            complex_fields=self.complex_fields))

        xml += self._cust_fields(object)
        return self._prepare_request(xml)

    def update(self, object):
        return self._update(QUICKBOOKS_ENUMS.RESOURCE_CUSTOMER, object)
