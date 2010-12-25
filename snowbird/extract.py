def extract_for_model(model, fields=[]):
    """
    Writes the contents of the database table for a
    Django model to a .csv file
    """

    #TODO mysql writes output files with mysql user acl
    
    #TODO get correct cursor for model
    db = 'default'
    cur = connections[db].cursor()
    
    table = model._meta.db_table
    if not fields:

        colmap = self.get_field_col_map(model, 
                                    getattr(modelsource, 'fields', []))
    field_names = [f.attname for f in model._meta.fields]
    filename = os.path.join(E_DIR, 'e_%s_%s.csv' % (db, table, ))

    MYSQL_OUTFILE_TEMPLATE = \
    """
    SELECT %s INTO OUTFILE '%s' 
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"'
    LINES TERMINATED BY '\n'
    FROM %s
    """ % (','.join(field_names),
        filename,
        table, )
            
    try:
        cur.execute(MYSQL_OUTFILE_TEMPLATE)
    except OperationalError:
        raise
    finally:
        cur.close()
    return (filename, table, field_names, )
