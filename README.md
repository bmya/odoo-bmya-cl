# l10n_cl_pos_basic_users

Odoo - Chilean Localization POS Basic Users
===========================================

This module simplificates terminology for a commerce using POS. This is a module intended for a very closed
mind user, who for example does not understand that "BOLETA" is almost the same thing that a "FACTURA". Or for guys
who use to mix payment type with tax document type, and that does not understand what a different "tax payer category"
is. (1st, 2nd, etc).

## Dependencies
l10n_cl_invoice

## Credits
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl

 
Odoo - Usuarios de POS básicos para Localización Chilena
=========================================================

Este módulo simplifica la terminología para un comercio que usa TPV (Terminal punto de venta o POS).
Intenta ayudar, ante un usuario de mente cerrada, que por ejemplo no entiende que una "BOLETA" y una "FACTURA" son
intrínsecamente - (o al menos para Odoo) - la misma cosa. O para usuarios que mezclan tipos de pago con tipos de documentos
tributarios, y no entienden qué significa una categoría de contribuyente (1ra, segunda, etc).

Modifica el nombre del partner "Consumidor Final" a CLIENTE BOLETA. seleccionando automáticamente para este tipo de cliente la emisión de 
un documento "BOLETA".

Crea además el documento tributario (inexistente como tal) denominado "nota de venta", el cual se destina a reflejar las ventas
que fueron emitidas mediante un voucher de tarjeta de crédito, para evitar declarar dos veces el comprobante como boleta.

Crea la entidad (partner) CLIENTE TARJETA (contribuyente final destinado a ventas con tarjeta). Cuando se selecciona este cliente, el sistema emitirá una nota de venta en lugar de una boleta.
Con esta finalidad, el módulo trabaja en conjunto con el l10n_cl_pos_credit_card_voucher. Esta característica se usa al imprimir boletas/facturas
en impresoras de matriz de puntos y no en impresoras fiscales, o electrónicas.

Modifica o crea relaciones necesarias en módulos de cl_invoice, para hacer correctamente las cosas con este tipo de documento (nota de venta)
el cual en definitiva, sólo se usa para poder registrar en Odoo los movimientos, sin reflejar el mismo en el libro de ventas, ya que 
habría duplicidad de tributo y se inclumpliría la resolución 05 / 2015 del SII.

(Ver los siguientes links:
http://www.sii.cl/portales/ticketporboleta/index.html
http://www.sii.cl/documentos/resoluciones/2015/reso05.pdf
)


## Dependencies
l10n_cl_invoice

## Créditos
<p>
<img alt="Logo BMYA" src="http://crm.blancomartin.cl/index.php?entryPoint=image&name=c82ab43f-e8dd-b2fa-25ff-56017f69d116" />
</p>
**Blanco Martin & Asociados EIRL** - http://blancomartin.cl
