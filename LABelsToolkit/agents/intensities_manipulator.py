import nibabel as nib
import numpy as np

from LABelsToolkit.tools.aux_methods.utils_path import get_pfi_in_pfi_out, connect_path_tail_head
from LABelsToolkit.tools.aux_methods.utils import labels_query
from LABelsToolkit.tools.image_colors_manipulations.normaliser import normalise_below_labels
from LABelsToolkit.tools.detections.contours import contour_from_segmentation
from LABelsToolkit.tools.image_shape_manipulations.merger import grafting


class LABelsToolkitIntensitiesManipulate(object):
    """
    Facade of the methods in tools, for work with paths to images rather than
    with data. Methods under LabelsManagerManipulate are taking in general
    one or more input manipulate them according to some rule and save the
    output in the output_data_folder or in the specified paths.
    """
    # TODO add filename for labels descriptors and manipulations of labels descriptors.

    def __init__(self, input_data_folder=None, output_data_folder=None):
        self.pfo_in = input_data_folder
        self.pfo_out = output_data_folder

    def normalise_below_label(self, pfi_input, pfi_output, filename_segm, labels, stats=np.median):
        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input, pfi_output, self.pfo_in, self.pfo_out)
        pfi_segm = connect_path_tail_head(self.pfo_in, filename_segm)

        im_input = nib.load(pfi_in)
        im_segm = nib.load(pfi_segm)

        labels_list, labels_names = labels_query(labels, im_segm.get_data())
        im_out = normalise_below_labels(im_input, labels_list, labels, stats=stats, exclude_first_label=True)

        nib.save(im_out, pfi_out)

    def get_contour_from_segmentation(self, pfi_input_segmentation, pfi_output_contour, omit_axis=None, verbose=0):
        pfi_in, pfi_out = get_pfi_in_pfi_out(pfi_input_segmentation, pfi_output_contour, self.pfo_in, self.pfo_out)
        im_segm = nib.load(pfi_in)

        im_contour = contour_from_segmentation(im_segm, omit_axis=omit_axis, verbose=verbose)

        nib.save(im_contour, pfi_output_contour)

    def get_grafting(self, pfi_input_hosting_mould, pfi_input_patch, pfi_output_grafted, pfi_input_patch_mask=None):
        pfi_hosting = connect_path_tail_head(self.pfo_in, pfi_input_hosting_mould)
        pfi_patch = connect_path_tail_head(self.pfo_in, pfi_input_patch)

        im_hosting = nib.load(pfi_hosting)
        im_patch   = nib.load(pfi_patch)
        im_mask    = None

        if pfi_input_patch_mask is not None:
            pfi_mask = connect_path_tail_head(self.pfo_in, pfi_input_patch_mask)
            im_mask  = nib.load(pfi_mask)

        im_grafted = grafting(im_hosting, im_patch, im_patch_mask=im_mask)

        pfi_output = connect_path_tail_head(self.pfo_out, pfi_output_grafted)
        nib.save(im_grafted, pfi_output)

