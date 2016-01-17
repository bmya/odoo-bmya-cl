[![Build Status](https://travis-ci.org/odoo-chile/l10n_cl_financial_indicators.svg)](https://travis-ci.org/odoo-chile/l10n_cl_financial_indicators)
[![Coverage Status](https://coveralls.io/repos/odoo-chile/l10n_cl_financial_indicators/badge.svg?branch=8.0&service=github)](https://coveralls.io/github/odoo-chile/l10n_cl_financial_indicators?branch=8.0)
[![Code Climate](https://codeclimate.com/github/odoo-chile/l10n_cl_financial_indicators/badges/gpa.svg)](https://codeclimate.com/github/odoo-chile/l10n_cl_financial_indicators)


Odoo - Update Chilean Financial Indicators
==========================================

Module that updates the following indicators used in Chile for Odoo
sofware:

Dollar
Euro
UF
UTM

It connects to SBIFs webservices. Prior to use, you must get your
own apikey from this webpage:

#Version 1.0

##Enhancementes of this version
##-----------------------------
1) Ensure that base currency is set to CLP
2) Adds UF y UTM as currencies. In case they have been deleted, it also adds USD and EUR
3) Allow to manage update of each currency manually.
4) It makes calculation with needed precision.
5) Dependency: this module depends on a generic webservices module, which acts as a repository for more webservices (webservices_generic)
webservices_generic allows to add several kind of webservices you could need inside Odoo.


##ToDo 
##-----
1) Launch a wizard when installed, so that you can add your SBIF apikey just once.


##Important!
##-----------------------------
If you are upgrading from previous version, we advice to delete UF and UTM. This way the external reference name
will be correctly established.

You should also install these modules for better experience:
	account_invoice_prices_update (purchases)
	base_currency_inverse_rate (to see the inverse rate, which is always more familiar to your brain)


Currency or pseudo/currencies updated by the module:
	USD, EUR, UF, UTM

## Credits
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl

 
Actualizador de indices financieros chilenos para Odoo
======================================================

Este módulo de Odoo, actualiza los siguientes indicadores usados en Chile:

Dolar
Euro
UF
UTM

Se conecta a los webservices provistos por la Superintendencia de Bancos
e Instituciones Financieras de Chile - SBIF, para obtener los valores 
oficiales del día.
Previo al uso, Ud. debe obtener su propia clave de API
desde esta página web:

http://api.sbif.cl/api/contactanos.jsp

Monedas que actualiza:
	USD, EUR, UF, UTM

Si la nomenclatura no es exactamente la misma, esta implementacion
no podrá encontrar las monedas para ser actualizadas.

#Versión 1.0

##Mejoras realizadas en el módulo
##-------------------------------
1) Asegura que esté la moneda contable (CLP) es la moneda base.
2) ingresa UF y UTM como monedas. En caso que no estén ingresa también USD y EUR
3) permite manejar la actualización de cada una de las monedas manualmente
4) realiza el cálculo de manera correcta. (OK)
5) mejora: se incorporó un repositorio de webservices. (webservices_generic)
La idea es que este módulo sirva como repositorio de servidores para diferentes servicios que se quieran incorporar a Odoo.


##Mejoras Para hacer
##------------------
1) Que lance un asistente (wizard) cuando se instale, de manera que permita el ingreso de la clave api del 
SBIF sólo una vez.

##Recomendaciones (Importante!)
##-----------------------------
Eliminar las monedas UF y UTM si ya las tienen ingresadas de antes, para que tome las referencias correctas.
Instalar además los siguientes módulos:
	account_invoice_prices_update (para compras)
	base_currency_inverse_rate (para poder ver los rates de monedas en fórmula inversa)

 
## Credits
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl
