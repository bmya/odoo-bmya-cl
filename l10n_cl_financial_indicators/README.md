[![Build Status](https://travis-ci.org/odoo-chile/l10n_cl_financial_indicators.svg)](https://travis-ci.org/odoo-chile/l10n_cl_financial_indicators)
[![Coverage Status](https://coveralls.io/repos/odoo-chile/l10n_cl_financial_indicators/badge.svg?branch=8.0&service=github)](https://coveralls.io/github/odoo-chile/l10n_cl_financial_indicators?branch=8.0)
[![Code Climate](https://codeclimate.com/github/odoo-chile/l10n_cl_financial_indicators/badges/gpa.svg)](https://codeclimate.com/github/odoo-chile/l10n_cl_financial_indicators)

l10n_cl_financial_indicators

#English

Odoo - Update Chilean Financial Indicators
==========================================

## Description

Module that updates the following indicators used in Chile for Odoo
sofware:

Dollar
Euro
UF
UTM

It connects to SBIFs webservices. 

## Installation

Prior to use, you must get your
own apikey from this webpage:

An then replace it at:

apikey.py
(rename apikey.py.sample to apikey.py and include your own api key there)

You must also have the following these currency values loaded in your 
system, using the following Id for each one:

USD
EUR
UF
UTM

If the spell is not the same, this implementation won't be able to find
the currencies or the indexes to update.
 
### Dependencies

    sudo pip install -r requirements.txt

If you don't have Pip, find it here: http://pypi.python.org/pypi/pip

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

Actualizador de indices financieros chilenos para Odoo
======================================================

## Descripción

Este módulo de Odoo, actualiza los siguientes indicadores usados en Chile:

Dolar
Euro
UF
UTM

Se conecta a los webservices provistos por la Superintendencia de Bancos
e Instituciones Financieras de Chile - SBIF, para obtener los valores 
oficiales del día.

## Instalación

Previo al uso, Ud. debe obtener su propia clave de API
desde esta página web:

http://api.sbif.cl/api/contactanos.jsp

Y entonces, reemplazar la misma en:

apikey.py

(renombra apikey.py.sample a apikey.py e incluye allí tu propia clave api)

Ud. deberá tener las siguientes monedas ingresadas en su sistema Odoo,
utilizando la siguiente identificación para las mismas:

USD
EUR
UF
UTM

Si la nomenclatura no es exactamente la misma, esta implementacion
no podrá encontrar las monedas para ser actualizadas.
 
### Dependencias

    sudo pip install -r requirements.txt

If you don't have Pip, find it here: http://pypi.python.org/pypi/pip

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
