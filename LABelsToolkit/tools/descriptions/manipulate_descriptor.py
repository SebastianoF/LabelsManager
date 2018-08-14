import collections
import copy
import numpy as np

from LABelsToolkit.tools.aux_methods.sanity_checks import is_valid_permutation
from LABelsToolkit.tools.descriptions.label_descriptor_manager import descriptor_standard_header


def permute_labels_from_descriptor(in_ldm, permutation):
    """
    Given a permutation, as specified in
    Save on the same place: yes it is destructive, but results can be undone with the inverse permutation
    :param in_ldm: instance of a class labels descriptor manager.
    :param permutation: a permutation defined by a list of integers (checked by is_valid_permutation under
    sanity_check).
    :return:
    """
    assert is_valid_permutation(permutation)
    out_ldm = copy.copy(in_ldm)
    d = out_ldm.dict_label_descriptor
    for k1, k2 in zip(permutation[0],permutation[1]):
        d[k1], d[k2] = d[k2], d[k1]
    return out_ldm


def generate_dummy_label_descriptor(pfi_output=None, list_labels=range(5), list_roi_names=None,
                                    list_colors_triplets=None):
    """
    For testing purposes, it creates a dummy label descriptor with the itk-snap convention
    :param pfi_output: where to save the eventual label descriptor
    :param list_labels: list of labels range, default 0:5
    :param list_roi_names: names of the regions of interests. If None, default names are assigned.
    :param list_colors_triplets: list of lists of rgb same lenght of list_roi_names if any.
    :return: label descriptor as a dictionary.
    """
    d = collections.OrderedDict()
    num_labels = len(list_labels)
    visibility = [(1.0, 1, 1)] * num_labels
    if list_roi_names is None:
        list_roi_names = ["label {}".format(j) for j in list_labels]
    else:
        assert len(list_labels) == len(list_roi_names)
    if list_colors_triplets is None:
        list_colors_triplets = [list(np.random.choice(range(256), 3)) for _ in range(num_labels)]
    else:
        assert len(list_labels) == len(list(list_colors_triplets))

    for j in range(num_labels):
        up_d = {str(j): [list_colors_triplets[j], visibility[j], list_roi_names[j]]}
        d.update(up_d)
    f = open(pfi_output, 'w+')
    f.write(descriptor_standard_header)
    for j in d.keys():
        if j.isdigit():
            line = '{0: >5}{1: >6}{2: >6}{3: >6}{4: >9}{5: >6}{6: >6}    "{7}"\n'.format(
                j, d[j][0][0], d[j][0][1], d[j][0][2], d[j][1][0], d[j][1][1], d[j][1][2], d[j][2])
            f.write(line)
    f.close()
    return d
