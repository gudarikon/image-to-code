import pandas as pd

from src.text_to_code.prepare_dataset import prepare_dataset


def test_img_to_text(images_folder_path, codes_folder_path, ocr_preds_folder_path,  tmp_path):

    prepare_dataset(images_folder_path, codes_folder_path, ocr_preds_folder_path, tmp_path / "table.csv")

    table_path = tmp_path / "table.csv"

    df = pd.read_csv(table_path, index_col=0, encoding="utf-16")

    assert all([col in df.columns for col in ["image_path", "source_code", "predicted_code"]])
