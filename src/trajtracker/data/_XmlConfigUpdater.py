
import inspect
import xml.etree.ElementTree as ET

from trajtracker import _TTrkObject, BadFormatError


class XmlConfigUpdater(_TTrkObject):
    """

    """

    def __init__(self):
        super(XmlConfigUpdater, self).__init__()


    #--------------------------------------------------
    def configure_objects(self, xml, objects, xml_source):

        for one_obj_config in xml:
            obj_id = one_obj_config.tag

            #-- Make sure that this object in fact exists
            if obj_id not in objects:
                raise BadFormatError("Invalid xml configuration in {:} (<'{:}' ...>): there is no object to configure named {:}".format(
                    xml_source, obj_id, obj_id))

            self.configure_object(one_obj_config, objects[obj_id])


    #--------------------------------------------------
    def configure_object(self, xml, obj):

        #-- Update by XML attributes
        for attr_name in xml.attrib:
            self._validate_attr(obj, attr_name)
            setattr(obj, attr_name, _ValueFromXML(xml.tag, xml.attrib[attr_name]))

        #-- Update by XML elements: this must be done via functions
        for sub_element in xml:
            self._validate_attr(obj, sub_element.tag)
            setattr(obj, sub_element.tag, _ValueFromXML(xml.tag, sub_element))


    #--------------------------------------------------
    def _validate_attr(self, obj, attr_name):
        try:
            setattr(obj, attr_name, _TestIfXmlSupported())
            raise BadFormatError('Invalid XML configuration: {:}.{:} cannot be configured from XML'.format(type(obj).__name__, attr_name))
        except _TestIfXmlSupported:
            pass


#==================================================================
# Annotations to define on the class
#==================================================================


#------------------------------------------------------------------------------------
# When setting attribute value from XML, we set it to this value
#
class _ValueFromXML(object):
    def __init__(self, tag, value):
        self.tag = tag
        self.value = value


class _TestIfXmlSupported(Exception):
    pass




#------------------------------------------------------------------------------------
# Actually convert the value from the XML (string if it was an attribute; or an XML Element) to the
# target object's expected attribute value
#
def _convert_xml_value_to_attr_value(obj, attr_name, xml_value, converter, convert_raw_xml):

    value = xml_value.value

    if convert_raw_xml:
        #-- Make sure that we got the XML node
        if not isinstance(xml_value.value, ET.Element):
            BadFormatError(
                'Invalid XML configuration <{:} ...>: to configure {:}.{:} via XML, you must define a sub-block'.format(
                xml_value.tag, type(obj).__name__, attr_name))

    elif isinstance(xml_value.value, ET.Element):
        #-- We got the XML element (node), but we need its text value
        value = xml_value.value.text.strip()

    return converter(value)


#------------------------------------------------------------------------------------
# The annotation
#
# noinspection PyPep8Naming
def fromXML(converter, raw_xml=False):

    #-- Define the real decorator
    def real_decorator(setter):

        #-- Create a setter for the attribute
        def set_attr_from_xml(self, value):
            if isinstance(value, _ValueFromXML):
                setter(self, _convert_xml_value_to_attr_value(self, setter.__name__, value, converter, raw_xml))
            elif isinstance(value, _TestIfXmlSupported):
                raise _TestIfXmlSupported()
            else:
                setter(self, value)

        return set_attr_from_xml

    return real_decorator

