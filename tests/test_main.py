import unittest
from unittest.mock import call, patch

import numpy as np

import main as app


class ComputeMeanColorTests(unittest.TestCase):
    def test_returns_channel_wise_mean_as_floats(self):
        image = np.array(
            [
                [[0, 10, 20], [20, 30, 40]],
                [[40, 50, 60], [60, 70, 80]],
            ],
            dtype=np.uint8,
        )

        result = app.compute_mean_color(image)

        np.testing.assert_allclose(result, [30.0, 40.0, 50.0])
        self.assertEqual(result.dtype, float)


class MainWorkflowTests(unittest.TestCase):
    @patch.object(app, "Camera")
    @patch.object(app, "Plugin")
    def test_captures_publishes_and_uploads_snapshot(self, plugin_class, camera_class):
        plugin = plugin_class.return_value.__enter__.return_value
        camera = camera_class.return_value.__enter__.return_value
        snapshot = camera.snapshot.return_value
        snapshot.data = np.array([[[10, 20, 30]]], dtype=np.uint8)
        snapshot.timestamp = 123456789

        app.main()

        camera_class.assert_called_once_with("left")
        plugin.publish.assert_has_calls(
            [
                call("color.mean.r", 10.0, timestamp=123456789),
                call("color.mean.g", 20.0, timestamp=123456789),
                call("color.mean.b", 30.0, timestamp=123456789),
            ]
        )
        snapshot.save.assert_called_once_with("snapshot.jpg")
        plugin.upload_file.assert_called_once_with(
            "snapshot.jpg", timestamp=123456789
        )


if __name__ == "__main__":
    unittest.main()
