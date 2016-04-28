DELETE FROM ir_module_module WHERE name = 'l10n_cl_toponyms';
DELETE FROM ir_model_data 
		WHERE name = 'module_l10n_cl_toponyms' 
		AND module = 'base' 
		AND model = 'ir.module.module';
UPDATE ir_module_module_dependency SET name = 'l10n_cl_counties'
       WHERE name = 'l10n_cl_toponyms';
UPDATE ir_translation SET module = 'l10n_cl_counties'
       WHERE module = 'l10n_cl_toponyms';