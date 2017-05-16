"""
Measurements on labels.
"""
import numpy as np
import os
import nibabel as nib
from tabulate import tabulate


class SegmentationAnalyzer(object):

    def __init__(self, pfi_segmentation='', pfi_scalar_im='', icv_factor=None, return_mm3=True):

        for p in [pfi_segmentation, pfi_scalar_im]:
            if not os.path.exists(p):
                IOError('Input data path {} does not exist.')

        self.pfi_segmentation = pfi_segmentation
        self.return_mm3 = return_mm3
        self.pfi_scalar_im = pfi_scalar_im
        self.icv_factor = icv_factor

        self._segmentation =  nib.load(self.pfi_segmentation)
        self._scalar_im = nib.load(self.pfi_scalar_im)

    def get_total_volume(self):

        num_voxels = np.count_nonzero(self._segmentation.get_data())

        if self.return_mm3:
            mm_3 = num_voxels * np.abs(np.prod(np.diag(self._segmentation.get_affine())))
            return mm_3
        else:
            return num_voxels

    def get_volumes_per_label(self, selected_labels, verbose=0):

        if isinstance(selected_labels, int):
            selected_labels = [selected_labels, ]

        # get tot volume
        tot_brain_volume = self.get_total_volume()

        # Get volumes per regions:
        voxels = np.zeros(len(selected_labels), dtype=np.uint64)

        for index_label_k, label_k in enumerate(selected_labels):
            places = self._segmentation.get_data()  == label_k
            voxels[index_label_k] = np.count_nonzero(places)

        vol = np.abs(np.prod(np.diag(self._segmentation.get_affine()))) * voxels.astype(np.float64)

        # get volumes over total volume:
        vol_over_tot = vol / float(tot_brain_volume)

        # get volume over ICV estimates
        if self.icv_factor is not None:
            vol_over_icv = vol / float(self.icv_factor)
        else:
            vol_over_icv = np.zeros_like(vol)

        # show a table at console:
        if verbose:
            headers = ['labels', 'Vol', 'Vol/totVol', 'Vol/ICV']
            table = [[r, v, v_t, v_icv] for r, v, v_t, v_icv in zip(selected_labels, vol, vol_over_tot, vol_over_icv)]
            print(tabulate(table, headers=headers))

        return vol, voxels, vol_over_tot, vol_over_icv

    def get_average_below_labels(self, selected_labels, verbose=1):

        if not os.path.exists(self.pfi_scalar_im):
            IOError('Input pfi_data missing')

        if isinstance(selected_labels, int):
            selected_labels = [selected_labels, ]
        elif isinstance(selected_labels, list):
            pass
        else:
            raise IOError('Input labels must be a list or an int.')

        assert self._scalar_im.shape == self._segmentation.get_data().shape

        # Get volumes per regions:
        values = np.zeros(len(selected_labels), dtype=np.float64)

        all_places = np.zeros_like(self._segmentation.get_data(), dtype=np.bool)

        for index_label_k, label_k in enumerate(selected_labels):

            all_places += self._segmentation.get_data() == label_k

            masked_scalar_data = all_places.astype(np.float64) * self._scalar_im.astype(np.float64)
            # remove zero elements from the array:
            non_zero_masked_scalar_data = (masked_scalar_data > 0.00000000001) * masked_scalar_data
            values[index_label_k] = np.mean(non_zero_masked_scalar_data)

            if verbose:
                print('Mean below the labels {0} : {1}'.format(selected_labels[index_label_k], values[index_label_k]))

        return values
