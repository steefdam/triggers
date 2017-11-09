CREATE OR REPLACE FUNCTION terra_index.create_html_tables() RETURNS trigger AS $$
global html
global naam

select_pr_mp = plpy.execute('WITH mp AS (SELECT prid, mpid FROM terra_index."tblMeasurementPoints" WHERE componenten IS NULL)
SELECT DISTINCT prcode, ar.prid, ar.mpid FROM terra_index."tblSoilAnalysisResults" AS ar, mp WHERE ar.prid = mp.prid AND ar.mpid = mp.mpid ORDER BY ar.prid DESC, ar.mpid DESC')
plpy.info(select_pr_mp)

for my_row in select_pr_mp:

    pr_id = my_row["prid"]
    pr_code = my_row["prcode"]
    mp_id = my_row["mpid"]

    #haal een subtabel op met meetwaarden en componentcodes
    component_meetwaarden = plpy.execute('SELECT componentname, asmeasurevalue FROM terra_index."tblSoilAnalysisResults" WHERE prid = {} AND mpid = {} AND componentname IS NOT NULL'.format(pr_id, mp_id))
    plpy.info(component_meetwaarden)

    #lets build some html
    html = "'<table>"

    #loop over de subtabel
    for component in component_meetwaarden:
        # schrijf de rest van de html
        html += "<tr><td>" + str(component["componentname"]) + "</td><td>" + str(component["asmeasurevalue"]) + "</td></tr>"

    html += "</table>'"
    update_row = plpy.execute('UPDATE terra_index."tblMeasurementPoints" SET componenten = {} WHERE prid = {} AND mpid= {}'.format(html, pr_id, mp_id))

$$
LANGUAGE plpython3u;

