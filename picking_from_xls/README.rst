
======================
Stock Picking From XLS
======================

This allows to make internal transfers from an excel file, with the following structure


+-----------+------------------+-------------+-----+
|SKU        |NAME              |DESCRIPTION  |QTY  |
+===========+==================+=============+=====+
|IN1010201  |Blue Cheese XXX   |ADJUSTMENT   |   1 |
+-----------+------------------+-------------+-----+
|IN1010301  |Barbacue beef     |CHECK        |  20 |
+-----------+------------------+-------------+-----+

The "SKU" must match as default_code field in products.
The values you put at column "NAME" are not taken in account by the transfer.
"QUANTITY" is the quantity in the product unit set at the product record.

Installation
============

Multiple warehouses must be checked in inventory configuration.
Install the module.
Once installed, go to inventory board and choose a picking of type 'internal'. You will see a place in the header
of the picking where you can upload the excel file.
Inmmediatly, the products will be injected in the move lines. Then you can save the picking, and follow the natural flow
in Odoo.

.. image:: /picking_from_xls/static/description/stock_operation.png
   :alt: Operations configuration Graphic
   :width: 600


Negative values in quantity
---------------------------

This addon does not support negative values, so, if you want to use it to adjust inventory, you must create two types
of internal operations, for example:
1) from WH to adjustment (to decrement stock)
2) from adjustment to WH (to increment stock)



Dependencies
------------

Known issues / Roadmap
======================

Credits
=======

Blanco Martín & Asociados - Odoo Silver Partner 2018.

Contributors
------------

* BMyA Developement Task Force: <dev@blancomartin.cl>
* Daniel Blanco <daniel@blancomartin.cl>



Maintainer
==========

Blanco Martín & Asociados - Odoo Silver Partner 2018.

.. image:: https://blancomartin.cl/logo.png
   :alt: Blanco Martin y Asociados' logo
   :target: https://blancomartin.cl


This module is maintained by Blanco Martín & Asociados.

To contribute to this module, please visit https://blancomartin.cl.

License
-------

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.
