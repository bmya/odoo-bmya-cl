��          �      ,      �  �  �  �  @  �  
  �     d  �
  �         �  
   �     �  �   �     �  ;   �  @      /   A     q     }  f  �  �  �  �  �  �  w  �  j  �    �   �&      E'     f'     u'  �   �'     j(  ;   r(  @   �(  /   �(     )     +)     
         
                   	                                             
            
                <header>
                <strong>Facturación Electrónica - Acuse de Recibo de Envio de DTE ${object.name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar el resultado del proceso de revisión y
                validación de un envío de Documentos Tributarios Electronicos que Usted
                realizó.</p>
                <br />
                <p>Esta es una aplicación automática, por lo tanto no conteste este correo ni
                haga consultas o comentarios a la dirección de origen.</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Aceptación Comercial - ${object.display_name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar la respuesta de aceptación comercial
                de su(s) Documento(s) Tributarios Electronico(s).</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Recepción de Mercaderías - ${object.display_name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar la respuesta de recepción de mercaderías o servicios
                correspondientes a su(s) Documento(s) Tributarios Electronico(s).</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Rechazo Comercial ${object.name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar el resultado del proceso de revisión y
                rechazo de un envío de Documentos Tributarios Electronicos que Usted
                realizó.</p>
                <br />
                <p>Esta es una aplicación automática, por lo tanto no conteste este correo ni
                haga consultas o comentarios a la dirección de origen.</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            <div>
                <p>Dear ${object.partner_id.name}
                % set access_action = object.with_context(force_website=True).get_access_action()
                % set is_online = access_action and access_action['type'] == 'ir.actions.act_url'
                % set access_url = object.get_mail_url()

                % if object.partner_id.parent_id:
                    (<i>${object.partner_id.parent_id.name}</i>)
                % endif
                ,</p>
                <p>Here is, in attachment, your
                % if object.number:
                invoice <strong>${object.number}</strong>
                % else:
                invoice
                % endif
                % if object.origin:
                (with reference: ${object.origin})
                % endif
                amounting in <strong>${format_amount(object.amount_total, object.currency_id)}</strong>
                from ${object.company_id.name}.
                </p>

                % if is_online:
                    <br><br>
                    <center>
                      <a href="${object.docs_online_token}" style="background-color: #1abc9c; padding: 20px; text-decoration: none; color: #fff; border-radius: 5px; font-size: 16px;" class="o_default_snippet_text">View Invoice</a>
                    </center>
                % endif
                    <br><br>

                % if object.state=='paid':
                    <p>This invoice is already paid.</p>
                % else:
                    <p>Please remit payment at your earliest convenience.</p>
                % endif

                <p>Thank you,</p>
                <p style="color:#888888">
                % if object.user_id and object.user_id.signature:
                    ${object.user_id.signature | safe}
                % endif
                </p>
                </div>
             ${(object.company_id.partner_id.ref|safe or object.company_id.partner_id.name|safe)} DTE (Ref ${(object.display_name or 'n/a')}) Acuse de Recibo - ${object.name} Compose Email Imprimir PDF Imprimir PDF desde Documentos Online. ATENCION!                         Si Ud. envía un documento no                         aprobado por el SII, puede estar incurriendo                         en una irregularidad administrativa. Invoice Respuesta de Aceptación Comercial - ${object.display_name} Respuesta de Recepción de Mercaderías - ${object.display_name} Respuesta de Rechazo Comercial - ${object.name} URL Factura sii.send_queue Project-Id-Version: Odoo Server 11.0+e-20180814
Report-Msgid-Bugs-To: 
POT-Creation-Date: 2018-09-27 20:53+0000
PO-Revision-Date: 2018-09-27 17:58-0300
Language-Team: 
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n != 1);
X-Generator: Poedit 2.1.1
Last-Translator: 
Language: es
 
            
                <header>
                <strong>Facturación Electrónica - Acuse de Recibo de Envio de DTE ${object.name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar el resultado del proceso de revisión y
                validación de un envío de Documentos Tributarios Electronicos que Usted
                realizó.</p>
                <br />
                <p>Esta es una aplicación automática, por lo tanto no conteste este correo ni
                haga consultas o comentarios a la dirección de origen.</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Aceptación Comercial - ${object.display_name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar la respuesta de aceptación comercial
                de su(s) Documento(s) Tributarios Electronico(s).</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Recepción de Mercaderías - ${object.display_name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar la respuesta de recepción de mercaderías o servicios
                correspondientes a su(s) Documento(s) Tributarios Electronico(s).</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            
                <header>
                <strong>Facturación Electrónica - Respuesta de Rechazo Comercial ${object.name}</strong>
                </header>
                <p>En el archivo adjunto puede encontrar el resultado del proceso de revisión y
                rechazo de un envío de Documentos Tributarios Electronicos que Usted
                realizó.</p>
                <br />
                <p>Esta es una aplicación automática, por lo tanto no conteste este correo ni
                haga consultas o comentarios a la dirección de origen.</p>
                <br /><br /><br /><br />
                <p>Enviado Usando Odoo</p>
            
             
            <div>
                <p>Estimado(s) ${object.partner_id.name}
                % set access_action = object.with_context(force_website=True).get_access_action()
                % set is_online = access_action and access_action[‘type’] == ‘ir.actions.act_url’
                % set access_url = object.get_mail_url()

                % if object.partner_id.parent_id:
                    (<i>${object.partner_id.parent_id.name}</i>)
                % endif
                ,</p>
                <p>Aqui encontrarán en adjunto su
                % if object.number:
                factura <strong>${object.number}</strong>
                % else:
                factura
                % endif
                % if object.origin:
                (con referencia: ${object.origin})
                % endif
                por un monto de <strong>${format_amount(object.amount_total, object.currency_id)}</strong>
                originada por ${object.company_id.name}.
                </p>

                % if is_online:
                    <br><br>
                    <center>
                      <a href=“${object.docs_online_token}” style=“background-color: #1abc9c; padding: 20px; text-decoration: none; color: #fff; border-radius: 5px; font-size: 16px;” class=“o_default_snippet_text”>Ver Factura en www.documentosonline.cl</a>
                    </center>
                % endif
                    <br><br>

                % if object.state==‘paid’:
                    <p>Esta factura ya se encuentra pagada.</p>
                % else:
                    <p>Quedamos a la espera de su pago.</p>
                % endif

                <p>Gracias,</p>
                <p style=“color:#888888”>
                % if object.user_id and object.user_id.signature:
                    ${object.user_id.signature | safe}
                % endif
                </p>
                </div>
             ${(object.company_id.partner_id.ref|safe or object.company_id.partner_id.name|safe)} DTE (Ref ${(object.display_name or ’n/a’)}) Acuse de Recibo - ${object.name} Redactar Email Imprimir PDF Imprimir PDF desde Documentos Online. ATENCION!                         Si Ud. envía un documento no                         aprobado por el SII, puede estar incurriendo                         en una irregularidad administrativa. Factura Respuesta de Aceptación Comercial - ${object.display_name} Respuesta de Recepción de Mercaderías - ${object.display_name} Respuesta de Rechazo Comercial - ${object.name} URL Factura sii.send_queue 