import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

# from django.core.exceptions import ValidationError
# from psycopg.errors import UniqueViolation


@pytest.mark.accounts
@pytest.mark.django_db
class TestAccount:
    """tests different user creations scenarios"""

    def test_create_standard_user(self, user_st):
        """tests creating standard user account"""

        Account = get_user_model()

        assert user_st.email == "test@user.com"
        assert user_st.is_active is True
        assert user_st.is_staff is False
        assert user_st.is_superuser is False

        assert user_st.is_moderator is False
        assert user_st.is_admin is False

        try:
            assert user_st.username is None
        except AttributeError:
            pass

        with pytest.raises(TypeError):
            # no data passed
            Account.objects.create_user()

        with pytest.raises(TypeError):
            # passed only email
            Account.objects.create_user(email="")

        with pytest.raises(TypeError):
            # passed only password
            Account.objects.create_user(password="")

        with pytest.raises(TypeError):
            # passed only pesel
            Account.objects.create_user(pesel="10010010022")

        with pytest.raises(ValueError):
            # email left empty
            Account.objects.create_user(
                email="",
                password="foo",
                pesel="10010010022",
            )

        with pytest.raises(ValueError):
            # password left empty
            Account.objects.create_user(
                email="dummy@user.com",
                password="",
                pesel="10010010022",
            )

        with pytest.raises(ValueError):
            # pesel left wrong
            Account.objects.create_user(
                email="dummy@user.com",
                password="foo",
                pesel="123",
            )

    def test_create_superuser(self, user_ad):
        """tests creating super user"""

        Account = get_user_model()

        assert user_ad.email == "test@admin.com"
        assert user_ad.is_active
        assert user_ad.is_staff
        assert user_ad.is_superuser

        assert user_ad.is_admin is True

        try:
            assert user_ad.username is None
        except AttributeError:
            pass

        with pytest.raises(ValueError):
            Account.objects.create_superuser(
                email="super@user.io",
                password="foo",
                pesel="20020020011",
                is_superuser=False,
            )

    def test_create_moderator(self, user_md):
        """tests creating moderator"""

        Account = get_user_model()

        assert user_md.email == "test@mod.com"
        assert user_md.is_active
        assert user_md.is_staff
        assert user_md.is_superuser is False

        assert user_md.is_admin is False
        assert user_md.is_moderator

        with pytest.raises(ValueError):
            Account.objects.create_moderator(
                email="test@mod.io",
                password="Foo",
                pesel="34534534512",
                is_superuser=True,
            )

    def test_check_duplicate(self, user_st):
        """tests catching duplicate emails when creating accounts"""

        Account = get_user_model()

        # same email
        with pytest.raises(IntegrityError):
            Account.objects.create_user(
                email="test@user.com",
                first_name="John",
                last_name="Doe",
                password="foo",
                pesel="12312312344",
            )

    def test_check_duplicate2(self, user_st):
        """tests catching duplicate pesels when creating accounts"""

        Account = get_user_model()

        with pytest.raises(IntegrityError):
            Account.objects.create_user(
                email="test@user.io",
                first_name="John",
                last_name="Doe",
                password="foo",
                pesel="12312312311",
            )

    def test_check_groups(self, user_st, user_ad, user_md):
        """tests assigining groups to users during creation process"""

        Account = get_user_model()
        # Account = Acc()

        assert user_st.type is Account.AccountType.STANDARD
        assert user_ad.type is Account.AccountType.ADMIN
        assert user_md.type is Account.AccountType.MODERATOR

        assert user_st.is_admin is False
        assert user_st.is_moderator is False

        assert user_ad.is_admin is True

        assert user_md.is_admin is False
        assert user_md.is_moderator is True

    def test_check_group_permissions(self, user_st, user_ad, user_md):
        """tests correct permissions for users"""

        perms_st = user_st.get_all_permissions()
        perms_ad = user_ad.get_all_permissions()
        perms_md = user_md.get_all_permissions()

        for perm in perms_st:
            _, perm = perm.split(".")

            assert perm.startswith("view_")

        for perm in perms_ad:
            _, perm = perm.split(".")

            assert perm.startswith(("view_", "change_", "add_", "delete_"))

        for perm in perms_md:
            _, perm = perm.split(".")

            assert perm.startswith(("view_", "change_"))
