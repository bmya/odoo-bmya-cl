
.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

==========================================
Multicompany Fix for Accounts and Journals
==========================================




Configuration
=============

Simply install

Usage
=====

En many2one fields, you will see the company between brackets. This helps not getting confused of the accounts you are using in each journal, or the journal you are using for account registration, or the tax you are selecting.

Known issues / Roadmap
======================
In the development, tried to define name_get inside an AbstractModel, but it didn't work.
So, the workaround was to define it in a normal Model class for each model.

Author
======
Author: Blanco Martín & Asociados.

Credits and Contributors
========================

* Daniel Blanco <daniel@blancomartin.cl>

Maintainer
==========

Blanco Martín & Asociados - Odoo Silver Partner.

.. image:: https://blancomartin.cl/logo.png
   :alt: Blanco Martin y Asociados' logo
   :target: https://blancomartin.cl


This module is maintained by Blanco Martín & Asociados.

To contribute to this module, please visit https://blancomartin.cl.
