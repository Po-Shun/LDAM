from structure import MixedDiagnosisStructure, check_device
import argparse
import pandas as pd
import os

def main():
  """
  sample : python3 main.py -a 1 -b 2 -c 3 -p 20 -i 30
  # substructure A: 1
  # substructure B: 2
  # substructure C: 3
  broken probability: 20 %
  """
  parser = argparse.ArgumentParser()
  parser.add_argument('-a', type = int, help="# of substructure A")
  parser.add_argument('-b', type = int, help="# of substructure B")
  parser.add_argument('-c', type = int, help="# of substructure C")
  parser.add_argument('-p', type = float, help="broken probability")
  parser.add_argument('-i', type = int, help="iteration times")
  args = parser.parse_args()
  total_iteration = args.i
  sturcture_a = list() 
  sturcture_b = list() 
  sturcture_c = list()
  results = list()
   
  for iter in range(total_iteration):
    graph = MixedDiagnosisStructure(iter, args.p)
    graph.add_subgraph_A(args.a)
    graph.add_subgraph_B(args.b)
    graph.add_subgraph_C(args.c)
    sturcture_a.append(graph.df_A)
    sturcture_b.append(graph.df_B)
    sturcture_c.append(graph.df_C)
    results.append(graph.result)
  
  df_a = pd.concat(sturcture_a)
  df_b = pd.concat(sturcture_b)
  df_c = pd.concat(sturcture_c)
  dir_name = 'a{}_b{}_c{}_p{}_i{}'.format(args.a, args.b, args.c, args.p, args.i)
  print(dir_name)
  os.mkdir(dir_name)
  filename_a = os.path.join(dir_name, "a.csv")
  filename_b = os.path.join(dir_name, "b.csv")
  filename_c = os.path.join(dir_name, "c.csv")
  df_a.to_csv(filename_a)
  df_b.to_csv(filename_b)
  df_c.to_csv(filename_c)

  dict = {'result': results, 'iter':range(total_iteration)}
  df_result = pd.DataFrame(dict)
  filename_result = os.path.join(dir_name, "result.csv")
  df_result.to_csv(filename_result)

if __name__ == '__main__':
  main()