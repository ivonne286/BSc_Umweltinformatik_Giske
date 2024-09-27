import sqlite3
from contextlib import closing

def create_views(conn: sqlite3.Connection):
    print("Views are being created now.")
    """Create Views in the final DB."""
    with closing(conn.cursor()) as cursor:
        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Auswertung_original;
            """
        )
        
        _ = cursor.execute(
            """
            CREATE VIEW View_Auswertung_original
            AS
            SELECT
				sample_evaluation.id AS Evaluation_ID,
				specimen.voucher_id AS Voucher_ID,
				mission.id AS Mission_ID,
				error_type.code AS Fehlercode,
				category.id AS Kategorie_ID,
				sample_evaluation.notes AS Notizen
            FROM sample_evaluation
			INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
			INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
			INNER JOIN category ON category.id = sample_evaluation.category_id
			INNER JOIN mission ON mission.id = specimen.mission_id
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Auswertung_original_lesbar;
            """
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Auswertung_original_lesbar
            AS
            SELECT
				sample_evaluation.id AS Evaluation_ID,
				specimen.voucher_id AS Voucher_ID,
				mission.name AS Mission_Name,
				error_type.name AS Fehlertyp,
				category.name AS Kategorie,
				sample_evaluation.notes AS Notizen
            FROM sample_evaluation
			INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
			INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
			INNER JOIN category ON category.id = sample_evaluation.category_id
			INNER JOIN mission ON mission.id = specimen.mission_id
			;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_alle_echten_Fehler;
            """
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_alle_echten_Fehler
            AS
            SELECT
                sample_evaluation.id,
                specimen.voucher_id AS Voucher_ID,
                mission.name AS Mission_Name,
                error_type.name AS Fehlertyp,
				error_type.code,
                category.name AS Kategorie,
                sample_evaluation.discussion_available AS "Diskussion? 0=nein, 1=ja",
                sample_evaluation.notes AS Notizen
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            WHERE error_type.code IS NOT 1 AND error_type.code NOT LIKE "8%"
            ORDER BY sample_evaluation.id
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehleranzahl_pro_Mission
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Fehleranzahl_pro_Mission
            AS
            SELECT
	            mission.name AS Name_Mission,
	            COUNT(*) AS Fehleranzahl,
                COUNT(DISTINCT sample_evaluation.specimen_id) AS fehlerhafte_Belege
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            WHERE error_type.name IS NOT "Kein Fehler"
            GROUP BY mission.name
            ORDER BY Fehleranzahl DESC
            ;"""
        )

        _ = cursor.execute(
            """
        DROP VIEW IF EXISTS View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme;
        """
        )

        _ = cursor.execute("""

        CREATE VIEW View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme
        AS
        SELECT
	        mission.name AS Name_Mission,
	        COUNT(*) AS "Fehleranzahl_oV",
            COUNT(DISTINCT sample_evaluation.specimen_id) AS fehlerhafte_Belege
        FROM sample_evaluation
        INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
        INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
        INNER JOIN category ON category.id = sample_evaluation.category_id
        INNER JOIN mission ON mission.id = specimen.mission_id
        WHERE error_type.name IS NOT "Kein Fehler" and error_type.name NOT LIKE "Val%"
        GROUP BY mission.id
        """)

        _ = cursor.execute(
            """
        DROP VIEW IF EXISTS View_Fehlerquote_pro_Mission;    
        """
        )

        _ = cursor.execute(
            """
        CREATE VIEW View_Fehlerquote_pro_Mission AS
        SELECT
            mission.name AS Name_der_Mission,
		    mission.year AS Jahr_Mission,
		    mission.amount_of_categories AS Anzahl_Kategorien,
            COUNT(DISTINCT sample_evaluation.specimen_id) AS "überprüfte Belege",
		    COUNT(DISTINCT sample_evaluation.specimen_id)*mission.amount_of_categories AS "überprüfte Einträge",
            View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme.Fehleranzahl_oV AS "fehlerhafte Einträge (ohne Validierungsprobleme)",
		    round(View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme.Fehleranzahl_oV*100.00/(COUNT(DISTINCT sample_evaluation.specimen_id)*mission.amount_of_categories),1) AS "Fehlerquote in Prozent"
        FROM sample_evaluation
        INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
        INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
        INNER JOIN category ON category.id = sample_evaluation.category_id
        INNER JOIN mission ON mission.id = specimen.mission_id
	    INNER JOIN View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme ON View_Fehleranzahl_pro_Mission_ohne_Validierungsprobleme.Name_Mission = Name_der_Mission
        GROUP BY Name_der_Mission
        ORDER BY mission.id
        """
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehleranzahl_pro_Mission_detailliert;
            """
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Fehleranzahl_pro_Mission_detailliert
            AS
            SELECT
                mission.name AS Name_der_Mission,
				mission.year AS Jahr_Mission,
                mission.amount_finished_by_herbonauts AS Größe_Mission,
                COUNT(DISTINCT sample_evaluation.specimen_id) AS "davon überprüft",
                View_Fehleranzahl_pro_Mission.fehlerhafte_Belege AS "davon Belege mit Fehler",
                View_Fehleranzahl_pro_Mission.Fehleranzahl AS "Fehleranzahl gesamt"
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            INNER JOIN View_Fehleranzahl_pro_Mission ON View_Fehleranzahl_pro_Mission.Name_Mission = Name_der_Mission
            GROUP BY Name_Mission
            ORDER BY Jahr_Mission
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_alle_Fehlerkombinationen_Liste;
            """
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_alle_Fehlerkombinationen_Liste
            AS
            SELECT
		        error_type.name AS Fehlertyp,
		        category.name AS Kategorie,
		        COUNT(error_type.name) AS Anzahl,
		        ROUND((COUNT(error_type.name) * 100.00 / 238),2) AS prozentualer_Anteil_an_allen_238_Fehlern
            FROM sample_evaluation
			INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
			INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
			WHERE error_type.code IS NOT 1
			GROUP BY Fehlertyp, Kategorie
			ORDER BY Anzahl DESC
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehler_pro_Kategorie_ohne_Valid_prob
            ;""")
        
        _ = cursor.execute(
            """
            CREATE VIEW View_Fehler_pro_Kategorie_ohne_Valid_prob
            AS
            SELECT
	            category.name AS Kategorie,
                COUNT(*) AS Fehleranzahl_ohne_Validierungsprobleme
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
	        INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
	        WHERE error_type.id != 1 and error_type.name NOT LIKE "Val%"
            GROUP BY Kategorie
            ORDER BY Fehleranzahl_ohne_Validierungsprobleme DESC
            ;""")
        
        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehler_pro_Kategorie_nur_Validierungsprobleme
            ;""")
        
        _ = cursor.execute(
            """
            CREATE VIEW View_Fehler_pro_Kategorie_nur_Validierungsprobleme
            AS
            SELECT
                category.name AS Kategorie,
                COUNT(*) AS Validierungsprobleme
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
            WHERE error_type.id != 1 AND error_type.name LIKE "Val%"
            GROUP BY Kategorie
            ORDER BY Validierungsprobleme DESC
            ;""")
        
        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Häufigkeit_der_Fehlertypen
            ;""")
        
        _ = cursor.execute(
            """
            CREATE VIEW View_Häufigkeit_der_Fehlertypen
            AS
            SELECT
	            error_type.name AS Fehlertyp,
	            COUNT(*) AS Anzahl,
		    cause_group.name AS "Fehlerursache kurz",
		    ROUND((COUNT(*)*100.00/238),2) AS "%-Anteil an allen 238 Fehlern"
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
	        INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
	        WHERE error_type.id != 1
            GROUP BY Fehlertyp
            ORDER BY Anzahl DESC
            ;""")
        
        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehlerursachen_summiert
            ;"""
        )
        
        _ = cursor.execute(
            """
            CREATE VIEW View_Fehlerursachen_summiert
            AS
            SELECT
            cause_group.name AS Fehlerursache,
            cause_group.description AS Beschreibung,
            COUNT(*) AS Anzahl_in_Stichprobe
            FROM sample_evaluation
			INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
			INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
			INNER JOIN category ON category.id = sample_evaluation.category_id
			INNER JOIN mission ON mission.id = specimen.mission_id
			INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
            WHERE cause_group.id != 0
            GROUP BY cause_group.name
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehleranzahl_je_fehlerhaftem_Datensatz
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Fehleranzahl_je_fehlerhaftem_Datensatz
            AS
            SELECT
                specimen.voucher_id AS Datensatz_Voucher_ID,
                count(specimen.voucher_id) as Fehler_pro_Datensatz,
				mission.name AS Mission_Name
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            WHERE error_type.id IS NOT 1
	        group by Datensatz_Voucher_ID
	        order by Fehler_pro_Datensatz desc
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Fehleranzahl_je_fehlerhaftem_Datensatz_summiert
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Fehleranzahl_je_fehlerhaftem_Datensatz_summiert
            AS
            SELECT
                COUNT(Fehler_pro_Datensatz) AS Anzahl_Datensätze_mit_Fehlern,
                Fehler_pro_Datensatz AS Anzahl_Fehler_pro_Datensatz,
                COUNT(Fehler_pro_Datensatz) * Fehler_pro_Datensatz AS Fehler_gesamt
            FROM View_Fehleranzahl_je_fehlerhaftem_Datensatz
            GROUP BY Fehler_pro_Datensatz
            ORDER BY Anzahl_Datensätze_mit_Fehlern asc
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Basis_Kreuztabelle
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Basis_Kreuztabelle
            AS
            SELECT
                error_type.id,
                error_type.name AS Fehlertyp,
                category.name AS Kategorie
            FROM sample_evaluation
			INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
			INNER JOIN category ON category.id = sample_evaluation.category_id
			WHERE error_type.code IS NOT 1
			ORDER BY error_type.cause_group_id, error_type.id
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Alle_Herbonauten_bedingten_Fehler
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Alle_Herbonauten_bedingten_Fehler
            AS
            SELECT
                error_type.name AS Fehlertyp,
                category.name AS Kategorie,
                COUNT(error_type.name) AS Anzahl,
                ROUND((COUNT(error_type.name) * 100.00 / 238),1) AS prozentualer_Anteil_an_allen_238_Fehlern
            FROM sample_evaluation
			INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
			INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
			WHERE error_type.code IS NOT 1 and cause_group.id = 1
			GROUP BY Fehlertyp, Kategorie
			ORDER BY Anzahl DESC
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Alle_Systembedingten_Fehler
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Alle_Systembedingten_Fehler
            AS
            SELECT
                error_type.name AS Fehlertyp,
                category.name AS Kategorie,
                COUNT(error_type.name) AS Anzahl,
                ROUND((COUNT(error_type.name) * 100.00 / 238),1) AS prozentualer_Anteil_an_allen_238_Fehlern
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            INNER JOIN cause_group ON cause_group.id = error_type.cause_group_id
            WHERE error_type.code IS NOT 1 and cause_group.id = 2
            GROUP BY Fehlertyp, Kategorie
            ORDER BY Anzahl DESC
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Länder_veränderte_Regionen
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Länder_veränderte_Regionen AS
            with country_count as (
                SELECT
                    json_extract(s.validated_data, '$.country - country') AS country,
                    COUNT(*) AS TOTAL
                FROM specimen s where s.in_sample = 1 group by country
                )
            SELECT
                json_extract(specimen.validated_data, '$.country - country') AS Land,
				country_count.TOTAL AS Gesamt_Belege_pro_Land,
                COUNT(json_extract(specimen.validated_data, '$.country - country')) AS Belege_mit_veränderter_Region
            FROM specimen
                INNER JOIN sample_evaluation ON sample_evaluation.specimen_id = specimen.id
                JOIN country_count ON country_count.country = json_extract(specimen.validated_data, '$.country - country')
            WHERE specimen.in_sample = 1 AND error_type_id = 9 AND category_id = 2
            GROUP BY Land
            ORDER BY Gesamt_Belege_pro_Land DESC
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_alle_Validierungsprobleme
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_alle_Validierungsprobleme
            AS
            SELECT
                sample_evaluation.id,
                specimen.voucher_id AS Voucher_ID,
                mission.name AS Mission_Name,
                error_type.name AS Fehlertyp,
				error_type.code,
                category.name AS Kategorie,
                sample_evaluation.discussion_available AS "Diskussion? 0=nein, 1=ja",
                sample_evaluation.notes AS Notizen
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            INNER JOIN category ON category.id = sample_evaluation.category_id
            INNER JOIN mission ON mission.id = specimen.mission_id
            WHERE error_type.code LIKE "8%"
            ORDER BY sample_evaluation.id
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Diskussion_Nutzung_Datensätze_mit_Fehler
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Diskussion_Nutzung_Datensätze_mit_Fehler
            AS
            SELECT
                count(DISTINCT voucher_id) as Anzahl_Datensätze_mit_Fehler_und_Diskussion,
                discussion_available,
                round((count(DISTINCT voucher_id)*100.00/167), 2) AS prozentual
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            WHERE sample_evaluation.discussion_available is 1
            AND sample_evaluation.error_type_id != 1
            ;"""
        )

        _ = cursor.execute(
            """
            DROP VIEW IF EXISTS View_Diskussion_Nutzung_Datensätze_ohne_Fehler
            ;"""
        )

        _ = cursor.execute(
            """
            CREATE VIEW View_Diskussion_Nutzung_Datensätze_ohne_Fehler
            AS
            SELECT
                count(DISTINCT voucher_id) as Anzahl_Datensätze_ohne_Fehler_und_mit_Diskussion,
                discussion_available,
                round((count(DISTINCT voucher_id)*100.00/333), 2) AS prozentual
            FROM sample_evaluation
            INNER JOIN specimen ON specimen.id = sample_evaluation.specimen_id
            INNER JOIN error_type ON error_type.id = sample_evaluation.error_type_id
            WHERE sample_evaluation.discussion_available is 1
            AND sample_evaluation.error_type_id = 1
            ;"""
        )

    print("The views have been created.")