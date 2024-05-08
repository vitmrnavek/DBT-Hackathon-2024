import sys
import ruamel.yaml

yaml = ruamel.yaml.YAML(typ='safe')
with open('foobar.yaml') as fp:
  data = yaml.load(fp)

end_value = 0
for one_value in  data['A']['A3']['A3A']['A3A1'].values():
   end_value += one_value

print(end_value)

yaml.dump(data, sys.stdout)
