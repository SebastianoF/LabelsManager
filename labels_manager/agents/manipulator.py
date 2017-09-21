import nibabel as nib
import numpy as np

from labels_manager.tools.aux_methods.utils_path import get_pfi_in_pfi_out, connect_path_tail_head
from labels_manager.tools.aux_methods.utils_nib import set_new_data
from labels_manager.tools.aux_methods.utils import labels_query
from labels_manager.tools.image_colors_manipulations.cutter import cut_4d_volume_with_a_1_slice_mask_nib
from labels_manager.tools.image_colors_manipulations.relabeller import relabeller, \
    permute_labels, erase_labels, assign_all_other_labels_the_same_value, keep_only_one_label
from labels_manager.tools.image_shape_manipulations.merger import merge_labels_from_4d
from labels_manager.tools.image_shape_manipulations.splitter import split_labels_to_4d
from labels_manager.tools.image_colors_manipulations.normaliser import normalise_below_labels
from labels_manager.tools.detections.contours import contour_from_segmentation

class LabelsManagerManipulate(object):
    """
    Facade of the methods in tools, for work with paths to images rather than
    with data. Methods under LabelsManagerManipulate are taking in general
    one or more input manipulate them according to some rule and save the
    output in the output_data_folder or in the specified paths.
    """
    # TODO add filename for labels descriptors and manipulations of labels descriptors

    def __init__(self, input_data_folder=None, output_data_folder=None):
        self.pfo_in = input_data_folder
        self.pfo_out = output_data_folder

    def relabel(self, pfi_input, pfi_output=None, list_old_labels=(),
                list_new_labels=()):
        """
        Masks of :func:`labels_manager.tools.manipulations.relabeller.relabeller` using filename
        """

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in,
                                             self.pfo_out)
        im_labels = nib.load(pfi_in)
        data_labels = im_labels.get_data()
        data_relabelled = relabeller(data_labels, list_old_labels=list_old_labels,
                                     list_new_labels=list_new_labels)

        im_relabelled = set_new_data(im_labels, data_relabelled)

        nib.save(im_relabelled, pfi_out)
        print('Relabelled image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def permute_labels(self, pfi_input, pfi_output=None, permutation=()):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels = nib.load(pfi_in)
        data_labels = im_labels.get_data()
        data_permuted = permute_labels(data_labels, permutation=permutation)

        im_permuted = set_new_data(im_labels, data_permuted)
        nib.save(im_permuted, pfi_out)
        print('Permuted labels from image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def erase_labels(self, pfi_input, pfi_output=None, labels_to_erase=()):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels = nib.load(pfi_in)
        data_labels = im_labels.get_data()
        data_erased = erase_labels(data_labels, labels_to_erase=labels_to_erase)

        im_erased = set_new_data(im_labels, data_erased)
        nib.save(im_erased, pfi_out)
        print('Erased labels from image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def assign_all_other_labels_the_same_value(self, pfi_input, pfi_output=None,
        labels_to_keep=(), same_value_label=255):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels = nib.load(pfi_in)
        data_labels = im_labels.get_data()
        data_reassigned = assign_all_other_labels_the_same_value(data_labels,
                                labels_to_keep=labels_to_keep, same_value_label=same_value_label)

        im_reassigned = set_new_data(im_labels, data_reassigned)
        nib.save(im_reassigned, pfi_out)
        print('Reassigned labels from image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def keep_one_label(self, pfi_input, pfi_output=None, label_to_keep=1):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels = nib.load(pfi_in)
        data_labels = im_labels.get_data()
        data_one_label = keep_only_one_label(data_labels, label_to_keep)

        im_one_label = set_new_data(im_labels, data_one_label)
        nib.save(im_one_label, pfi_out)
        print('Label {0} kept from image {1} and saved in {2}.'.format(label_to_keep, pfi_in, pfi_out))
        return pfi_out

    def extend_slice_new_dimension(self, pfi_input, pfi_output=None, new_axis=3, num_slices=10):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_slice = nib.load(pfi_in)
        data_slice = im_slice.get_data()

        data_extended = np.stack([data_slice, ] * num_slices, axis=new_axis)

        im_extended = set_new_data(im_slice, data_extended)
        nib.save(im_extended, pfi_out)
        print('Extended image of {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def split_in_4d(self, pfi_input, pfi_output=None, list_labels=None, keep_original_values=True):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels_3d = nib.load(pfi_in)
        data_labels_3d = im_labels_3d.get_data()
        assert len(data_labels_3d.shape) == 3
        if list_labels is None:
            list_labels = list(np.sort(list(set(data_labels_3d.flat))))
        data_split_in_4d = split_labels_to_4d(data_labels_3d, list_labels=list_labels, keep_original_values=keep_original_values)

        im_split_in_4d = set_new_data(im_labels_3d, data_split_in_4d)
        nib.save(im_split_in_4d, pfi_out)
        print('Split labels from image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def merge_from_4d(self, pfi_input, pfi_output=None):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)

        im_labels_4d = nib.load(pfi_in)
        data_labels_4d = im_labels_4d.get_data()
        assert len(data_labels_4d.shape) == 4
        data_merged_in_3d = merge_labels_from_4d(data_labels_4d)

        im_merged_in_3d = set_new_data(im_labels_4d, data_merged_in_3d)
        nib.save(im_merged_in_3d, pfi_out)
        print('Merged labels from 4d image {0} saved in {1}.'.format(pfi_in, pfi_out))
        return pfi_out

    def cut_4d_volume_with_a_1_slice_mask(self, pfi_input, filename_mask, pfi_output=None):

        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)
        pfi_mask = connect_path_tail_head(self.pfo_in, filename_mask)

        im_dwi = nib.load(pfi_in)
        im_mask = nib.load(pfi_mask)

        im_masked = cut_4d_volume_with_a_1_slice_mask_nib(im_dwi, im_mask)

        nib.save(im_masked, pfi_out)

    def normalise_below_label(self, pfi_input, pfi_output, filename_segm, labels, stats=np.median):
        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)
        pfi_segm = connect_path_tail_head(self.pfo_in, filename_segm)

        im_input = nib.load(pfi_in)
        im_segm = nib.load(pfi_segm)

        labels_list, labels_names = labels_query(labels, im_segm.get_data(), exclude_zero=True)
        im_out = normalise_below_labels(im_input, labels_list, labels, stats=stats)

        nib.save(im_out, pfi_out)
        
    def get_contour_from_segmentation(self, pfi_input_segmenation, pfi_output_contour, omit_axis=None, verbose=0):
        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input_segmenation, pfi_output_contour, self.pfo_in, self.pfo_out)
        im_segm = nib.load(pfi_in)

        im_contour = contour_from_segmentation(im_segm, omit_axis=omit_axis, verbose=verbose)

        nib.save(im_contour, pfi_output_contour)

