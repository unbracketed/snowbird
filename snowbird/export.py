
class ExportDjango:
    """
    A ModelMap provides support for declaring data transformation maps between
    sources and destinations of data. 
    """

    def __init__(self, iosrc):
        self.extract_dir = E_DIR


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

    def get_reader(filename):
        "Returns an iterator for a Django model extract"
        return csv.reader(open(filename, 'r'))

    def get_as_dict(modelsource):
        "Converts a Django Model source to a dict"
        _d = {}
        filename, table, fields = modelsource 
        for row in get_reader(filename):
            if len(row) == len(fields):
                _d.update(row)
            else:
                #TODO
                pass

