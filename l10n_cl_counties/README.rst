.. image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
   :target: http://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3


================
l10n_cl_counties
================

New module for Chilean locations
--------------------------------
Odoo 13.0, in its base implementation, has incorporated the 16 regions of Chile, which can be selected through the
"State" field. The "City" field has been reserved to place the "comunas" (counties) information in it, for simplicity
and taking into account that the value it acquires from the communes, despite being mandatory in the Electronic
invoicing is not a field that has to contain a value controlled by the SII. However, aware of the importance of
communes in the geopolitical specification of Chile, we have modified this new version of our module,
(which exists since version 8.0) to maintain full compatibility with the new Odoo 13.0 implementation.

It contains:
- 346 communes (counties), from Aysén to Zapallar.
- 68 additional records which includes the head cities and the relation between them and regions.
We have not included the provinces for simplicity and being a less used value.

Internally, this module copies the commune value over the city field, making it compatible with the future electronic
invoice implementation of Odoo.

Nuevo Módulo para Ubicaciones Geográficas en Chile
--------------------------------------------------
Odoo 13.0, en su implementación base, ha incorporado las 16 regiones de Chile, las cuales pueden ser seleccionadas
mediante el campo "Estado" y se ha reservado el campo "Ciudad" para colocar en éste la información de las comunas,
por simplicidad y tomando en cuenta que el valor que adquiere de las comunas, a pesar de ser obligatorio en la
facturación electrónica, no es un campo que tenga que contener un valor controlado por el SII.
Sin embargo, Concientes de lo importante que son las comunas en la especificación geopolítica de Chile, hemos modificado
esta nueva versión de nuestro módulo, (el cual existe desde la versión 8.0) para que mantenga total compatibilidad con
la nueva modalidad de implementación de Odoo 13.0

Contiene:
- 346 comunas, desde Aysén hasta Zapallar
- 68 registros adicionales que incluyen, las ciudades cabecera y la relación de las mismas con las regiones.
No se incluyen las provincias por simplicidad, siendo un valor que es menos utilizado.

Internamente, este módulo copia el valor de la comuna sobre el campo "city", haciéndolo compatible con la implementación
de facturación electrónica de Odoo, que estará disponible en breve.


=======
Credits
=======

Authors:
Blanco Martín & Asociados


Contributors
------------

* BMyA Development Task Force: <dev@blancomartin.cl>
* Daniel Blanco <daniel@blancomartin.cl>

Maintainer
----------

.. image:: https://blancomartin.cl/logo.png
   :alt: Blanco Martin y Asociados' logo
   :target: https://blancomartin.cl


This module is maintained by Blanco Martín & Asociados.

To contribute to this module, please visit https://blancomartin.cl.
