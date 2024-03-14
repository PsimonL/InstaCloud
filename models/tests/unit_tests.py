import unittest
from unittest.mock import patch, MagicMock
from models.model import predict_class


class TestPredictClass(unittest.TestCase):
    @patch('models.model.cv2.imread')
    @patch('models.model.YOLO')
    def test_predict_dog(self, mock_yolo, mock_imread):
        # Set up mock return values
        mock_imread.return_value = 'image_data'
        mock_model = MagicMock()
        mock_model.predict.return_value = [MagicMock(names=['dog'], boxes=MagicMock(cls=[MagicMock(item=lambda: 0)]))]
        mock_yolo.return_value = mock_model

        # Call the function
        result = predict_class('dog.jpg')

        # Assert the expected outcome
        self.assertEqual(result, 'dog')

    @patch('models.model.cv2.imread')
    @patch('models.model.YOLO')
    def test_predict_cat(self, mock_yolo, mock_imread):
        # Setup mock return value
        mock_imread.return_value = 'image_data'
        mock_model = MagicMock()
        mock_model.predict.return_value = [MagicMock(names=['cat'], boxes=MagicMock(cls=[MagicMock(item=lambda: 0)]))]
        mock_yolo.return_value = mock_model

        # Call the function
        result = predict_class('cat.jpg')

        # Assert the expected outcome
        self.assertEqual(result, 'cat')

    @patch('models.model.cv2.imread')
    @patch('models.model.YOLO')
    def test_predict_random(self, mock_yolo, mock_imread):
        # Setup mock return value
        mock_imread.return_value = 'image_data'
        mock_model = MagicMock()
        mock_model.predict.return_value = [MagicMock(names=['giraffe'], boxes=MagicMock(cls=[MagicMock(item=lambda: 0)]))]
        mock_yolo.return_value = mock_model

        # Call the function
        result = predict_class('random.jpg')

        # Assert the expected outcome
        self.assertEqual(result, 'giraffe')


if __name__ == '__main__':
    unittest.main()
