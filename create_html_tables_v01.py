# Autuer: Stef Verdonk, gisspecialisten B.V.
# Dit script voegt een tabel to met alle componenten en meetwaarden bij een meetpunt
# Het betreft het formatten van een stuk HTML.

#database connectie
#################################
import psycopg2

hostname = 'localhost'
username = 'postgres'
password = '***'
database = 'terra_index'

myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

# Het is noodzakelijk om de isolation level op nul te zetten
# als je create, insert of drop statements wilt uitvoeren!!!
myConnection.set_isolation_level(0)

cur = myConnection.cursor()

#################################

#from geofoxx_database_login import geofoxx_DB
#con = geofoxx_DB.create_connection()
#cur = con.cursor()

#hulpfuncties voor html
def td_wrap(string):
    return '<td>' + string + '</td>'

def tr_wrap(string):
    return '<tr>' + string + '</tr>'

def th_wrap(string):
    return '<th>' + string + '</th>'


# maak lijst met unieke combinaties prid, mpid
sql = 'with mp as (select prid, mpid from terra_index."tblMeasurementPoints" where componenten is null) select distinct prcode, ar.prid, ar.mpid from terra_index."tblSoilAnalysisResults" as ar, mp where ar.prid = mp.prid and ar.mpid = mp.mpid order by ar.prid desc, ar.mpid desc'
cur.execute(sql)
pr_mp_combinations = cur.fetchall()

#loop over deze lijst
for i, pr_mp in enumerate(pr_mp_combinations):

    #debug statements
    if i % 100 == 0:
        print(i)

    prid = pr_mp[0]
    mpid = pr_mp[2]
    prcode = pr_mp[1]

    # haal een subtabel op met meetwaarden en componentcodes
    sql = 'select componentname, asmeasurevalue from terra_index."tblSoilAnalysisResults" WHERE prid = {} AND mpid = {} AND componentname IS NOT NULL'.format(prid, mpid)
    cur.execute(sql)
    components_vals = cur.fetchall()

    #lets build some html
    html = "'<table>"

    #loop over de subtabel
    for component in components_vals:
        # schrijf de rest van de html
        html += tr_wrap(td_wrap(str(component[0]))+td_wrap(str(component[1])))

    html += "</table>'"
    sql = 'UPDATE terra_index."tblMeasurementPoints" SET componenten = {} WHERE prid = {} AND mpid= {}'.format(html, prid, mpid)
    cur.execute(sql)

con.commit()

myConnection.close()


# query maken van componenten per punt
# deze componenten formatten component: waarde. etc.



"""
prid:               |
mpid:               |
terra_index_link    |   
map_pad_link        |
component 1         |
component 2         |
..
..
..
"""
