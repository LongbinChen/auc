import math

pos = []
neg = []
x = []

tpr_list = []
fpr_list = []

#auc = 0.6, alpha = 0.07
#auc = 0.7, alpha = 0.28
#auc = 0.8, alpha = 0.72
alpha = 0.72
total_area = 0.0
mis_area = 0.0
pos_area = 0.0
neg_area = 0.0

neg_weight = 4.0

for i in range(-8000, 8000):
  t = float(i) / 1000.0
  x.append(t) 
  pos_val = math.exp(-alpha * t*t)
  pos.append(pos_val)
  neg_val = math.exp(-alpha * (t - 1.0)*(t-1.0))
  neg.append(neg_val)
  pos_area += pos_val 
  neg_area += neg_val
   
  TPR = pos_area  
  FPR = neg_area 
  tpr_list.append(TPR) 
  fpr_list.append(FPR) 

for i in range(len(tpr_list)):
   tpr_list[i] = tpr_list[i] / pos_area
   fpr_list[i] = fpr_list[i] / pos_area
   #print tpr_list[i], fpr_list[i]
   precision = tpr_list[i] / (tpr_list[i] + neg_weight * fpr_list[i])  
   if i % 100 == 0:
     print x[i], tpr_list[i], fpr_list[i],  precision, tpr_list[i], (tpr_list[i] + neg_weight * fpr_list[i])

#calculate AUC 
area = 0 

pre_x = 0.0
pre_y = 0.0
for x, y in zip(fpr_list, tpr_list):
  delta_x = x - pre_x   
  area += delta_x * (pre_y + y) * 0.5
  pre_x = x
  pre_y = y

print "AUC", area


