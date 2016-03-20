
#English

Odoo - Localización Chilena
===========================

## Description

Maintenance system for folios authorization codes (CAF) files for Chilean Electronic Tax Documents (DTEs)


## Installation
 
### Dependencies


## Contributing
We follow these guidelines and advice:

1. Fork this project.
2. Create your feature branch: `git checkout -b my-enhancements-or-features`
3. Commit your changes: `git commit -am 'Add my own enhacements or features'`
4. Push to the branch: `git push origin my-enhancements-or-features`
5. Submit a pull request to us (y)

## Credits
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.

#Spanish

Odoo - Localización Chilena
===========================

## Descripción

Sistema para mantenimiento de archivos de códigos de autorización de folios (CAF) para Documentos Tributarios Electrónicos (DTEs) de Chile

## Instalación
 
### Dependencias

## Propuesta para armado de Módulos relativos a WebServices SII

Se basa en el siguiente link del SII:

http://www.sii.cl/factura_electronica/formato_xml.htm


Estructura Propuesta para Módulos de Odoo - WS Sii
--------------------------------------------------

dte_caf
-------
Bajar schema XML de Archivo de Consumo de Folios
Bajar descripción del formato del Archivo de Consumo de Folios

dte_wssii
---------
Documentos Tributarios Electrónicos:

Bajar schema XML de Documentos Tributarios Electrónicos (Incluye Documentos de exportación)
Bajar diagrama de schema XML de Documentos Tributarios Electrónicos
Ejemplo XML de Documentos Tributarios Electrónicos

dte_wssii(?)
------------
Boletas Electrónicas

Bajar schema XML de Boletas Electrónicas
Bajar diagrama de schema XML de Boletas Electrónicas
Bajar descripción del formato de Boletas Electrónicas


dte_gd
------
Libro de Guías de Despacho Electrónicas:
Bajar Schema XML de Libro de Guías de Despacho Electrónicas
Bajar Diagrama de Schema XML de Libro de Guías de Despacho Electrónicas

dte_exchange
------------
Intercambio entre Contribuyentes:

Bajar schema XML de Intercambio entre Contribuyentes
Bajar diagrama de schema XML de Intercambio entre Contribuyentes
Bajar descripción del formato de Intercambio entre Contribuyentes

dte_rec
-------
Recibo de las Mercaderías o Servicios prestados, según Ley 19.983:

Bajar schema XML de Recibo ley 19.983
Bajar diagrama de schema XML de Recibo ley 19.983
Bajar descripción del formato del 19.983


????? ()
-----
Respuesta SII a Envíos Automáticos:

Bajar schema XML de Respuesta SII a Envíos Automáticos
Bajar diagrama de schema XML de Respuesta SII a Envíos Automáticos

Bajar schema Respuesta SII a Envíos Automáticos de Libros
Bajar diagrama de schema de Respuesta SII a Envíos Automáticos de Libros




Los módulos de libros de compras y ventas, son dependientes de account_vat_ledger,
puesto que son módulos que heredan de ellos y agregan una pestaña para lograr la funcionalidad
buscada.

	account_vat_ledger_iecv
	-----------------------
	Información Electrónica de Compras y Ventas:

	Bajar schema XML de Información Electrónica de Compras y Ventas
	Bajar diagrama de schema XML de Información Electrónica de Compras y Ventas

	account_vat_ledger_be
	---------------------
	Libro de Boletas Electrónicas

	Bajar schema XML de Libro de Boletas Electrónicas
	Bajar diagrama de schema XML de Libro Boletas Electrónicas
	Bajar descripción del formato del Libro de Boletas Electrónicas
	Archivo de Consumo de Folios




## Cómo contribuir
Seguimos estas lineas básicas y recomendaciones:

1. Haga un `Fork` de este proyecto.
2. Cree su propia rama con características: `git checkout -b mis-mejoras-o-caracteristicas`
3. Haga `Commit` de sus cambios: `git commit -am 'Agrego mis propias mejoras o características'`
4. Haga `Push` a su rama: `git push origin mis-mejoras-o-caracteristicas`
5. Envíenos un `pull request` para que incorporemos sus mejoras al proyecto principal

## Créditos
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl

## Licencia

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License along with this program. If not, see http://www.gnu.org/licenses/.