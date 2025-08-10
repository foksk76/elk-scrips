import pytest
from unittest.mock import MagicMock
from unfreeze_indices import unfreeze_all_indices

def test_unfreeze_all_indices_no_frozen(monkeypatch):
    # Мокаем es_client.cat.indices возвращая пустой список
    es_client = MagicMock()
    es_client.cat.indices.return_value = []
    
    # Перехватим вывод print
    printed = []
    monkeypatch.setattr("builtins.print", lambda s: printed.append(s))
    
    unfreeze_all_indices(es_client)
    
    assert any("No frozen indices found" in line for line in printed)

def test_unfreeze_all_indices_success(monkeypatch):
    frozen = [
        {'index': 'index1', 'search.throttled': 'true'},
        {'index': 'index2', 'search.throttled': 'true'}
    ]
    es_client = MagicMock()
    es_client.cat.indices.return_value = frozen
    
    es_client.indices.unfreeze.return_value = None
    
    printed = []
    monkeypatch.setattr("builtins.print", lambda s: printed.append(s))
    
    unfreeze_all_indices(es_client)
    
    assert any("Found 2 frozen indices" in line for line in printed)
    assert any("Successfully unfroze index: index1" in line for line in printed)
    assert any("Successfully unfroze index: index2" in line for line in printed)
    assert any("Successfully unfroze 2/2 indices" in line for line in printed)

def test_unfreeze_all_indices_partial_failure(monkeypatch):
    frozen = [
        {'index': 'index1', 'search.throttled': 'true'},
        {'index': 'index2', 'search.throttled': 'true'}
    ]
    es_client = MagicMock()
    es_client.cat.indices.return_value = frozen
    
    def unfreeze_side_effect(index):
        if index == 'index1':
            return None
        else:
            raise Exception("fail")
    
    es_client.indices.unfreeze.side_effect = unfreeze_side_effect
    
    printed = []
    monkeypatch.setattr("builtins.print", lambda s: printed.append(s))
    
    unfreeze_all_indices(es_client)
    
    assert any("Successfully unfroze index: index1" in line for line in printed)
    assert any("Failed to unfreeze index index2: fail" in line for line in printed)
    assert any("Successfully unfroze 1/2 indices" in line for line in printed)
