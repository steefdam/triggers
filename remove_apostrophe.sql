CREATE OR REPLACE FUNCTION terra_index.remove_apostrophe() RETURNS trigger AS
$BODY$
BEGIN
UPDATE 
   terra_index."tblSoilAnalysisResults"
SET 
   componentname = REPLACE(componentname, '''', '')
WHERE 
   componentname LIKE '%''%';
RETURN NULL;
END;
$BODY$
LANGUAGE plpgsql