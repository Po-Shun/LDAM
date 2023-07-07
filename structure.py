import random
import math
import pandas as pd

DATFRAME_COLUMN_A = ['U', 'P', 'Q', 'ITER']
DATFRAME_COLUMN_B = ["U", "W", "X", "Y", "Z", 'ITER']
DATFRAME_COLUMN_C = ["U", "V", 'ITER']


"""
substructure A
    *(U)
    |
    *(P)
    |
    *(Q)
"""
class subgraph_A:
  def __init__(self, status):
    self.P = None
    self.Q = None
    self.set_status(status)
  
  def set_status(self, status):
    self.P = status[0]
    self.Q = status[1]

"""
substructure B
    *(U)
    /\
   /  \
  *(W) *(X)
   \  /
    \/
    |
    *(Y)
    |
    *(Z)
"""
class subgraph_B:
  def __init__(self, status):
    self.W = None
    self.X = None 
    self.Y = None 
    self.Z = None
    self.set_status(status)
  
  def set_status(self,status):
    self.W = status[0]
    self.X = status[1] 
    self.Y = status[2] 
    self.Z = status[3]

"""
substructure C
    *(U)
    |
    *(V)
"""
class subgraph_C:
  def __init__(self, status):
    self.V = None 
    self.set_status(status);

  def set_status(self, status):
    self.V = status[0]

"""
This class is used to decide whether the devices are broken by providing the probability
"""
class well_decider:
  def __init__(self, broken_prob):
    self.values = [False, True]
    self.weights = [100 - broken_prob, broken_prob]  
  """
  return type -> list
  this method will return a bool list which represents the status of corresponding devices
  """
  def decide_broken(self, nums):
    return random.choices(self.values, self.weights, k = nums)


"""
the omega function
---------------------
False: not broken
True:  broken
---------------------
truth table:
p -> u      | omega(p,u)
---------------------
0    0      |  0
0    0      |  1
1    0      |  X(randon return 0/1)
"""
def check_device(p,u):
  if(p == False):
    return u
  else:
    values = [False, True]
    weight = [50, 50]
    return random.choices(values, weight, k = 1)[0]

class MixedDiagnosisStructure(well_decider):
  def __init__(self, iter, broken_prob):
    well_decider.__init__(self, broken_prob)
    self.iter = iter
    #  status of root node 
    self.U = self.decide_broken(1)[0]
    self.cluster_A = list()
    self.cluster_B = list()
    self.cluster_C = list()
    self.df_A = pd.DataFrame(columns=DATFRAME_COLUMN_A)
    self.df_B = pd.DataFrame(columns=DATFRAME_COLUMN_B)
    self.df_C = pd.DataFrame(columns=DATFRAME_COLUMN_C)
    self.a = 0
    self.b = 0
    self.c = 0
    self.result = 0
  
  def add_subgraph_A(self, nums):
    self.a = nums
    for idx in range(nums):
      sub = subgraph_A(self.decide_broken(2))
      self.df_A.loc[len(self.df_A.index)] = [self.U, sub.P, sub.Q, self.iter]
      self.cluster_A.append(sub)

  def add_subgraph_B(self, nums):
    self.b = nums
    for idx in range(nums):
      sub = subgraph_B(self.decide_broken(4))
      self.df_B.loc[len(self.df_B.index)] = [self.U, sub.W, sub.X, sub.Y, sub.Z, self.iter]
      self.cluster_B.append(sub)

  def add_subgraph_C(self, nums):
    self.c = nums
    for idx in range(nums):
      sub = subgraph_C(self.decide_broken(1))
      self.df_C.loc[len(self.df_C.index)] = [self.U, sub.V, self.iter]
      self.cluster_C.append(sub)

  def printf_data(self):
    print(self.df_A)
    print(self.df_B)
    print(self.df_C)

  # Local diagnosis algorithm for mixed structure 
  def LDAM(self):
    a = self.a
    b = self.b
    c = self.c
    B0 = [[0,0,0,0,0], [0,0,0,1,0], [0,0,1,0,0]]
    B1 = [[1,1,0,1,0], [1,1,1,0,0], [1,1,0,0,0]]
    B2 = [[0,0,0,0,1], [0,0,0,1,1], [0,0,1,0,1], [0,0,1,1,1], [0,1,0,1,0], [1,0,1,0,0]]
    B3 = [[1,1,0,0,1], [1,1,0,1,1], [1,1,1,0,1], [1,1,1,1,1], [0,1,1,0,0], [1,0,0,1,0]]
    a_0 = a_1 = b_0 = b_1 = b_2 = b_3= c_0 = c_1 = 0
    if(a > 0):
      for cluster in self.cluster_A:
        check_result = [check_device(cluster.P, self.U), check_device(cluster.Q, cluster.P)]
        if check_result == [0, 0]:
          a_0 += 1
        elif check_result == [1, 0]:
          a_1 += 1
    
    if(b > 0):
      for cluster in self.cluster_B:
        check_result = [check_device(cluster.W, self.U), check_device(cluster.X, self.U), check_device(cluster.Y, cluster.W), check_device(cluster.Y, cluster.X), check_device(cluster.Z, cluster.Y)]
        if check_result in B0:
          b_0 += 1
        if check_result in B1:
          b_1 += 1
        if check_result in B2:
          b_2 += 1
        if check_result in B3:
          b_3 += 1
    
    if( c > 0):
      for cluster in self.cluster_C:
        check_result = check_device(cluster.V, self.U)
        if check_result == 0:
          c_0 += 1
        elif check_result == 1:
          c_1 += 1

    if a_0 + (2 * b_0) + b_2 + (math.floor((c_0 + c_1) / 2)) >= a_1 + (2 * b_1) + b_3 + c_1:
      self.result = 0
    else:
      self.result = 1





