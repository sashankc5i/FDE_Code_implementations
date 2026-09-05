import ast
from pathlib import Path

from src.model import build_model


def test_model_builds():
    assert build_model() is not None


def test_training_script_is_valid_python():
    script_path = Path(__file__).resolve().parents[1] / 'train_and_evaluate.py'
    source = script_path.read_text(encoding='utf-8')
    ast.parse(source)
