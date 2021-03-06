import xml.etree.ElementTree as ET

import numpy

from scripts.tutorial import plot


def load_data(dataset, r=0, d=1, debug_level=0):
    ''' Loads the dataset

    :type dataset: string
    :param dataset: the path to the dataset (SUMO xml output)
    :param r: how many past intervals to include in the input data
    :param d: how far future interval to predict
    '''

    #############
    # LOAD DATA #
    #############
    tree = ET.parse(dataset)
    elem = tree.getroot()
    intervals = elem.findall('.//interval')
    def f(idx_intr, idx_lane):
        try:
            lane = intervals[idx_intr].findall('.//lane')[idx_lane]
            speed = float(lane.get('speed'))
            density = float(lane.get('density'))
            return (speed * density / 3.6)
        except:
            if 1 <= debug_level:
                print('warning: no valid data at interval={}, lane={}'.format(idx_intr,idx_lane))
            #if 0 < idx_intr:
            #    return f(idx_intr-1, idx_lane)
            return 0

    # the size of dataset
    m = len(intervals[0].findall('.//lane'))
    n = len(intervals)

    # create (n-r-d)-by-mr matrix (input dataset)
    x = [[0 for col in xrange(m*(r+1))] for row in xrange(n-r-d)]
    for i in xrange(n-r-d):
        for j in xrange(m):
            for k in xrange(r+1):
                idx_intr = r+i-k
                idx_lane = j
                x[i][j*(r+1)+k] = f(idx_intr, idx_lane)
    dataset_x = numpy.asarray(x, dtype=numpy.float32)

    # create (n-r-d)-by-m matrix (output dataset)
    y = [[0 for col in xrange(m)] for row in xrange(n-r-d)]
    for i in xrange(n-r-d):
        for j in xrange(m):
            idx_intr = d+r+i
            idx_lane = j
            y[i][j] = f(idx_intr, idx_lane)
    dataset_y = numpy.asarray(y, dtype=numpy.float32)

    return (dataset_x, dataset_y)

if __name__ == '__main__':
    try:
        dataset1_x, dataset1_y = load_data('../../data/cross3ltl_full_3/lane.129600.1.xml',r=0,d=1)
        plot.plot(dataset1_y, block=False)
        dataset2_x, dataset2_y = load_data('../../data/cross3ltl_full_3/lane.129600.2.xml',r=0,d=1)
        plot.plot(dataset2_y, block=False)
        dataset3_x, dataset3_y = load_data('../../data/cross3ltl_full_3/lane.129600.3.xml',r=0,d=1)
        plot.plot(dataset3_y)
    except Exception as e:
        print('error')
        print(str(e))