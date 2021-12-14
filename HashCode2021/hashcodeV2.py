from pprint import pprint


def clip(n,l,h):
  return max(l,min(n,h))



class Intersection:

  def __init__(self, id) -> None:
    self.id = id
    self.streets_that_arrive = {}
    self.streets_that_leave = {}
    self.open_for = None

  def street_arrives(self, name, data):
    self.streets_that_arrive[name] = data

  def street_leaves(self, name, data):
    self.streets_that_leave[name] = data

  def best_street(self):
    calles = self.streets_that_arrive.items()
    best = sorted(calles, key=lambda c:-c[1]['time_across'])
    return best[0][0]

  def min_llegada(self):
    return min([t['time_across'] for t in self.streets_that_arrive.values()])

  def filtered_streets(self, strs):
    return [st for st in self.streets_that_arrive.keys() if st not in strs]

  def min_llegadas(self, frecs):
    ff = [frecs[s] for s in self.streets_that_arrive if s in frecs]
    if len(ff): return min(ff)
    return 1

  def suma_llegadas(self, frecs):
    total = 0
    for s in self.streets_that_arrive:
      if s in frecs:
        total += frecs[s]
    return total

  def get_streets(self, frecs: dict):
    names = list(self.streets_that_arrive.keys())
    if len(names) == 1:
      return [(names[0], 1)]
    if not sum([frecs.get(s, 0) for s in names]):
      return [(names[0], 1)]
    total_coches = self.suma_llegadas(frecs)

    calles_final = []
    calles_con_coches = [s for s in names if frecs.get(s, 0) > 0]
    for c in calles_con_coches:
        frec_calle = frecs[c]
        n = clip(frec_calle/total_coches, 1, 10)
        calles_final.append((c,n))
    return calles_final


def get_header_info(header):
  return tuple(map(lambda x:int(x), header.split()))

def get_street_info(line):
  data = line.strip().split()
  return data[2], {
    'int_start': int(data[0]),
    'int_end': int(data[1]),
    'time_across': int(data[3])
  }

def get_car_info(line):
  data = line.strip().split()
  return {
    'streets_to_travel': data[0],
    'streets': data[1:]
  }


def frecuencias_calles(cars):
  calles = []
  for c in cars:
    calles.extend(c['streets'])
  frecuencias = { c:0 for c in calles } 
  for c in calles:
    frecuencias[c] += 1
  return frecuencias

def frecuencias_ordenadas(frecuencias):
  frec_tuples = [(k,v) for k,v in frecuencias.items()]
  sorted_frecs = sorted(frec_tuples, key=lambda x:-x[1])
  return {k:v for k,v in sorted_frecs}




def main():
  file = 'f.txt'
  with open(file, 'r') as f:
    duration, num_intersections,  num_streets, num_cars, bonus = get_header_info(f.readline())
    streets = [ get_street_info(f.readline()) for _ in range(num_streets) ]
    set_calles = {st[0] for st in streets }
    streets = { k:v for k,v in streets }
    cars = [get_car_info(f.readline()) for _ in range(num_cars)]


  intersections = [Intersection(i) for i in range(num_intersections)]
  for name, data in streets.items():
    intersections[data['int_end']].street_arrives(name, data)
    intersections[data['int_start']].street_leaves(name, data)

  frecuencias = frecuencias_calles(cars)
  # print(frecuencias)
  # frecs_dict = frecuencias_ordenadas(frecuencias)  
  # print(frecs_dict)

  with open('output.txt', 'w') as f:
    f.write(f'{len(intersections)}\n')
    for inters in intersections:
      int_sts = inters.get_streets(frecuencias)
      f.write(f'{inters.id}\n')
      f.write(f'{len(int_sts)}\n')
      for s in int_sts:
        name, val = s
        f.write(f'{name} {val}\n')




if __name__ == '__main__':
  main()