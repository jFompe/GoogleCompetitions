from pprint import pprint


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


def main():
  file = 'f.txt'
  total_calles = set()
  with open(file, 'r') as f:
    duration, num_intersections,  num_streets, num_cars, bonus = get_header_info(f.readline())
    streets = [ get_street_info(f.readline()) for _ in range(num_streets) ]
    total_calles.update([st[0] for st in streets])
    streets = { k:v for k,v in streets }
    cars = [get_car_info(f.readline()) for _ in range(num_cars)]

  intersections = [Intersection(i) for i in range(num_intersections)]
  for name, data in streets.items():
    intersections[data['int_end']].street_arrives(name, data)
    intersections[data['int_start']].street_leaves(name, data)

  calles_pasadas = set()

  calles = []
  for c in cars:
    calles.extend(c['streets'])

  frecuencias = {c:0 for c in calles}
  for car in cars:
    for c in car['streets']:
      frecuencias[c] += 1
  frec_tuple = []
  for k,v in frecuencias.items():
    frec_tuple.append((k,v))
  sorted_frecs = sorted(frec_tuple, key=lambda x:-x[1])
  # print(sorted_frecs)
  frecs_dict = {k:v for k,v in sorted_frecs}
  # print(frecs_dict)

  for c in cars:
    calles_pasadas.update(c['streets'])

  dif = total_calles - calles_pasadas

  contador = 0
  with open('output.txt', 'w') as f:
    f.write(f'{len(intersections)}\n')
    # f.write(f'{n}\n') 
    for inters in intersections:
      ml = inters.min_llegadas(frecs_dict)
      llegan = inters.filtered_streets(dif)
      if len(llegan):
        contador += 1
        f.write(f'{inters.id}\n')
        f.write(f'{len(llegan)}\n')
        for k in llegan:
          f.write(f'{k} {max(1,int(frecs_dict[k]/ml))}\n')


  print(contador)




  # pprint(streets)
  # pprint(cars)





if __name__ == '__main__':
  main()