import matplotlib.pyplot as plt

# pms_range, vtl_range, df_range, prf_range = [-10.0, 10.0], [0.7, 1.3], [0.8, 1.2], [0.1, 6]
pms_range, vtl_range, df_range, prf_range = [-10.0, 10.0], [0.6, 1.4], [0.6, 1.4], [0.1, 10]
ranges = [pms_range, vtl_range, df_range, prf_range]


def average(euclid1, euclid2, i):
    avg = (euclid1[i] + euclid2[i]) / 2
    euc_avg = euclid1.copy()
    euc_avg[i] = avg
    return euc_avg


def find_exemplars(point, _range, multiplier):
    step_size = (_range[1] - _range[0]) * 0.5 * multiplier
    # print('Range:', _range, 'Multiplier:', multiplier, 'Step size:', step_size)
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


def plot_background():
    plt.ion()
    fig = plt.figure()
    plt_left = fig.add_subplot(121)
    plt_left.set_xlabel('pitch median shift')
    plt_left.set_ylabel('vocal tract length')
    # plt_left.axis('equal')
    plt_left.plot([pms_range[0], pms_range[0], pms_range[1], pms_range[1], pms_range[0]],
                  [vtl_range[0], vtl_range[1], vtl_range[1], vtl_range[0], vtl_range[0]])
    plt_right = fig.add_subplot(122)
    plt_right.set_xlabel('duration factor')
    plt_right.set_ylabel('pitch range factor')
    # plt_right.axis('equal')
    plt_right.plot([df_range[0], df_range[0], df_range[1], df_range[1], df_range[0]],
                   [prf_range[0], prf_range[1], prf_range[1], prf_range[0], prf_range[0]])
    return plt_left, plt_right


def plot_line(plt_a, plt_b, a_range, point, dim):
    line = [[], []]
    line[0], line[1] = point.copy(), point.copy()
    line[0][dim], line[1][dim] = a_range[0], a_range[1]
    plt_a.plot([x[0] for x in line], [x[1] for x in line])
    plt_b.plot([x[2] for x in line], [x[3] for x in line])


def plot_euclid(plt_a, plt_b, *args):
    for choice in args:
        plt_a.plot(choice.euclid[0], choice.euclid[1], 'o')
        plt_b.plot(choice.euclid[2], choice.euclid[3], 'o')
