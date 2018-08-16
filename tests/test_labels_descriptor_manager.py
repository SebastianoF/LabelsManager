import collections
import os
from os.path import join as jph

from nose.tools import assert_raises

from LABelsToolkit.tools.aux_methods.label_descriptor_manager import LabelsDescriptorManager, \
    generate_dummy_label_descriptor
from LABelsToolkit.tools.phantoms_generator import local_data_generator as ldg


def _create_data_set_for_tests():
    if not os.path.exists(jph(ldg.pfo_target_atlas, 'label_descriptor.txt')):
        print('Generating testing dataset. May take a while, but it is done only once!')
        ldg.generate_atlas_at_specified_folder()


def check_list_equal(l1, l2):
    return len(l1) == len(l2) and sorted(l1) == sorted(l2)


def test_basics_methods_labels_descriptor_manager_wrong_input_path():
    _create_data_set_for_tests()

    pfi_unexisting_label_descriptor_manager = 'zzz_path_to_spam'
    with assert_raises(IOError):
        LabelsDescriptorManager(pfi_unexisting_label_descriptor_manager)


def test_basics_methods_labels_descriptor_manager_wrong_input_convention():
    _create_data_set_for_tests()

    not_allowed_convention_name = 'just_spam'
    with assert_raises(IOError):
        LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'), not_allowed_convention_name)


def test_basic_dict_input():
    _create_data_set_for_tests()

    dict_ld = collections.OrderedDict()
    dict_ld.update({0: [[0, 0, 0],   [1.0, 1.0, 1.0], 'Bkg']})
    dict_ld.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_ld.update({2: [[0, 255, 0], [1.0, 1.0, 1.0], 'WM']})
    dict_ld.update({3: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})
    dict_ld.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))

    check_list_equal(ldm.dict_label_descriptor.keys(), dict_ld.keys())
    for k in ldm.dict_label_descriptor.keys():
        check_list_equal(ldm.dict_label_descriptor[k], dict_ld[k])


def test_save_in_itk_snap_convention():
    _create_data_set_for_tests()

    ldm = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    ldm.save_label_descriptor(jph(ldg.pfo_target_atlas, 'label_descriptor2.txt'))

    f1 = open(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'), 'r')
    f2 = open(jph(ldg.pfo_target_atlas, 'label_descriptor2.txt'), 'r')

    for l1, l2 in zip(f1.readlines(), f2.readlines()):
        assert l1 == l2

    os.system('rm {}'.format(jph(ldg.pfo_target_atlas, 'label_descriptor2.txt')))


def test_save_in_fsl_convention_reload_as_dict_and_compare():
    _create_data_set_for_tests()

    ldm_itk = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    # change convention
    ldm_itk.convention = 'fsl'
    ldm_itk.save_label_descriptor(jph(ldg.pfo_target_atlas, 'label_descriptor_fsl.txt'))

    ldm_fsl = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor_fsl.txt'), labels_descriptor_convention='fsl')

    # NOTE: test works only with default 1.0 values - fsl convention is less informative than itk-snap..
    check_list_equal(ldm_itk.dict_label_descriptor.keys(), ldm_fsl.dict_label_descriptor.keys())
    for k in ldm_itk.dict_label_descriptor.keys():
        check_list_equal(ldm_itk.dict_label_descriptor[k], ldm_fsl.dict_label_descriptor[k])

    os.system('rm {}'.format(jph(ldg.pfo_target_atlas, 'label_descriptor_fsl.txt')))


# TESTING: labels permutations - permute_labels_in_descriptor


def test_relabel_labels_descriptor():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({10: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({11: [[0, 255, 0], [1.0, 1.0, 1.0], 'WM']})
    dict_expected.update({12: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})
    dict_expected.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))

    old_labels = [1, 2, 3]
    new_labels = [10, 11, 12]

    ldm_relabelled = ldm_original.relabel(old_labels, new_labels, sort=True)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


def test_relabel_labels_descriptor_with_merging():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    # dict_expected.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({1: [[0, 255, 0], [1.0, 1.0, 1.0], 'WM']})
    dict_expected.update({5: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})
    dict_expected.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))

    old_labels = [1, 2, 3]
    new_labels = [1, 1, 5]

    ldm_relabelled = ldm_original.relabel(old_labels, new_labels, sort=True)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])



def test_permute_labels_from_descriptor_wrong_input_permutation():
    _create_data_set_for_tests()

    ldm = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    perm = [[1, 2, 3], [1, 1]]

    with assert_raises(IOError):
        ldm.permute_labels(perm)


def test_permute_labels_from_descriptor_check():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({3: [[0, 255, 0], [1.0, 1.0, 1.0], 'WM']})
    dict_expected.update({2: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})
    dict_expected.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    perm = [[1, 2, 3], [1, 3, 2]]
    ldm_relabelled = ldm_original.permute_labels(perm)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


def test_erase_labels():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    labels_to_erase = [2, 3]
    ldm_relabelled = ldm_original.erase_labels(labels_to_erase)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


def test_erase_labels_unexisting_labels():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({3: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    labels_to_erase = [2, 4, 16, 32]
    ldm_relabelled = ldm_original.erase_labels(labels_to_erase)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


def test_assign_all_other_labels_the_same_value():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({1: [[255, 0, 0], [1.0, 1.0, 1.0], 'Skull']})
    dict_expected.update({4: [[255, 0, 255], [1.0, 1.0, 1.0], 'CSF']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    labels_to_keep = [1, 4]
    other_value = 0
    ldm_relabelled = ldm_original.assign_all_other_labels_the_same_value(labels_to_keep, other_value)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


def test_keep_one_label():
    _create_data_set_for_tests()

    dict_expected = collections.OrderedDict()
    dict_expected.update({0: [[0, 0, 0], [1.0, 1.0, 1.0], 'Bkg']})
    dict_expected.update({3: [[0, 0, 255], [1.0, 1.0, 1.0], 'GM']})

    ldm_original = LabelsDescriptorManager(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'))
    label_to_keep = 3
    ldm_relabelled = ldm_original.keep_one_label(label_to_keep)

    check_list_equal(dict_expected.keys(), ldm_relabelled.dict_label_descriptor.keys())
    for k in dict_expected.keys():
        check_list_equal(dict_expected[k], ldm_relabelled.dict_label_descriptor[k])


# TESTING: Generate dummy descriptor - generate_dummy_label_descriptor


def test_generate_dummy_labels_descriptor_wrong_input1():
    with assert_raises(IOError):
        generate_dummy_label_descriptor(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'), list_labels=range(5),
                                        list_roi_names=['1', '2'])


def test_generate_dummy_labels_descriptor_wrong_input2():
    with assert_raises(IOError):
        generate_dummy_label_descriptor(jph(ldg.pfo_target_atlas, 'label_descriptor.txt'), list_labels=range(5),
                                        list_roi_names=['1', '2', '3', '4', '5'],
                                        list_colors_triplets=[[0,0,0], [1,1,1]])
