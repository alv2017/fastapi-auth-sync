import pytest

from api.apps.auth.passwords import hash_password, verify_password


class TestPasswordHashing:
    def test_hash_password(self):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password)

        assert len(password) < 72
        assert isinstance(hashed, str)
        assert hashed != password

    def test_hash_long_password(self):
        long_password = "Abracadabra" * 100
        hashed = hash_password(long_password)

        assert len(long_password) > 72
        assert isinstance(hashed, str)
        assert hashed != long_password

    def test_hash_different_salts(self):
        password = "My-strong-password-123!!!"
        hashed1 = hash_password(password)
        hashed2 = hash_password(password)

        assert hashed1 != hashed2

    @pytest.mark.parametrize("rounds", [8, 10, 12, 14])
    def test_hash_with_different_rounds(self, rounds):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password, rounds=rounds)

        assert isinstance(hashed, str)
        assert hashed != password


class TestPasswordVerification:
    def test_verify_correct_password_default_rounds(self):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.parametrize("rounds", [8, 10, 12, 14])
    def test_verify_correct_password(self, rounds):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password, rounds=rounds)

        assert verify_password(password, hashed) is True

    def test_verify_incorrect_password_default_rounds(self):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password)
        wrong_password = "Wrong-password-456!!!"

        assert password != wrong_password
        assert verify_password(wrong_password, hashed) is False

    @pytest.mark.parametrize("rounds", [8, 10, 12, 14])
    def test_verify_incorrect_password(self, rounds):
        password = "My-strong-password-123!!!"
        hashed = hash_password(password, rounds=rounds)
        wrong_password = "Wrong-password-456!!!"

        assert password != wrong_password
        assert verify_password(wrong_password, hashed) is False

    @pytest.mark.parametrize("rounds", [8, 10, 12, 14])
    def test_verify_long_password_default_rounds(self, rounds):
        password = "Abracadabra" * 100
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True

    @pytest.mark.parametrize("rounds", [8, 10, 12, 14])
    def test_verify_long_password(self, rounds):
        password = "Abracadabra" * 100
        hashed = hash_password(password, rounds=rounds)

        assert verify_password(password, hashed) is True

    def test_verify_invalid_hash(self):
        password = "My-strong-password-123!!!"
        invalid_hashed = "invalid-hash-string"

        assert verify_password(password, invalid_hashed) is False
