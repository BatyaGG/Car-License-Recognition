dicta = {'a':1,'r':1,'s':4,'q':99}
dicta['a']=dicta['a']+1;
dicta.update({'a':dicta['a']+1})
keys = dicta.keys()
values = dicta.values()
print keys
print values
print keys[values.index(max(values))]
print dicta.has_key('3')