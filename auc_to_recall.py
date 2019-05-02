import argparse
import math



def calculate_auc_with_alpha(alpha):
    """
    return auc for a given alpha
    :param alpha:
    :return: auc
    """
    pos = []
    neg = []
    x = []

    tpr_list = []
    fpr_list = []

    pos_area = 0.0
    neg_area = 0.0

    for i in range(-8000, 8000):
         t = float(i) / 1000.0
         x.append(t)
         pos_val = math.exp(-alpha * (t + 1.0) * (t + 1.0))
         pos.append(pos_val)
         neg_val = math.exp(-alpha * (t - 1.0) * (t - 1.0))
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


    #calculate AUC
    area = 0
    pre_x = 0.0
    pre_y = 0.0
    for x, y in zip(fpr_list, tpr_list):
        delta_x = x - pre_x
        area += delta_x * (pre_y + y) * 0.5
        pre_x = x
        pre_y = y

    return area, fpr_list, tpr_list


def calculate_alpha(expected_auc = 0.7):
    """
    larger alpha will have smaller AUC
    :param expected_auc:
    :return:
    """

    min_alpha = 0
    max_alpha = 1000

    while max_alpha - min_alpha > 0.0001:
        mid_alpha = (min_alpha + max_alpha) / 2.0
        mid_auc, _, _ = calculate_auc_with_alpha(mid_alpha)
        if expected_auc > mid_auc:
            min_alpha = mid_alpha
        elif expected_auc < mid_auc:
            max_alpha = mid_alpha
        else:
            return mid_alpha
    print mid_alpha, mid_auc, max_alpha, min_alpha

    return mid_alpha

def run(params):

    """
    :param params:
    :return:
    """

    alpha = calculate_alpha(float(params.auc))
    auc, fpr_list, tpr_list = calculate_auc_with_alpha(alpha)

    print "find alpha = %.3f to achieve auc %.3f\n" % (alpha, auc)

    ratio = float(params.ratio)

    print "TP\tFP\tprec\trecall"
    for i in range(len(tpr_list)):
        precision = tpr_list[i] / (tpr_list[i] + ratio * fpr_list[i] + 0.0000001)
        if i % 10 == 0:
            print "%.3f\t%.3f\t%.3f\t%.3f" % ( tpr_list[i], fpr_list[i],  precision, tpr_list[i])\

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--auc', default=0.7, help='the auc value, default 0.7')
    parser.add_argument('--ratio', default=2.0, help='the ratio of negative sample to positive sample, default 2.0')

    params = parser.parse_args()
    run(params)



