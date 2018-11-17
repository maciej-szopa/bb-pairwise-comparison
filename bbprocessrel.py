pms_range, vtl_range, df_range, prf_range = [-10.0, 10.0], [0.6, 1.4], [0.6, 1.4], [0.1, 10]
ranges = [pms_range, vtl_range, df_range, prf_range]


def average(euclid1, euclid2, i):
    avg = (euclid1[i] + euclid2[i]) / 2
    euc_avg = euclid1.copy()
    euc_avg[i] = avg
    return euc_avg


def find_exemplars(point, _range, multiplier):
    step_size = (_range[1] - _range[0]) * 0.5 * multiplier
    point_prim, point_bis = point - step_size, point + step_size
    if point_prim < _range[0]:
        point_prim = _range[0]
    if point_bis > _range[1]:
        point_bis = _range[1]
    return point_prim, point_bis


def set_choices(a, _ranges, dim, step, euclid):
    a1, a2 = find_exemplars(a, _ranges[dim], 0.7 ** step)
    ac, ac1, ac2 = euclid.copy(), euclid.copy(), euclid.copy()
    ac[dim], ac1[dim], ac2[dim] = a, a1, a2
    return ac1, ac, ac2
