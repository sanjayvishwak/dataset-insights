import numpy as np
import torch

from datasetinsights.data.bbox import BBox2D
from datasetinsights.estimators.faster_rcnn import (
    _gt_preds2tensor,
    convert_bboxes2canonical,
    list3d_2canonical,
    pad_box_lists,
    prepare_bboxes,
)

padding_box = BBox2D(
    label=np.nan, score=np.nan, x=np.nan, y=np.nan, w=np.nan, h=np.nan
)


def test_pad_box_lists():
    box_a, box_b = (
        BBox2D(label=0, x=10, y=10, w=10, h=10),
        BBox2D(label=1, x=20, y=20, w=10, h=10),
    )
    uneven_list = [
        ([box_a], []),
        ([box_a, box_b], [box_b]),
        ([box_b], [box_a, box_b]),
        ([box_b], [box_a]),
    ]

    actual_result = pad_box_lists(uneven_list, max_boxes_per_img=3)
    expected_result = [
        (
            [box_a, padding_box, padding_box],
            [padding_box, padding_box, padding_box],
        ),
        ([box_a, box_b, padding_box], [box_b, padding_box, padding_box]),
        ([box_b, padding_box, padding_box], [box_a, box_b, padding_box]),
        ([box_b, padding_box, padding_box], [box_a, padding_box, padding_box]),
    ]
    for i in range(len(expected_result)):
        assert len(expected_result[i][0]) == len(actual_result[i][0])
        assert len(expected_result[i][1]) == len(actual_result[i][1])
        for t_index in range(2):
            for j in range(len(expected_result[i][t_index])):
                if np.isnan(expected_result[i][t_index][j].label):
                    assert np.isnan(actual_result[i][t_index][j].label)
                else:
                    assert (
                        expected_result[i][t_index][j]
                        == actual_result[i][t_index][j]
                    )
    assert True


def test_list3d_2canonical():
    box_a, box_b = (
        BBox2D(label=0, x=10, y=10, w=10, h=10),
        BBox2D(label=1, x=20, y=20, w=10, h=10),
    )
    list3d = [
        [
            [
                [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
            [
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
        ],
        [
            [
                [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
            [
                [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
        ],
        [
            [
                [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
            [
                [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
        ],
        [
            [
                [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
            [
                [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
            ],
        ],
    ]
    expected_result = [
        ([box_a], []),
        ([box_a, box_b], [box_b]),
        ([box_b], [box_a, box_b]),
        ([box_b], [box_a]),
    ]
    actual_result = list3d_2canonical(list3d)
    assert actual_result == expected_result


def test_gt_preds2tensor():
    box_a, box_b = (
        BBox2D(label=0, x=10, y=10, w=10, h=10),
        BBox2D(label=1, x=20, y=20, w=10, h=10),
    )
    uneven_list = [
        ([box_a], []),
        ([box_a, box_b], [box_b]),
        ([box_b], [box_a, box_b]),
        ([box_b], [box_a]),
    ]
    actual_result = _gt_preds2tensor(uneven_list, 3)
    expected_result = torch.Tensor(
        [
            [
                [
                    [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
                [
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
            ],
            [
                [
                    [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                    [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
                [
                    [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
            ],
            [
                [
                    [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
                [
                    [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                    [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
            ],
            [
                [
                    [1.0, 1.0, 20.0, 20.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
                [
                    [0.0, 1.0, 10.0, 10.0, 10.0, 10.0],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
                ],
            ],
        ]
    )
    torch.eq(expected_result, actual_result)


def test_convert_empty():
    targets = prepare_bboxes([])
    assert len(targets["boxes"]) < 1


def _same_dict(expected, actual):
    assert len(expected.keys()) == len(actual.keys())
    for k in expected.keys():
        expected_tensor = expected[k]
        actual_tensor = actual[k]
        assert torch.all(torch.eq(expected_tensor, actual_tensor))
    return True


def _same_dict_list(expected, actual):
    assert len(expected) == len(actual)
    for i in range(len(expected)):
        _same_dict(expected[i], actual[i])
    return True


def test_convert2torchvision_format():
    boxes = [
        BBox2D(label=0, x=10, y=10, w=10, h=10),
        BBox2D(label=1, x=20, y=20, w=10, h=10),
    ]

    actual_targets = prepare_bboxes(boxes)
    expected_targets = {
        "boxes": torch.Tensor([[10, 10, 20, 20], [20, 20, 30, 30]]),
        "labels": torch.LongTensor([0, 1]),
    }

    assert _same_dict(expected_targets, actual_targets)


def same_list_of_list_of_bboxes(l_1, l_2):
    assert len(l_1) == len(l_2)
    for i in range(len(l_1)):
        assert len(l_1[i]) == len(l_2[i])
        for j in range(len(l_1[i])):
            assert l_1[i][j] == l_2[i][j]
    return True


def test_convert2canonical():
    boxes_rcnn_format = [
        {
            "boxes": torch.Tensor(
                [[10.5, 10.5, 20.5, 20.5], [20.5, 20.5, 30.5, 30.5]]
            ),
            "labels": torch.Tensor([0, 1]),
            "scores": torch.FloatTensor([0.3, 0.9]),
        }
    ]
    actual_result = convert_bboxes2canonical(boxes_rcnn_format)
    expected_result = [
        [
            BBox2D(label=0, x=10.5, y=10.5, w=10, h=10, score=0.3),
            BBox2D(label=1, x=20.5, y=20.5, w=10, h=10, score=0.9),
        ]
    ]
    assert same_list_of_list_of_bboxes(actual_result, expected_result)


def test_convert2canonical_batch():
    boxes_rcnn_format = [
        {
            "boxes": torch.Tensor([[10.0, 10, 20, 20], [20, 20, 30, 30]]),
            "labels": torch.LongTensor([0, 1]),
        },
        {
            "boxes": torch.Tensor([[10, 10, 20, 20], [20, 20, 30, 30]]),
            "labels": torch.LongTensor([2, 3]),
        },
    ]
    actual_result = convert_bboxes2canonical(boxes_rcnn_format)
    expected_result = [
        [
            BBox2D(label=0, x=10, y=10, w=10, h=10),
            BBox2D(label=1, x=20, y=20, w=10, h=10),
        ],
        [
            BBox2D(label=2, x=10, y=10, w=10, h=10),
            BBox2D(label=3, x=20, y=20, w=10, h=10),
        ],
    ]
    assert same_list_of_list_of_bboxes(actual_result, expected_result)
