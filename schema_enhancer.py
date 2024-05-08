import yaml
import json


def find_element_by_name(value, ls):
    return [(i,idx) for idx,i in enumerate(ls) if i['name'] == value][0]

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True
def find_element(element, json):
    keys = element.split('.')
    source=find_element_by_name(keys[0], json["sources"])
    table=find_element_by_name(keys[1], source[0]["tables"])
    column=find_element_by_name(keys[2], table[0]["columns"])
    return (source[1], table[1], column[1])


class Schema:
    def __init__(self, schema):
        """fetch schema configuration from yaml file address"""
        with open(schema, 'r') as f:
            self.schema = yaml.load(f, Loader=yaml.FullLoader)
        self.mapping = self.schema.get('mapping')
        self.schema_template = self.schema.get('schema_template')
    def apply_schema_template_to_source_yaml(self, file):
        """apply schema template to the file"""
        with open(file, 'r') as f:
            source_schema = yaml.load(f, Loader=yaml.FullLoader)
        schema = self.schema_template
        for table in self.mapping:
            table_template=schema[table]
            mapped_columns=self.mapping[table]
            for column in mapped_columns:
                column_templates=table_template["columns"]
                column_template=find_element_by_name(column, column_templates)
                for column_location in mapped_columns[column]:
                    column_idx_location=find_element(column_location, source_schema)
                    col_name=column_location.split('.')[-1]
                    column_template[0]["name"]=col_name
                    source_schema["sources"][column_idx_location[0]]["tables"][column_idx_location[1]]["columns"][column_idx_location[2]]=column_template[0]
        with open(file, 'w') as f:
            yaml.dump(source_schema, f,Dumper=NoAliasDumper)



if __name__ == "__main__":
    schema=Schema('main_schema.yml')
    schema.apply_schema_template_to_source_yaml('models/sources/data_sample.yml')



